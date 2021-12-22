from odoo import models, fields, api
from odoo.exceptions import ValidationError, Warning

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    _description = 'Sale Order'

    ratecard_id = fields.Many2one('rate.card', string='Rate Card')
