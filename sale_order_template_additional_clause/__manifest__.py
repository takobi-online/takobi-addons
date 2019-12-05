# Copyright 2019 Lorenzo Battistini @ TAKOBI
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
{
    "name": "Sale order template additional clause",
    "description": "This module allows to write additional clauses in sale order template. "
                   "Also, it is possibile to specify whether clauses require acceptance in online quotation or not",
    "version": "12.0.1.0.0",
    "category": "Sales",
    "website": "https://takobi.online",
    "author": "TAKOBI",
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "sale_management",
    ],
    "data": [
        "views/sale_order_template_views.xml",
        "views/sale_order_views.xml",
        "views/sale_portal_templates.xml",
        "views/assets.xml",
        "report/sale_report_templates.xml",
    ],
    "demo": [
    ],
}
