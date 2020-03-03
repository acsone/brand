# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class ContractContract(models.Model):

    _inherit = "contract.contract"

    @api.onchange("brand_id")
    def onchange_brand_allowed_payment_mode(self):
        self.ensure_one()
        domain = []
        if self.brand_id and self.brand_id.allowed_payment_mode_ids:
            domain = [("id", "in", self.brand_id.allowed_payment_mode_ids.ids)]
        return {"domain": {"payment_mode_id": domain}}

    @api.onchange("partner_id")
    def on_change_partner_id(self):
        res = super(ContractContract, self).on_change_partner_id()
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
