# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ResBrandMixin(models.AbstractModel):

    _inherit = "res.brand.mixin"

    allowed_payment_mode_ids = fields.Many2many(
        related="brand_id.allowed_payment_mode_ids"
    )
