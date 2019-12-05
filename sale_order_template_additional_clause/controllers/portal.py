from odoo.addons.sale.controllers.portal import CustomerPortal
from odoo import http


class CustomerPortal(CustomerPortal):

    @http.route()
    def portal_quote_accept(
        self, res_id, access_token=None, partner_name=None, signature=None,
        order_id=None
    ):
        res = super(CustomerPortal, self).portal_quote_accept(
            res_id, access_token, partner_name, signature, order_id)
        if 'error' not in res:
            order_sudo = self._document_check_access(
                'sale.order', res_id, access_token=access_token)
            if order_sudo.note_requires_acceptance:
                order_sudo.note_accepted = True
            if order_sudo.additional_clause_requires_acceptance:
                order_sudo.additional_clause_accepted = True
        return res
