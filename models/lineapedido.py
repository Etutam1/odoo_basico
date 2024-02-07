from odoo import models, fields, api
from odoo.exceptions import ValidationError


class lineapedido(models.Model):
    _name = 'odoo_basico.lineapedido'
    _description = 'exemplo linea pedido'
    _order = 'name asc'

    name = fields.Char(required=True, size=20, string="Linea Pedido:")
    descripcion = fields.Text(string="Descripción da Línea Pedido:")

    # Os campos One2many Non se almacenan na BD
    pedido_id = fields.Many2one('odoo_basico.pedido', ondelete="cascade", required=True)

    informacion_ids = fields.Many2many("odoo_basico.informacion",
                                       string="Rexistro de Información",
                                       relation="odoo_basico_lineapedido_informacion",
                                       column1="lineapedido_id", column2="informacion_id")