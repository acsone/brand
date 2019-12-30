# Copyright (C) 2019 Open Source Integrators
# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class AccountInvoice(models.Model):
    _name = 'account.invoice'
    _inherit = ['account.invoice', 'res.brand.mixin']

    @api.onchange("partner_id", "company_id", "brand_id")
    def _onchange_partner_id(self):
        res = super()._onchange_partner_id()
        if not self.brand_id:
            return res
        partner_account_brand_model = self.env["res.partner.account.brand"]
        company_id = self.company_id.id
        partner = (
            self.partner_id
            if not company_id
            else self.partner_id.with_context(force_company=company_id)
        )
        invoice_type = self.type or self.env.context.get("type", "out_invoice")
        if partner:
            rec_account = (
                partner_account_brand_model._get_partner_account_by_brand(
                    "receivable", self.brand_id, partner
                )
            )
            rec_account = (
                rec_account.account_id
                if rec_account
                else partner.property_account_receivable_id
            )
            pay_account = (
                partner_account_brand_model._get_partner_account_by_brand(
                    "payable", self.brand_id, partner
                )
            )
            pay_account = (
                pay_account.account_id
                if pay_account
                else partner.property_account_payable_id
            )
            if invoice_type in ("in_invoice", "in_refund"):
                account_id = pay_account
            else:
                account_id = rec_account
            self.account_id = account_id
        return res

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
