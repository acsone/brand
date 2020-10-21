# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductPricelist(models.Model):

    _inherit = "product.pricelist"

    def _compute_price_rule_get_items(
        self, products_qty_partner, date, uom_id, prod_tmpl_ids, prod_ids, categ_ids
    ):
        self.ensure_one()
        items = super(ProductPricelist, self)._compute_price_rule_get_items(
            products_qty_partner, date, uom_id, prod_tmpl_ids, prod_ids, categ_ids
        )
        # super returns all items applied on (any) brand
        # We want only items applied on 'prod_ids' brands
        products = self.env["product.product"].browse(prod_ids)
        brand_ids = products.mapped("product_brand_id").ids
        items -= self.env["product.pricelist.item"].search(
            [("id", "in", items.ids), ("product_brand_id", "not in", brand_ids)]
        )
        return items


class ProductPricelistItem(models.Model):

    _inherit = "product.pricelist.item"

    product_brand_id = fields.Many2one(
        comodel_name="product.brand",
        string="Brand",
        ondelete="cascade",
        help="Specify a brand if this rule only applies to products"
        "belonging to this brand. Keep empty otherwise.",
    )
    applied_on = fields.Selection(selection_add=[("4_brand", "Brand")])

    @api.constrains("product_id", "product_tmpl_id", "categ_id", "product_brand_id")
    def _check_product_consistency(self):
        super(ProductPricelistItem, self)._check_product_consistency()
        for item in self:
            if item.applied_on == "4_brand" and not item.product_brand_id:
                raise ValidationError(
                    _("Please specify the brand for which this rule should be applied")
                )

    @api.depends(
        "applied_on",
        "categ_id",
        "product_tmpl_id",
        "product_id",
        "compute_price",
        "fixed_price",
        "pricelist_id",
        "percent_price",
        "price_discount",
        "price_surcharge",
        "product_brand_id",
    )
    def _get_pricelist_item_name_price(self):
        super(ProductPricelistItem, self)._get_pricelist_item_name_price()
        for item in self:
            if item.product_brand_id and item.applied_on == "4_brand":
                item.name = _("Brand: %s") % (item.product_brand_id.display_name)

    @api.onchange("product_id", "product_tmpl_id", "categ_id", "product_brand_id")
    def _onchane_rule_content(self):
        super(ProductPricelistItem, self)._onchane_rule_content()

    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:
            if values.get("applied_on", False):
                # Ensure item consistency for later searches.
                applied_on = values["applied_on"]
                if applied_on == "4_brand":
                    values.update(
                        dict(product_id=None, product_tmpl_id=None, categ_id=None)
                    )
                elif applied_on == "3_global":
                    values.update(dict(product_brand_id=None))
                elif applied_on == "2_product_category":
                    values.update(dict(product_brand_id=None))
                elif applied_on == "1_product":
                    values.update(dict(product_brand_id=None))
                elif applied_on == "0_product_variant":
                    values.update(dict(product_brand_id=None))
        return super(ProductPricelistItem, self).create(vals_list)

    def write(self, values):
        if values.get("applied_on", False):
            # Ensure item consistency for later searches.
            applied_on = values["applied_on"]
            if applied_on == "4_brand":
                values.update(
                    dict(product_id=None, product_tmpl_id=None, categ_id=None)
                )
            elif applied_on == "3_global":
                values.update(dict(product_brand_id=None))
            elif applied_on == "2_product_category":
                values.update(dict(product_brand_id=None))
            elif applied_on == "1_product":
                values.update(dict(product_brand_id=None))
            elif applied_on == "0_product_variant":
                values.update(dict(product_brand_id=None))
        return super(ProductPricelistItem, self).write(values)
