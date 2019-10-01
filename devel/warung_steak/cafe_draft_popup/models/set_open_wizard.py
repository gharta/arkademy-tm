from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError

class SetOpenWizard(models.TransientModel):

    _name = 'set.open.wizard'
    state = fields.Selection([
        ('draft', 'Draft'),
        ('open', 'Open'),
    ], string='Status', default='draft', required=True,)
    pegawai_id = fields.Many2one('cafe.pegawai', string='Pelayan')
    notes = fields.Text('Notes', default='Catatan Tambahan...')

    @api.model
    def default_get(self, default_fields):
        res = super(SetOpenWizard, self).default_get(default_fields)
        res['notes'] = 'Catatan Tambahan dari Default Get'
        return res

    def process_wizard(self):
        # Cara untuk mendapatkan id yang dipilih
        ids_to_change = self._context.get('active_ids')
        # Panggil Tablenya
        Order = self.env['cafe.order']
        # Browse rows nya
        list_orders = Order.browse(ids_to_change)
        # Set status sesuai yang diinput
        for order in list_orders:
            order.state = self.state
            order.pegawai_id = self.pegawai_id.id
