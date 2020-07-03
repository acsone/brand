# Copyright (C) 2019 Open Source Integrators
# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from collections import OrderedDict

from odoo import api, fields, models


class AccountInvoice(models.Model):
    _name = 'account.invoice'
    _inherit = ['account.invoice', 'res.brand.mixin']

    brand_id = fields.Many2one(
        states={
            'open': [('readonly', True)],
            'in_payment': [('readonly', True)],
            'paid': [('readonly', True)],
            'cancel': [('readonly', True)],
        }
    )

    def _get_onchange_create(self):
        res = super()._get_onchange_create()
        return OrderedDict(
            [("_onchange_partner_brand", ["account_id"])] + list(res.items())
        )

    @api.onchange("partner_id", "company_id", "brand_id")
    def _onchange_partner_brand(self):
        if self.brand_id:
            pab_model = self.env["res.partner.account.brand"]
            company_id = self.company_id.id
            partner = (
                self.partner_id
                if not company_id
                else self.partner_id.with_context(force_company=company_id)
            )
            invoice_type = self.type or self.env.context.get(
                "type", "out_invoice"
            )
            if partner:
                rec_account = pab_model._get_partner_account_by_brand(
                    "receivable", self.brand_id, partner
                )
                rec_account = (
                    rec_account
                    if rec_account
                    else partner.property_account_receivable_id
                )
                pay_account = pab_model._get_partner_account_by_brand(
                    "payable", self.brand_id, partner
                )
                pay_account = (
                    pay_account
                    if pay_account
                    else partner.property_account_payable_id
                )
                if invoice_type in ("in_invoice", "in_refund"):
                    account_id = pay_account
                else:
                    account_id = rec_account
                self.account_id = account_id
