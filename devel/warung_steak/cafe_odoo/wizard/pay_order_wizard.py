from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime

class PayOrderWizard(models.TransientModel):
    _inherit = 'pay.order.wizard'

    def process_wizard(self):
        super(PayOrderWizard, self).process_wizard()

        ids_to_change = self._context.get('active_ids')
        Order = self.env['cafe.order']
        list_orders = Order.browse(ids_to_change)
        if list_orders:
            order = list_orders[0]
            # Loop line nya
            for line in order.line_ids:
                # Pembuatan Stock Move
                # 1. Panggil Table
                StockMove = self.env['stock.move']
                StockLocation = self.env['stock.location']
                # 2. Search Location ID, Location DEST ID
                internal_location = StockLocation.search([('usage', '=', 'internal')], limit=1)
                customer_location = StockLocation.search([('usage', '=', 'customer')], limit=1)
                # 3. Create
                move = StockMove.create({
                    'location_id': internal_location.id,
                    'location_dest_id': customer_location.id,
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.quantity,
                    'quantity_done': line.quantity,
                    'origin': order.name,
                    'product_uom': self.env.ref('uom.product_uom_unit').id,
                    'name': order.name,
                })
                move._action_done()
                # Journal Cash
                journal_cash = self.env['account.journal'].search([('type', '=', 'cash')], limit=1)

                # Pembuatan Jurnal Pembayaran
                line_vals = []

                # Barang Keluar Belum Diinvoice
                account_barang_keluar = line.product_id.categ_id.property_stock_account_output_categ_id
                line_vals += [(0, 0, {
                    'name': 'Barang Keluar Belum Diinvoice',
                    'account_id': account_barang_keluar.id,
                    'credit': line.quantity * line.product_id.standard_price,
                    'debit': 0,
                })]
                # HPP
                account_hpp = line.product_id.categ_id.property_account_expense_categ_id
                line_vals += [(0, 0, {
                    'name': 'HPP',
                    'account_id': account_hpp.id,
                    'debit': line.quantity * line.product_id.standard_price,
                    'credit': 0,
                })]
                # Penjualan
                account_penjualan = line.product_id.categ_id.property_account_income_categ_id
                line_vals += [(0, 0, {
                    'name': 'Penjualan',
                    'account_id': account_penjualan.id,
                    'credit': line.quantity * line.price,
                    'debit': 0,
                })]
                # Bank / Cash
                account_bank = journal_cash.default_debit_account_id
                line_vals += [(0, 0, {
                    'name': 'Pembayaran',
                    'account_id': account_bank.id,
                    'debit': line.quantity * line.price,
                    'credit': 0,
                })]

                # Account Move
                vals = {
                    'journal_id': journal_cash.id,
                    'date': datetime.strftime(datetime.today(), "%Y-%m-%d"),
                    'company_id': self.env.user.company_id.id,
                    'ref': order.name,
                    'line_ids': line_vals
                }
                move = self.env['account.move'].create(vals)
                move.action_post()

        return True