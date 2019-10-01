from odoo import models, fields

class CafePegawai(models.Model):
    _name = 'cafe.pegawai'

    name = fields.Char(string='Nama Karyawan', required=True)
    alamat = fields.Text(string='Alamat')
    tahun_masuk = fields.Integer(string='Tahun Masuk')
    indeks_prestasi = fields.Float(string='Indeks Prestasi')
    
    tanggal_lahir = fields.Date(string='Tanggal Lahir')
    waktu_bangun = fields.Datetime(string='Waktu Bangun Tidur')
    gender = fields.Selection([
        ('l', 'Laki-laki'),
        ('p', 'Perempuan'),
    ], string='Gender')
    
    is_part_time = fields.Boolean(string='Part Time')

    image = fields.Binary('Image')

    def action_order_line(self):
        # Model / Class / Table
        OrderLine = self.env['cafe.order.line']
        SaleOrder = self.env['sale.order']
        PurchaseOrder = self.env['purchase.order']

        # Create / Add Record
        # ORM create : create({})
        orders = self.env['cafe.order'].search([])
        makanans = self.env['cafe.produk'].search([('tipe', '=', 'makanan')])
        if orders and makanans:
            first_order = orders[0]
            makanan = makanans[0]
            
            OrderLine.create({
                'quantity': 100,
                'price': 100,
                'order_id': first_order.id,
                'produk_id': makanan.id,
            })

        # Data / Record / Row
        # ORM get data : browse() / search([ ( , , ) ])
        lines = OrderLine.search([])

        for line in lines:
            # Field
            # ORM modifikasi : langsung .field, .write({}), .unlink()
            line.quantity = line.quantity + 1
            line.price = 100

            # line.write({
            #     'quantity': line.quantity + 1,
            #     'price': 100,
            # })

            # Method
