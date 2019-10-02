from odoo import models, fields, api

class CafeOrderLine(models.Model):
    _inherit = 'cafe.order.line'

    product_id = fields.Many2one('product.product', 'Product')