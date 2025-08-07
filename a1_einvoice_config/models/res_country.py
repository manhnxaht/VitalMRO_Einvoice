from odoo import models, fields


class Country(models.Model):
    _inherit = "res.country"


class CountryState(models.Model):
    _inherit = "res.country.state"

    einvois_code = fields.Char("MyInvois state code", size=2)
