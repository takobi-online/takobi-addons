#    Copyright (C) 2019 Cybrosys Technologies(<https://www.cybrosys.com>).
#    Copyright 2019 Lorenzo Battistini @ TAKOBI

{
    'name': "Stock Picking From Invoice",
    'version': '12.0.1.0.0',
    'summary': """Create Stock Picking From Supplier Invoice""",
    'description': """This Module Allows To Create Stocks Picking From Supplier Invoice""",
    'author': "TAKOBI, Cybrosys Techno Solutions",
    'website': "https://takobi.online",
    'category': 'Accounting',
    # Note: in case stock_picking_invoice_link was installed, a bridge module would probably be needed
    'depends': ['base', 'account', 'stock'],
    'data': ['views/invoice_stock_move_view.xml'],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': True,
    'application': False,
}
