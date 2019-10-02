from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError

class KaryawanWizard(models.TransientModel):

    _name = 'karyawan.wizard'

    gender = fields.Selection([
        ('l', 'Laki-laki'),
        ('p', 'Perempuan'),
    ], string='Gender')

    def process_wizard(self):
        # 1. Panggil Table
        Pegawai = self.env['cafe.pegawai']
        # 2. Search produk berdasarkan pilihan user
        list_pegawais = Pegawai.search([('gender', '=', self.gender)])
        # 3. Return report action dengan parameter list produk
        return self.env.ref('cafe_print_popup.cafe_karyawan_print').report_action(list_pegawais)
