# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class AccountInvoice(models.Model):

    _name = "account.invoice"
    _inherit = ["account.invoice", "res.brand.allowed.payment.mode.mixin"]

    @api.onchange("partner_id", "company_id")
    def _onchange_partner_id(self):
        res = super(AccountInvoice, self)._onchange_partner_id()
        if (
            self.partner_id
            and self.brand_id
            and self.brand_id.allowed_payment_mode_ids
        ):
            if (
                self.payment_mode_id
                not in self.brand_id.allowed_payment_mode_ids
            ):
                self.payment_mode_id = False
        return res
