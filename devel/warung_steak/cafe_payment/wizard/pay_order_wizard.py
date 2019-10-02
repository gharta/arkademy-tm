from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError

class PayOrderWizard(models.TransientModel):

    _name = 'pay.order.wizard'

    amount_total = fields.Float(string='Amount Total')
    payment_amount = fields.Float(string='Payment Amount')
    payment_return = fields.Float(string='Payment Return', compute='_compute_price')

    @api.depends('payment_amount')
    def _compute_price(self):
        for doc in self:
            doc.payment_return = doc.amount_total - doc.payment_amount

    # @api.onchange('payment_amount')
    # def get_price(self):
    #     self.payment_return = self.amount_total - self.payment_amount

    @api.model
    def default_get(self, default_fields):
        res = super(PayOrderWizard, self).default_get(default_fields)

        ids_to_change = self._context.get('active_ids')
        # 1. Panggil Table
        Order = self.env['cafe.order']
        # 2. Browse
        list_orders = Order.browse(ids_to_change)
        # 3. Ambil fieldnya
        if list_orders:
            order = list_orders[0]
            res.update({
                'amount_total': order.amount_total,
                'payment_amount': 0,
                'payment_return': order.amount_total,
            })
        return res

    def process_wizard(self):
        # Hands On : Validasi Payment Amount
        ids_to_change = self._context.get('active_ids')
        # 1. Panggil Table
        Order = self.env['cafe.order']
        # 2. Browse
        list_orders = Order.browse(ids_to_change)
        # 3. Ubah statenya
        if list_orders:
            order = list_orders[0]
            if self.payment_return <= 0:
                order.state = 'paid'