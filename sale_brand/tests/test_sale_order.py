# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestSaleOrder(TransactionCase):
    def setUp(self):
        super(TestSaleOrder, self).setUp()
        self.sale = self.env.ref('sale.sale_order_1')
        self.sale.brand_id = self.env['res.brand'].create({'name': 'brand'})
        self.sale.order_line.mapped('product_id').write(
            {'invoice_policy': 'order'}
        )
        self.sale.action_confirm()
        self.account_receivable_type = self.env.ref(
            'account.data_account_type_receivable'
        )
        self.account_receivable_brand_default = self.env[
            'account.account'
        ].create(
            {
                'name': 'Receivable Brand Default',
                'code': 'RCV01',
                'user_type_id': self.account_receivable_type.id,
                'reconcile': True,
            }
        )
        self.partner_account_brand = self.env['res.partner.account.brand'].create(
            {
                'partner_id': self.sale.partner_id.id,
                'account_id': self.account_receivable_brand_default.id,
                'brand_id': self.sale.brand_id.id,
                'account_type': 'receivable',
            }
        )

    def test_create_invoice(self):
        """It should create branded invoice"""
        self.assertEqual(self.sale.invoice_status, 'to invoice')
        invoice_ids = self.sale.action_invoice_create()
        invoice = self.env['account.invoice'].browse(invoice_ids[0])
        self.assertEqual(invoice.brand_id, self.sale.brand_id)
        self.assertEqual(invoice.account_id, self.account_receivable_brand_default)

    def test_create_down_payment_invoice(self):
        """It should create branded down-payment invoice"""
        advance_payment_wizard = self.env['sale.advance.payment.inv'].create(
            {'advance_payment_method': 'fixed', 'amount': 10.0}
        )
        advance_payment_wizard.with_context(
            active_ids=self.sale.ids
        ).create_invoices()
        invoice = self.sale.order_line.mapped('invoice_lines').mapped(
            'invoice_id'
        )
        self.assertEqual(invoice.brand_id, self.sale.brand_id)
