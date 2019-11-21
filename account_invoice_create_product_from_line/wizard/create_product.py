from odoo import models, fields, api


class CreateProduct(models.TransientModel):
    _name = 'wizard.create.product.from.invoice.line'
    _description = 'Create product from invoice line'

    mode = fields.Selection([
        ('search', "Search existing product"),
        ('create', 'New product'),
    ], "Mode", required=True, default="search")
    name = fields.Char("Name")
    code = fields.Char("Code")
    unit_price = fields.Float("Unit price")
    uom_id = fields.Many2one('uom.uom', 'Unit of Measure')
    product_id = fields.Many2one("product.product", "Selected product")

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
            'uom_po_id': self.uom_id.id,
        })
        inv_line.product_id = product.id
        if not inv_line.uom_id:
            inv_line.uom_id = self.uom_id.id

    @api.multi
    def use_product(self):
        self.ensure_one()
        line_id = self.env.context.get('active_id')
        inv_line = self.env['account.invoice.line'].browse(line_id)
        inv_line.product_id = self.product_id.id
        if not inv_line.uom_id:
            inv_line.uom_id = self.product_id.uom_po_id.id

    @api.model
    def default_get(self, fields):
        vals = super(CreateProduct, self).default_get(fields)
        if not vals.get('uom_id'):
            vals['uom_id'] = self.env['product.template']._get_default_uom_id()
        return vals
