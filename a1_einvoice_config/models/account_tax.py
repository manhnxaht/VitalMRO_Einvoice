# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class AccountTax(models.Model):
    _inherit = 'account.tax'

    # ------------------
    # Fields declaration
    # ------------------

    x_my_tax_type = fields.Selection(
        selection=[
            ('01', "Sales Tax"),
            ('02', "Service Tax"),
            ('03', "Tourism Tax"),
            ('04', "High-Value Goods Tax"),
            ('05', "Sales Tax on Low Value Goods"),
            ('06', "Not Applicable"),
            ('E', "Tax exemption (where applicable)"),
        ],
        string="Malaysian Tax Type",
        compute="_compute_my_tax_type",
        store=True,
        readonly=False,
    )

    # --------------------------------
    # Compute, inverse, search methods
    # --------------------------------

    @api.depends('amount', 'country_id', 'type_tax_use')
    def _compute_my_tax_type(self):
        """ Compute default tax type based on a few factors. """
        for tax in self:
            if tax.country_id.code != 'MY':
                tax.x_my_tax_type = False
            else:
                if tax.amount == 0:
                    tax.x_my_tax_type = 'E'
                elif tax.type_tax_use in ['sale', 'purchase']:
                    tax.x_my_tax_type = '01'
                else:
                    tax.x_my_tax_type = '06'
