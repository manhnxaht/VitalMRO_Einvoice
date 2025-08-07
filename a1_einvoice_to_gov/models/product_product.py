
from odoo import fields, models


class ProductProduct(models.Model):
    """
    These codes are required by the API. They represent the product classifications that are used in Malaysia.
    As defined in the list of codes allowed here: https://sdk.myinvois.hasil.gov.my/codes/classification-codes/
    """
    _inherit = "product.product"

    manual_classification_code = fields.Char(string="Customer Defined Malaysian classification code")
