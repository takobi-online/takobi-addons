from odoo import models, fields, api


class CreateProduct(models.TransientModel):
    _name = 'wizard.create.product.from.invoice.line'
    _description = 'Create product from invoice line'

    name = fields.Char("Name", required=True)
    code = fields.Char("Code")
    unit_price = fields.Float("Unit price")
    uom_id = fields.Many2one('uom.uom', 'Unit of Measure', required=True)

    @api.multi
    def create_product(self):
        self.ensure_one()
        line_id = self.env.context.get('active_id')
        inv_line = self.env['account.invoice.line'].browse(line_id)
        product = self.env['product.product'].create({
            'name': self.name,
            'default_code': self.code,
            'standard_price': self.unit_price,
            'uom_id': self.uom_id.id,
        })
        inv_line.product_id = product.id
        if not inv_line.uom_id:
            inv_line.uom_id = self.uom_id.id

    @api.model
    def default_get(self, fields):
        vals = super(CreateProduct, self).default_get(fields)
        if not vals.get('uom_id'):
            vals['uom_id'] = self.env['product.template']._get_default_uom_id()
        return vals
