from odoo import models, fields, api
from odoo.exceptions import ValidationError


class pedido(models.Model):
    _name = 'odoo_basico.informacion'
    _description = 'exemplo de odoo basico'
    # Os campos One2many Non se almacenan na BD
    lineapedido_ids = fields.One2many("odoo_basico.lineapedido", 'pedido_id')
    # Os campos Many2one crean un campo na BD
    pedido_id = fields.Many2one('odoo_basico.pedido',
                                ondelete="cascade", required=True)