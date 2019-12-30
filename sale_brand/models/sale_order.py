# Copyright (C) 2019 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class SaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = ['sale.order', 'res.brand.mixin']

    @api.multi
    def _prepare_invoice(self):
        for order in self:
            invoice_vals = super(SaleOrder, order)._prepare_invoice()
            invoice_vals.update({
                'brand_id': order.brand_id.id,
            })
        return invoice_vals

    @api.onchange('brand_id')
    def _onchange_brand_id(self):
        res = super()._onchange_brand_id()
        for order in self:
            if order.state == 'draft' and order.brand_id:
                order.analytic_account_id = order.brand_id.analytic_account_id
        return res
