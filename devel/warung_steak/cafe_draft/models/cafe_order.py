from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class CafeOrder(models.Model):
    _inherit = 'cafe.order'

    note = fields.Char(string='Note')

    customer = fields.Char(readonly=True, states={'draft': [('readonly', False)]})
    table_number = fields.Integer('Table Number')

    @api.multi
    def set_open(self):
        for doc in self:
            nama_baru = self.env['ir.sequence'].next_by_code('cafe.order.sequence')
            doc.name = nama_baru
            doc.state = 'open'

    @api.one
    def set_open_one(self):
        nama_sequence = self.env['ir.sequence'].next_by_code('cafe.order.sequence')
        self.name = self.customer + '-' + nama_sequence
        self.state = 'open'

    @api.one
    def set_lunas(self):
        self.note = 'lunas'
    
    # Button, on change, fungsi berhubungan dengan tampilan = api.one
    @api.one
    def set_gratis(self):
        for line in self.line_ids:
            line.price = 0
        
    # Computed, fungsi yang dijalankan dibelakang = api.multi
    @api.multi
    @api.depends('line_ids', 'line_ids.quantity', 'line_ids.price')
    def _compute_total(self):
        return super(CafeOrder, self)._compute_total()

    @api.one
    def add_order_line(self):
        # Add / Create
        # 1. Panggil Tablenya
        OrderLine = self.env['cafe.order.line']
        Produk = self.env['cafe.produk']
        # 2. Panggil method create
        list_produk_ayam = Produk.search([('name', 'ilike', 'Ayam')])
        if list_produk_ayam:
            produk_ayam = list_produk_ayam[0]
            OrderLine.create({
                'produk_id': produk_ayam.id,
                'quantity': 99,
                'price': produk_ayam.price,
                'order_id': self.id,
            })

    @api.one
    def delete_order_line(self):
        # 1. Panggil Tablenya
        OrderLine = self.env['cafe.order.line']
        Produk = self.env['cafe.produk']
        # 2. Panggil method create
        list_produk_ayam = Produk.search([('name', 'ilike', 'Ayam')])
        if list_produk_ayam:
            produk_ayam = list_produk_ayam[0]
            list_order_line = OrderLine.search([('order_id', '=', self.id), 
                ('produk_id', '=', produk_ayam.id)])
            for line in list_order_line:
                # set quantity 0
                line.unlink() # hapus