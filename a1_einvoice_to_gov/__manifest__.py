# -*- coding: utf-8 -*-
{
    "name": "A1 E-Invoice To GOV",
    "summary": "A1 E-Invoice To GOV",
    "description": """
        A1 E-Invoice To GOV
    """,
    "author": "A1",
    "category": "Accounting",
    "version": "13.0",
    "depends": ["base", "account_debit_note", "sale_management", "sale_stock", "point_of_sale", 'purchase',
                "a1_einvoice_config", "account"],
    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "data/einvoice_data.xml",
        "data/mail_template_data.xml",
        "data/res_country_state.xml",
        "data/default_customer.xml",
        # "wizard/create_consolidate_invoice.xml",
        # "views/account_move.xml",
        # "views/sale_views.xml",
        # "wizard/write_cancel_einvoice_reason_view.xml",
        # "wizard/adjustment_bill.xml",
        # "wizard/adjustment_invoice.xml",
        # "views/bill_credit_note.xml",
        # "views/bill_debit_note.xml",
        # "views/bill_refund_note.xml",
        # "views/invoice_credit_note.xml",
        # "views/invoice_debit_note.xml",
        # "views/invoice_refund_note.xml",
    ],
    # only loaded in demonstration mode
    "license": "LGPL-3",
    "installable": True,
    "application": True,
}
