from odoo import models, fields, api

class CafeOrderLine(models.Model):
    _inherit = 'cafe.order.line'

    product_id = fields.Many2one('product.product', 'Product')

class CafePegawai(models.Model):
    _inherit = 'cafe.pegawai'

    @api.multi
    def action_view_order(self):
        action = self.env.ref('cafe.cafe_order_action').read()[0]
        action['domain'] = [('pegawai_id', '=', self.id)]
        return action
        # if len(invoices) > 1:
        #     action['domain'] = [('id', 'in', invoices.ids)]
        # elif len(invoices) == 1:
        #     action['views'] = [(self.env.ref('account.invoice_form').id, 'form')]
        #     action['res_id'] = invoices.ids[0]
        # else:
        #     action = {'type': 'ir.actions.act_window_close'}