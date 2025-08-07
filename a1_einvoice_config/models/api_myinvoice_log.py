# -*- coding: utf-8 -*-
from odoo import models, fields


class APILog(models.Model):
    _name = "api.myinvoice.log"
    _description = "API Log"

    name = fields.Char("Name")
    status = fields.Selection(
        [
            ("new", "New"),
            ("success", "Success"),
            ("fail", "Fail"),
            ("cancel", "Cancel"),
        ],
        string="Status",
    )
    error_code = fields.Char("Error_code")
    sequence_id = fields.Many2one("api.myinvoice.sequence", string="Sequence")
    api_config_id = fields.Many2one("api.myinvoice.config", string="API")
    e_invoice_id = fields.Many2one("account.move", string="E-Invoice")
    data = fields.Text(string="E-Invoice")

