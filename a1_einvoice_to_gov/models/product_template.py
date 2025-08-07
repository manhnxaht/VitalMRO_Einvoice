
from odoo import fields, models


class ProductTemplate(models.Model):
    """
    add this required field so user can cahnge te
    """
    _inherit = "product.template"

    manual_classification_code = fields.Char(string="Customer Defined Malaysian classification code")
