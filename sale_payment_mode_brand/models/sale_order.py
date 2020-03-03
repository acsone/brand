# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class SaleOrder(models.Model):

    _name = "sale.order"
    _inherit = ["sale.order", "res.brand.allowed.payment.mode.mixin"]

    @api.onchange("partner_id")
    def onchange_partner_id(self):
        res = super(SaleOrder, self).onchange_partner_id()
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
