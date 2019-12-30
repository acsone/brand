# Copyright (C) 2019 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class AccountInvoice(models.Model):
    _name = 'account.invoice'
    _inherit = ['account.invoice', 'res.brand.mixin']

    @api.onchange('brand_id', 'invoice_line_ids')
    def _onchange_brand_id(self):
        res = super()._onchange_brand_id()
        for invoice in self:
            if invoice.state == 'draft' and invoice.brand_id:
                account_analytic = invoice.brand_id.analytic_account_id
                invoice.invoice_line_ids.update(
                    {'account_analytic_id': account_analytic.id}
                )
        return res
