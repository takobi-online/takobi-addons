# Copyright 2019 Lorenzo Battistini @ TAKOBI
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
{
    "name": "Create product from invoice line",
    "description": "This module allows to create a new product from an invoice "
                   "line, allowing user to set product data, without "
                   "overwriting data already present in invoice line",
    "version": "12.0.1.0.0",
    "category": "Invoices & Payments",
    "website": "https://takobi.online",
    "author": "TAKOBI",
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "account",
        "stock",
    ],
    "data": [
        "wizard/create_product_view.xml",
        "views/account_invoice_view.xml",
    ],
    "demo": [
    ],
}
