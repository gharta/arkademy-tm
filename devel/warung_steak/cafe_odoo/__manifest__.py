{
  'name': 'Modul Cafe yang menginherit proses bisnis Odoo',
  'author': 'Arkana',
  'version': '0.1',
  'depends': [
    'cafe', 'stock', 'account'
  ],
  'data': [
    'views/cafe_order.xml',
  ],
  'qweb': [
    # 'static/src/xml/nama_widget.xml',
  ],
  'sequence': 1,
  'auto_install': False,
  'installable': True,
  'application': True,
  'category': '- Arkademy Part 1',
  'summary': 'Catat Penjualan Sederhana',
  'license': 'OPL-1',
  'website': 'https://www.arkana.co.id/',
  'description': '-'
}