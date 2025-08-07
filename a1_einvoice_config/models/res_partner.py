# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from ...a1_einvoice_config.utils.tools_func import action_validate_tin


class Partner(models.Model):
    _inherit = "res.partner"

    country_id = fields.Many2one("res.country", string="Country")

    sst_registration_number = fields.Char(
        string="SST",
        help="Malaysian Sales and Service Tax Number",
    )
    ttx_registration_number = fields.Char(
        string="TTx",
        help="Malaysian Tourism Tax Number",
    )

    tin_validation_state = fields.Selection(
        selection=[
            ("valid", "Valid"),
            ("invalid", "Invalid"),
        ],
        string="Tin Validation State",
        help="Technical field, hold the result of TIN validation using MyInvois API.\n"
        "It is non blocking, and will simply help ensure that the customer of an invoice is valid to avoid submission errors.",
        compute="_compute_tin_validation_state",
        readonly=False,
        store=True,
        export_string_translation=False,
    )

    identification_type = fields.Selection(
        string="ID Type",
        selection=[
            ("NRIC", "MyKad/MyTentera/MyPR/MyKAS"),
            ("BRN", "Business Registration Number"),
            ("PASSPORT", "Passport"),
            ("ARMY", "Army"),
        ],
        default="BRN",
        help="The identification type and number used by the MyTax/MyInvois system to identify the user.\nNote: For MyPR and MyKAS to use NRIC scheme\n Note For Foreigner: please enter \"NA\" as Id No.",
    )

    identification_number = fields.Char(string="ID Number", required=True)
    identification_number_placeholder = fields.Char(
        compute="_compute_identification_number_placeholder"
    )



    @api.depends("identification_type", "identification_number", "vat")
    def _compute_tin_validation_state(self):
        """The three @depends are used for the validation. If they change, we will invalidate it and expect the user to revalidate."""
        self.tin_validation_state = False

    @api.depends("identification_type")
    def _compute_identification_number_placeholder(self):
        """Computes a dynamic placeholder that depends on the selected type to help the user inputs their data.
        The placeholders have been taken from the MyInvois doc.
        """
        for partner in self:
            placeholder = "N/A"
            if partner.identification_type == "NRIC":
                placeholder = "830503-11-4923"
            elif partner.identification_type == "BRN":
                placeholder = "202201234565"
            elif partner.identification_type == "PASSPORT":
                placeholder = "A00000000"
            elif partner.identification_type == "ARMY":
                placeholder = "830805-13-4983"
            partner.identification_number_placeholder = placeholder

    def _default_a1_einvoice_config_industrial_classification(self):
        return self.env.ref("a1_einvoice_config.class_00000", raise_if_not_found=False)

    a1_einvoice_config_industrial_classification = fields.Many2one(
        comodel_name="a1_einvoice_config.industry_classification",
        string="Ind. Classification",
        default=_default_a1_einvoice_config_industrial_classification,
    )

    def action_validate_tin(self):
        config = self.env["api.myinvoice.config"].search([], limit=1)
        if config:
            config.action_get_access_token()
            result = action_validate_tin(
                vat=self.vat,
                identification_type=self.identification_type,
                identification_number=self.identification_number,
                access_token=config.access_token,
            )
            self.tin_validation_state = result
