
from odoo import models, fields, api
from odoo.exceptions import ValidationError


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
    volume = fields.Float(digits=(6,6), compute="_volume", store=True, string= "Volume m3")
    literal = fields.Char(store=False)
    peso = fields.Float(digits=(6,2), default =2.7, string="Peso en KG.s/m3:")
    densidade = fields.Float(compute="_densidade", store=True, string="Densidade en KG/m3:")
    autorizado = fields.Boolean(default = True, string="¿Autorizado?")
    sexo_traducido = fields.Selection([('Hombre','Home'), ('Mujer','Muller'), ('Otros','Outros')], string="Sexo:")

    foto = fields.Binary(string='Foto')
    adxunto_nome = fields.Char(string="Nome Adxunto")
    adxunto = fields.Binary(string="Arquivo adxunto")

    #os campos Man2one crean un campo na BD
    moeda_id = fields.Many2one('res.currency', domain="[('position','=','after')]")

    # con domain, filtramos os valores mostrados. Pode ser mediante unha constante (vai entre comillas) ou unha variable
    moeda_euro_id = fields.Many2one('res.currency', default=lambda self: self.env['res.currency'].search([('name', '=', "EUR")], limit=1))
    gasto_en_euros = fields.Monetary("Gasto en Euros", 'moeda_euro_id')
    moeda_en_texto = fields.Char(related="moeda_id.currency_unit_label", string="Moeda en formato texto", store=True)
    creador_da_moeda = fields.Char(related="moeda_id.create_uid.login", string="Usuario creador da moeda", store=True)


    @api.depends('alto_en_cms', 'longo_en_cms', 'ancho_en_cms')
    def _volume(self):
        for rexistro in self:
            rexistro.volume = (float(rexistro.alto_en_cms) * float(rexistro.longo_en_cms) * float(rexistro.ancho_en_cms))/ 1000000

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

