from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError

class CatalogWizard(models.TransientModel):

    _name = 'catalog.wizard'

    catalog_type = fields.Selection(
        selection=[
            ('makanan', 'Makanan'),
            ('minuman', 'Minuman'),
            ],
        string='Catalog Type',
        required=True
        )

    def process_wizard(self):
        # 1. Panggil Table
        Produk = self.env['cafe.produk']
        # 2. Search produk berdasarkan pilihan user
        list_produks = Produk.search([('tipe', '=', self.catalog_type)])
        # 3. Return report action dengan parameter list produk
        return self.env.ref('cafe_print_popup.cafe_produk_print').report_action(list_produks)
