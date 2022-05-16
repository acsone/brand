# Copyright 2022 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProjectTask(models.Model):

    _inherit = "project.task"

    brand_id = fields.Many2one(comodel_name="res.brand", string="Brand")
