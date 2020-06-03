# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class AccountInvoice(models.Model):

    _name = "account.invoice"
    _inherit = ["account.invoice", "res.brand.allowed.payment.mode.mixin"]
