# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.account_payment_mode_brand.tests import (
    test_account_payment_mode_brand
)


class TestAccountPaymentModeBrand(
    test_account_payment_mode_brand.TestBasePaymentModeBrand
):
    def setUp(self):
        super(TestAccountPaymentModeBrand, self).setUp()
        self.sale = self.env["sale.order"].create(
            {"partner_id": self.partner.id, "brand_id": self.brand.id}
        )

    def test_sale_order_onchange_brand(self):
        self.assertEqual(
            self.sale.onchange_brand_allowed_payment_mode()["domain"][
                "payment_mode_id"
            ],
            [("id", "in", self.payment_mode_1.ids)],
        )
        self.brand.allowed_payment_mode_ids = False
        self.assertEqual(
            self.sale.onchange_brand_allowed_payment_mode()["domain"][
                "payment_mode_id"
            ],
            [],
        )
        self.sale.brand_id = False
        self.assertEqual(
            self.sale.onchange_brand_allowed_payment_mode()["domain"][
                "payment_mode_id"
            ],
            [],
        )

    def test_sale_order_onchange_partner(self):
        self.sale.onchange_partner_id()
        self.assertEqual(self.sale.payment_mode_id, self.payment_mode_1)
        self.brand.allowed_payment_mode_ids = self.payment_mode_2
        self.sale.onchange_partner_id()
        self.assertFalse(self.sale.payment_mode_id)
        self.brand.allowed_payment_mode_ids = False
        self.sale.onchange_partner_id()
        self.assertEqual(self.sale.payment_mode_id, self.payment_mode_1)
