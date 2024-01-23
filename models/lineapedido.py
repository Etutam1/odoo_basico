from odoo import models, fields, api
from odoo.exceptions import ValidationError


class lineapedido(models.Model):
    _name = 'odoo_basico.lineapedido.xml'
    _description = 'exemplo linea pedido'
    name = fields.Char(required=True, size=20, string="Linea Pedido:")

    # Os campos One2many Non se almacenan na BD
    pedido_id = fields.Many2one('odoo_basico.pedido',
                                ondelete="cascade", required=True)