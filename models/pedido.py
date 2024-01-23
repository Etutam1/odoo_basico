from odoo import models, fields, api
from odoo.exceptions import ValidationError


class pedido(models.Model):
    _name = 'odoo_basico.pedido'

    name = fields.Char(required=True, size=20, string="Pedido:")
    # Os campos One2many Non se almacenan na BD
    lineapedido_ids = fields.One2many("odoo_basico.lineapedido.xml", 'pedido_id')

