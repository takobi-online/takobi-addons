from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    additional_clause = fields.Text("Additional clauses", translate=True)
    additional_clause_requires_acceptance = fields.Boolean()
    note_requires_acceptance = fields.Boolean()
    note_accepted = fields.Boolean(readonly=True, copy=False)
    additional_clause_accepted = fields.Boolean(readonly=True, copy=False)

    @api.onchange('sale_order_template_id')
    def onchange_sale_order_template_id(self):
        res = super(SaleOrder, self).onchange_sale_order_template_id()
        if self.sale_order_template_id:
            template = self.sale_order_template_id.with_context(
                lang=self.partner_id.lang)
            if template.additional_clause:
                self.additional_clause = template.additional_clause
            self.additional_clause_requires_acceptance = template.additional_clause_requires_acceptance
            self.note_requires_acceptance = template.note_requires_acceptance
        return res

    def requires_acceptance(self):
        return (
            (self.note_requires_acceptance and not self.note_accepted) or
            (self.additional_clause_requires_acceptance and not self.additional_clause_accepted)
        )
