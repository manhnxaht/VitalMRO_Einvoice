# -*- coding: utf-8 -*-
{
    "name": "A1 E-Invoice Config",
    "summary": "A1 E-Invoice",
    "description": """
        A1 E-Invoice Config
    """,
    "author": "A1",
    "category": "Accounting",
    "version": "13.0",
    # any module necessary for this one to work correctly
    "depends": ["base", "sale_management"],
    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "data/a1_einvoice_config.industry_classification.csv",
        "views/api_myinvoice_config_view.xml",
        "views/api_myinvoice_log_view.xml",
        "views/res_partner_view.xml",
        "views/res_company_view.xml",
        "views/res_country_state_view.xml",
        "views/a1_e_invoice_industrial_classification_views.xml",
        "views/product_template_view.xml",
        "views/account_tax_view.xml",
        "views/menu_view.xml",
    ],
    # only loaded in demonstration mode
    "license": "LGPL-3",
    "installable": True,
    "application": True,
}
