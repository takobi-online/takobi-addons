
from odoo.exceptions import UserError
from odoo import models, fields, api, _


class Invoice(models.Model):
    _inherit = 'account.invoice'

    @api.model
    def _default_picking_receive(self):
        type_obj = self.env['stock.picking.type']
        company_id = self.env.context.get('company_id') or self.env.user.company_id.id
        types = type_obj.search([('code', '=', 'incoming'), ('warehouse_id.company_id', '=', company_id)], limit=1)
        if not types:
            types = type_obj.search([('code', '=', 'incoming'), ('warehouse_id', '=', False)])
        return types[:1]

    invoice_picking_id = fields.Many2one(
        'stock.picking', string="Incoming shipment", copy=False,
        help="Picking created directly from invoice")
    picking_type_id = fields.Many2one('stock.picking.type', 'Picking Type', required=True,
                                      default=_default_picking_receive,
                                      help="This will determine picking type of incoming shipment")
    has_products = fields.Boolean("Has products", compute="_compute_has_products")

    @api.multi
    def _compute_has_products(self):
        for inv in self:
            if inv.mapped('invoice_line_ids.product_id'):
                inv.has_products = True
            else:
                inv.has_products = False

    @api.multi
    def action_stock_receive(self):
        for inv in self:
            if not inv.mapped('invoice_line_ids.product_id'):
                raise UserError(_('Please create some invoice lines with product.'))
            if not inv.number:
                raise UserError(_('Please Validate invoice.'))
            if not inv.invoice_picking_id:
                pick = {
                    'picking_type_id': inv.picking_type_id.id,
                    'partner_id': inv.partner_id.id,
                    'origin': inv.number,
                    'location_dest_id': inv.picking_type_id.default_location_dest_id.id,
                    'location_id': inv.partner_id.property_stock_supplier.id
                }
                picking = self.env['stock.picking'].create(pick)
                inv.invoice_picking_id = picking.id
                moves = inv.invoice_line_ids.filtered(lambda r: r.product_id.type in ['product', 'consu'])._create_stock_moves(picking)
                moves = moves.filtered(lambda x: x.state not in ('done', 'cancel'))._action_confirm()
                seq = 0
                for move in sorted(moves, key=lambda move: move.date_expected):
                    seq += 5
                    move.sequence = seq
                moves._action_assign()
                picking.message_post_with_view('mail.message_origin_link',
                    values={'self': picking, 'origin': inv},
                    subtype_id=self.env.ref('mail.mt_note').id)

    @api.multi
    def action_view_picking(self):
        self.ensure_one()
        action = self.env.ref('stock.action_picking_tree_ready')
        result = action.read()[0]
        res = self.env.ref('stock.view_picking_form', False)
        result['views'] = [(res and res.id or False, 'form')]
        result['res_id'] = self.invoice_picking_id.id or False
        return result


class SupplierInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    @api.multi
    def _create_stock_moves(self, picking):
        moves = self.env['stock.move']
        done = self.env['stock.move'].browse()
        for line in self:
            price_unit = line.price_unit
            vals = {
                'name': line.name or '',
                'product_id': line.product_id.id,
                'product_uom': line.uom_id.id,
                'product_uom_qty': line.quantity,
                'location_id': line.invoice_id.partner_id.property_stock_supplier.id,
                'location_dest_id': picking.picking_type_id.default_location_dest_id.id,
                'picking_id': picking.id,
                'price_unit': price_unit,
                'picking_type_id': picking.picking_type_id.id,
                'warehouse_id': picking.picking_type_id.warehouse_id.id,
            }
            done += moves.create(vals)
        return done
