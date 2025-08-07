# -*- coding: utf-8 -*-
from odoo import models, fields


class APISequence(models.Model):
    _name = "api.myinvoice.sequence"
    _description = "API Sequence"
    _rec_name = "sequence"

    api_config_id = fields.Many2one("api.myinvoice.config", string="API Config")
    sequence = fields.Integer("Sequence")
    time = fields.Float("Time")
