import os

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools.safe_eval import pytz
import locale
from . import miñasUtilidades
from odoo.exceptions import Warning

class informacion(models.Model):
    _name = 'odoo_basico.informacion'
    _description = 'exemplo de odoo basico'
    _sql_constraints = [('nomeUnico', 'unique(name)', 'Non se pode repetir o nome')]
    _order = 'descripcion desc'

    name = fields.Char(required=True, size=20, string="Titulo:")
    descripcion = fields.Text(string="A descripción:")
    alto_en_cms = fields.Integer(string="Alto en centímetros:")
    longo_en_cms = fields.Integer(string="Longo en centímetros:")
    ancho_en_cms = fields.Integer(string="Ancho en centímetros:")
    volume = fields.Float(digits=(6, 6), compute="_volume", store=True, string="Volume m3")
    literal = fields.Char(store=False)
    peso = fields.Float(digits=(6, 2), default=2.7, string="Peso en KG.s/m3:")
    densidade = fields.Float(compute="_densidade", store=True, string="Densidade en KG/m3:")
    autorizado = fields.Boolean(default=True, string="¿Autorizado?")
    sexo_traducido = fields.Selection([('Hombre', 'Home'), ('Mujer', 'Muller'), ('Otros', 'Outros')], string="Sexo:")

    foto = fields.Binary(string='Foto')
    adxunto_nome = fields.Char(string="Nome Adxunto")
    adxunto = fields.Binary(string="Arquivo adxunto")

    # os campos Man2one crean un campo na BD
    moeda_id = fields.Many2one('res.currency', domain="[('position','=','after')]")

    # con domain, filtramos os valores mostrados. Pode ser mediante unha constante (vai entre comillas) ou unha variable
    moeda_euro_id = fields.Many2one('res.currency',
                                    default=lambda self: self.env['res.currency'].search([('name', '=', "EUR")],
                                                                                         limit=1))
    gasto_en_euros = fields.Monetary("Gasto en Euros", 'moeda_euro_id')
    moeda_en_texto = fields.Char(related="moeda_id.currency_unit_label", string="Moeda en formato texto", store=True)
    creador_da_moeda = fields.Char(related="moeda_id.create_uid.login", string="Usuario creador da moeda", store=True)
    data = fields.Date(string="Data", default=lambda self: fields.Date.today())
    data_hora = fields.Datetime(string="Data e Hora", default=lambda self: fields.Datetime.now())
    hora_utc = fields.Char(compute="_hora_utc", string="Hora UTC", size=15, store=True)
    hora_actual = fields.Char(compute="_hora_actual", string="Hora Actual", size=15, store=True)
    hora_timezone_usuario = fields.Char(compute="_hora_timezone_usuario", string="Hora Timezone do Usuario", size=15,
                                        store=True)

    mes_castelan= fields.Char(compute="_mes_castelan", string="Mes en castelan", size=15, store=True)
    mes_galego= fields.Char(compute="_mes_galego", string="Mes en galego", size=15, store=True)
    mes_ingles= fields.Char(compute="_mes_ingles", string="Mes en inglés", size=15, store=True)
    mes_frances =fields.Char(compute="_mes_frances", string="Mes en frances", size=15, store=True)

    @api.depends('alto_en_cms', 'longo_en_cms', 'ancho_en_cms')
    def _volume(self):
        for rexistro in self:
            rexistro.volume = (float(rexistro.alto_en_cms) * float(rexistro.longo_en_cms) * float(
                rexistro.ancho_en_cms)) / 1000000

    @api.depends('volume', 'peso')
    def _densidade(self):
        for rexistro in self:
            if rexistro.volume != 0:
                rexistro.densidade = float(rexistro.peso) / float(rexistro.volume)
            else:
                rexistro.densidade = 0

    @api.onchange('alto_en_cms')
    def _avisoAlto(self):
        for rexistro in self:
            if rexistro.alto_en_cms > 7:
                rexistro.literal = 'O alto ten un valor posiblemente excesivo %s é maior que 7' % rexistro.alto_en_cms
            else:
                rexistro.literal = ""

    @api.constrains('peso')  # Ao usar ValidationError temos que importar a libreria ValidationError
    def _constrain_peso(self):  # from odoo.exceptions import ValidationError
        for rexistro in self:
            if rexistro.peso < 1 or rexistro.peso > 4:
                raise ValidationError('Os peso de %s ten que ser entre 1 e 4 ' % rexistro.name)

    def _cambia_campo_sexo(self, rexistro):
        rexistro.sexo_traducido = "Hombre"

    def envio_email(self):
        meu_usuario = self.env.user
        # mail_de     Odoo pon o email que configuramos en gmail para facer o envio
        mail_reply_to = meu_usuario.partner_id.email  # o enderezo email que ten asociado o noso usuario
        mail_para = 'etutamc@gmail.com'  # o enderezo email de destino
        mail_valores = {
            'subject': 'Correo para "%s"' %self.name,
            'author_id': meu_usuario.id,
            'email_from': mail_reply_to,
            'email_to': mail_para,
            'message_type': 'email',
            'body_html': 'Datos %s: '
            '<br/> Sexo: %s, Altura: %s, Moneda: %s' % (self.name, self.sexo_traducido, self.alto_en_cms, self.moeda_id.name)
        }
        mail_id = self.env['mail.mail'].create(mail_valores)
        mail_id.sudo().send()
        return True

    @api.depends('data_hora')
    def _hora_utc(self):
        for rexistro in self:  # A hora se almacena na BD en horario UTC (2 horas menos no verán, 1 hora menos no inverno)
            rexistro.hora_utc = rexistro.data_hora.strftime("%H:%M:%S")

    def actualiza_hora_actual_UTC(
            self):  # Esta función é chamada dende un boton de informacion.xml e dende _hora_actual
        for rexistro in self:
            rexistro.hora_actual = fields.Datetime.now().strftime("%H:%M:%S")
        # Grava a hora en UTC, se quixesemos poderiamos usar a función  _convirte_data_hora_de_utc_a_timezone_do_usuario

    @api.depends('data_hora')
    def _hora_actual(self):
        for rexistro in self:
            rexistro.actualiza_hora_actual_UTC()

        # Esta función será chamada dende a función actualiza_hora_timezone_usuario_dende_boton_e_apidepends e
        #  dende pedido.py (Cando insertamos os valores do template self.env.user.tz non ten o timezone do usuario por iso se carga coa hora UTC,
        #  o botón en pedido.py é para actualizar todos os rexistros masivamente dende outro modelo)

    def actualiza_hora_timezone_usuario(self, obxeto_rexistro):
        obxeto_rexistro.hora_timezone_usuario = self.convirte_data_hora_de_utc_a_timezone_do_usuario(obxeto_rexistro.data_hora).strftime("%H:%M:%S")  # Convertimos a hora de UTC a hora do timezone do usuario

    def convirte_data_hora_de_utc_a_timezone_do_usuario(self, data_hora_utc_object):  # recibe a data hora en formato object
        usuario_timezone = pytz.timezone(self.env.user.tz or 'UTC')  # obter a zona horaria do usuario. Ollo!!! nas preferencias do usuario ten que estar ben configurada a zona horaria
        return pytz.UTC.localize(data_hora_utc_object).astimezone(usuario_timezone)  # hora co horario do usuario en formato object
        # para usar  pytz temos que facer  import pytz

    def actualiza_hora_timezone_usuario_dende_boton_e_apidepends(
            self):  # Esta función é chamada dende un boton de informacion.xml e dende @api.depends _hora_timezone_usuario
        self.actualiza_hora_timezone_usuario(
            self)  # leva self como parametro por que actualiza_hora_timezone_usuario ten 2 parametros
        # porque usamos tamén actualiza_hora_timezone_usuario dende outro modelo (pedido.py) e lle pasamos como parámetro o obxeto_rexistro
    @api.depends('data_hora')
    def _hora_timezone_usuario(self):
        for rexistro in self:
            rexistro.actualiza_hora_timezone_usuario_dende_boton_e_apidepends()

    # Podemos  configurar locales a nivel de sistema con dpkg-reconfigure locales poñendo un por defecto.
    # apt-get install locales
    # dpkg-reconfigure locales (podemos configurar varios)
    # locale (ver o locale por defecto)
    # locale -a (ver os dispoñibles)

    @api.depends('data')
    def _mes_castelan(self):
        # O idioma por defecto é o configurado en locale na máquina onde se executa odoo.
        # Podemos cambialo con locale.setlocale, os idiomas teñen que estar instalados na máquina onde se executa odoo.
        # Lista onde podemos ver os distintos valores: https://docs.moodle.org/dev/Table_of_locales#Table
        # Definimos en miñasUtilidades un método para asignar o distinto literal que ten o idioma en función da plataforma Windows ou GNULinux
        locale.setlocale(locale.LC_TIME, miñasUtilidades.cadeaTextoSegunPlataforma('Spanish_Spain.1252', 'es_ES.utf8'))
        for rexistro in self:
            rexistro.mes_castelan = rexistro.data.strftime("%B")  # strftime https://strftime.org/

    @api.depends('data')
    def _mes_galego(self):
        # O idioma por defecto é o configurado en locale na máquina onde se executa odoo.
        # Podemos cambialo con locale.setlocale, os idiomas teñen que estar instalados na máquina onde se executa odoo.
        # Lista onde podemos ver os distintos valores: https://docs.moodle.org/dev/Table_of_locales#Table
        # Definimos en miñasUtilidades un método para asignar o distinto literal que ten o idioma en función da plataforma Windows ou GNULinux
        locale.setlocale(locale.LC_TIME, miñasUtilidades.cadeaTextoSegunPlataforma('Galician_Spain.1252', 'gl_ES.utf8'))
        for rexistro in self:
            rexistro.mes_galego = rexistro.data.strftime("%B")
        locale.setlocale(locale.LC_TIME, miñasUtilidades.cadeaTextoSegunPlataforma('Spanish_Spain.1252', 'es_ES.utf8'))

    @api.depends('data')
    def _mes_ingles(self):
        # O idioma por defecto é o configurado en locale na máquina onde se executa odoo.
        # Podemos cambialo con locale.setlocale, os idiomas teñen que estar instalados na máquina onde se executa odoo.
        # Lista onde podemos ver os distintos valores: https://docs.moodle.org/dev/Table_of_locales#Table
        # Definimos en miñasUtilidades un método para asignar o distinto literal que ten o idioma en función da plataforma Windows ou GNULinux
        locale.setlocale(locale.LC_TIME, miñasUtilidades.cadeaTextoSegunPlataforma('english_united kingdom', 'en_GB.utf8'))
        for rexistro in self:
            rexistro.mes_ingles = rexistro.data.strftime("%B")
        locale.setlocale(locale.LC_TIME, miñasUtilidades.cadeaTextoSegunPlataforma('english_united kingdom', 'en_GB.utf8'))

    @api.depends('data')
    def _mes_frances(self):
        # O idioma por defecto é o configurado en locale na máquina onde se executa odoo.
        # Podemos cambialo con locale.setlocale, os idiomas teñen que estar instalados na máquina onde se executa odoo.
        # Lista onde podemos ver os distintos valores: https://docs.moodle.org/dev/Table_of_locales#Table
        # Definimos en miñasUtilidades un método para asignar o distinto literal que ten o idioma en función da plataforma Windows ou GNULinux
        locale.setlocale(locale.LC_TIME, miñasUtilidades.cadeaTextoSegunPlataforma('Galician_Spain.1252', 'fr_FR.utf8'))
        for rexistro in self:
            rexistro.mes_frances = rexistro.data.strftime("%B")
        locale.setlocale(locale.LC_TIME, miñasUtilidades.cadeaTextoSegunPlataforma('french_france', 'fr_FR.utf8'))

    def ver_contexto(self):  # Este método é chamado dende un botón de informacion.xml
        for rexistro in self:
            # Ao usar warning temos que importar a libreria mediante from odoo.exceptions import Warning
            # Importamos tamén a libreria os mediante import os
            raise ValidationError(
                'Contexto: %s Ruta: %s Contido %s' % (rexistro.env.context, os.getcwd(), os.listdir(os.getcwd())))
            # env.context é un diccionario  https://www.w3schools.com/python/python_dictionaries.asp
        return True
