# -*- coding: utf-8 -*-
from odoo import models, fields, _
from odoo.exceptions import UserError, ValidationError
from ..services.handle_api import get_access_token
from ..utils.const_params import api_url, env_base_url, scope, grant_type


class APIConfig(models.Model):
    _name = "api.myinvoice.config"
    _inherit = ["mail.thread", "mail.activity.mixin", "portal.mixin"]
    _description = "API Config"

    name = fields.Char("Name")
    client_id = fields.Char("Client ID")
    client_secret = fields.Char("Client Secret")
    is_active = fields.Boolean("Activate", default=True)
    access_token = fields.Text("Access Token")
    sequence_ids = fields.One2many("api.myinvoice.sequence", "api_config_id", string="Resubmit")
    recall_times = fields.Integer("Recall Times", default=3)
    during_times = fields.Integer("During Times", default=0)
    company_id = fields.Many2one('res.company', string="Company")

    def action_get_access_token(self):
        access_token = get_access_token(api_url, client_id=self.client_id, scope=scope,
                                        client_secret=self.client_secret, grant_type=grant_type)
        if access_token:
            self.access_token = access_token
        else:
            raise ValidationError("Error occurs when get access token !")


