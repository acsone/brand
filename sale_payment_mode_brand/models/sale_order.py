# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class SaleOrder(models.Model):

    _name = "sale.order"
    _inherit = ["sale.order", "res.brand.allowed.payment.mode.mixin"]
