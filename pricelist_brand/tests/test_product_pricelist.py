# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase
from odoo.tools import float_compare


class TestProductPricelist(TransactionCase):
    def setUp(self):
        super(TestProductPricelist, self).setUp()
        self.product_brand_obj = self.env["product.brand"]
        self.product_brand = self.env["product.brand"].create(
            {"name": "Test Brand", "description": "Test brand description"}
        )
        self.product = self.env.ref("product.product_product_4")
        self.product.write({"product_brand_id": self.product_brand.id})
        self.product_2 = self.env.ref("product.product_product_5")

        self.list0 = self.ref("product.list0")
        self.pricelist = self.env["product.pricelist"].create(
            {
                "name": "Test Pricelist",
                "item_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "Default pricelist",
                            "compute_price": "formula",
                            "base": "pricelist",
                            "base_pricelist_id": self.list0,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "name": "10% Discount on Test Brand",
                            "applied_on": "4_brand",
                            "product_brand_id": self.product_brand.id,
                            "compute_price": "formula",
                            "base": "list_price",
                            "price_discount": 10,
                        },
                    ),
                ],
            }
        )

    def test_calculation_price_of_products_pricelist(self):
        """Test calculation of product price based on pricelist"""
        context = {}
        context.update({"pricelist": self.pricelist.id, "quantity": 1})

        # Check sale price of branded product
        product_with_context = self.product.with_context(context)
        self.assertEqual(
            float_compare(
                product_with_context.price,
                (
                    product_with_context.lst_price
                    - product_with_context.lst_price * (0.10)
                ),
                precision_digits=2,
            ),
            0,
        )

        # Check sale price of not branded product (should not change)
        product_2_with_context = self.product_2.with_context(context)
        self.assertEqual(
            float_compare(
                product_2_with_context.price,
                product_2_with_context.lst_price,
                precision_digits=2,
            ),
            0,
        )
