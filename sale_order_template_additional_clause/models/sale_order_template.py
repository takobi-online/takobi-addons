from odoo import models, fields


class SaleOrderTemplate(models.Model):
    _inherit = 'sale.order.template'

    additional_clause = fields.Text("Additional clauses", translate=True)
    additional_clause_requires_acceptance = fields.Boolean()
    note_requires_acceptance = fields.Boolean()
