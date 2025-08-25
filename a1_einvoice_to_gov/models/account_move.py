# -*- coding: utf-8 -*-
import base64
import json
import time
from datetime import datetime, timedelta
from hashlib import sha256

import requests

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from ...a1_einvoice_config.utils.const_params import api_url, share_url

COUNTRY_CODE_MAP = {
    "BD": "BGD",
    "BE": "BEL",
    "BF": "BFA",
    "BG": "BGR",
    "BA": "BIH",
    "BB": "BRB",
    "WF": "WLF",
    "BL": "BLM",
    "BM": "BMU",
    "BN": "BRN",
    "BO": "BOL",
    "BH": "BHR",
    "BI": "BDI",
    "BJ": "BEN",
    "BT": "BTN",
    "JM": "JAM",
    "BV": "BVT",
    "BW": "BWA",
    "WS": "WSM",
    "BQ": "BES",
    "BR": "BRA",
    "BS": "BHS",
    "JE": "JEY",
    "BY": "BLR",
    "BZ": "BLZ",
    "RU": "RUS",
    "RW": "RWA",
    "RS": "SRB",
    "TL": "TLS",
    "RE": "REU",
    "TM": "TKM",
    "TJ": "TJK",
    "RO": "ROU",
    "TK": "TKL",
    "GW": "GNB",
    "GU": "GUM",
    "GT": "GTM",
    "GS": "SGS",
    "GR": "GRC",
    "GQ": "GNQ",
    "GP": "GLP",
    "JP": "JPN",
    "GY": "GUY",
    "GG": "GGY",
    "GF": "GUF",
    "GE": "GEO",
    "GD": "GRD",
    "GB": "GBR",
    "GA": "GAB",
    "SV": "SLV",
    "GN": "GIN",
    "GM": "GMB",
    "GL": "GRL",
    "GI": "GIB",
    "GH": "GHA",
    "OM": "OMN",
    "TN": "TUN",
    "JO": "JOR",
    "HR": "HRV",
    "HT": "HTI",
    "HU": "HUN",
    "HK": "HKG",
    "HN": "HND",
    "HM": "HMD",
    "VE": "VEN",
    "PR": "PRI",
    "PS": "PSE",
    "PW": "PLW",
    "PT": "PRT",
    "SJ": "SJM",
    "PY": "PRY",
    "IQ": "IRQ",
    "PA": "PAN",
    "PF": "PYF",
    "PG": "PNG",
    "PE": "PER",
    "PK": "PAK",
    "PH": "PHL",
    "PN": "PCN",
    "PL": "POL",
    "PM": "SPM",
    "ZM": "ZMB",
    "EH": "ESH",
    "EE": "EST",
    "EG": "EGY",
    "ZA": "ZAF",
    "EC": "ECU",
    "IT": "ITA",
    "VN": "VNM",
    "SB": "SLB",
    "ET": "ETH",
    "SO": "SOM",
    "ZW": "ZWE",
    "SA": "SAU",
    "ES": "ESP",
    "ER": "ERI",
    "ME": "MNE",
    "MD": "MDA",
    "MG": "MDG",
    "MF": "MAF",
    "MA": "MAR",
    "MC": "MCO",
    "UZ": "UZB",
    "MM": "MMR",
    "ML": "MLI",
    "MO": "MAC",
    "MN": "MNG",
    "MH": "MHL",
    "MK": "MKD",
    "MU": "MUS",
    "MT": "MLT",
    "MW": "MWI",
    "MV": "MDV",
    "MQ": "MTQ",
    "MP": "MNP",
    "MS": "MSR",
    "MR": "MRT",
    "IM": "IMN",
    "UG": "UGA",
    "TZ": "TZA",
    "MY": "MYS",
    "MX": "MEX",
    "IL": "ISR",
    "FR": "FRA",
    "IO": "IOT",
    "SH": "SHN",
    "FI": "FIN",
    "FJ": "FJI",
    "FK": "FLK",
    "FM": "FSM",
    "FO": "FRO",
    "NI": "NIC",
    "NL": "NLD",
    "NO": "NOR",
    "NA": "NAM",
    "VU": "VUT",
    "NC": "NCL",
    "NE": "NER",
    "NF": "NFK",
    "NG": "NGA",
    "NZ": "NZL",
    "NP": "NPL",
    "NR": "NRU",
    "NU": "NIU",
    "CK": "COK",
    "XK": "XKX",
    "CI": "CIV",
    "CH": "CHE",
    "CO": "COL",
    "CN": "CHN",
    "CM": "CMR",
    "CL": "CHL",
    "CC": "CCK",
    "CA": "CAN",
    "CG": "COG",
    "CF": "CAF",
    "CD": "COD",
    "CZ": "CZE",
    "CY": "CYP",
    "CX": "CXR",
    "CR": "CRI",
    "CW": "CUW",
    "CV": "CPV",
    "CU": "CUB",
    "SZ": "SWZ",
    "SY": "SYR",
    "SX": "SXM",
    "KG": "KGZ",
    "KE": "KEN",
    "SS": "SSD",
    "SR": "SUR",
    "KI": "KIR",
    "KH": "KHM",
    "KN": "KNA",
    "KM": "COM",
    "ST": "STP",
    "SK": "SVK",
    "KR": "KOR",
    "SI": "SVN",
    "KP": "PRK",
    "KW": "KWT",
    "SN": "SEN",
    "SM": "SMR",
    "SL": "SLE",
    "SC": "SYC",
    "KZ": "KAZ",
    "KY": "CYM",
    "SG": "SGP",
    "SE": "SWE",
    "SD": "SDN",
    "DO": "DOM",
    "DM": "DMA",
    "DJ": "DJI",
    "DK": "DNK",
    "VG": "VGB",
    "DE": "DEU",
    "YE": "YEM",
    "DZ": "DZA",
    "US": "USA",
    "UY": "URY",
    "YT": "MYT",
    "UM": "UMI",
    "LB": "LBN",
    "LC": "LCA",
    "LA": "LAO",
    "TV": "TUV",
    "TW": "TWN",
    "TT": "TTO",
    "TR": "TUR",
    "LK": "LKA",
    "LI": "LIE",
    "LV": "LVA",
    "TO": "TON",
    "LT": "LTU",
    "LU": "LUX",
    "LR": "LBR",
    "LS": "LSO",
    "TH": "THA",
    "TF": "ATF",
    "TG": "TGO",
    "TD": "TCD",
    "TC": "TCA",
    "LY": "LBY",
    "VA": "VAT",
    "VC": "VCT",
    "AE": "ARE",
    "AD": "AND",
    "AG": "ATG",
    "AF": "AFG",
    "AI": "AIA",
    "VI": "VIR",
    "IS": "ISL",
    "IR": "IRN",
    "AM": "ARM",
    "AL": "ALB",
    "AO": "AGO",
    "AQ": "ATA",
    "AS": "ASM",
    "AR": "ARG",
    "AU": "AUS",
    "AT": "AUT",
    "AW": "ABW",
    "IN": "IND",
    "AX": "ALA",
    "AZ": "AZE",
    "IE": "IRL",
    "ID": "IDN",
    "UA": "UKR",
    "QA": "QAT",
    "MZ": "MOZ",
}


def document_hash_sha256(base64_str):
    # Decode Base64
    decode_base64 = base64.b64decode(base64_str)
    # Encode the hash in base64
    sha256_hash = sha256(decode_base64).hexdigest()
    return sha256_hash


def base64_encode_json(json_str):
    json_bytes = json_str.encode("utf-8")
    return base64.b64encode(json_bytes)


class AccountMove(models.Model):
    _inherit = "account.move"

    x_file_id = fields.Many2one(
        comodel_name="ir.attachment",
        compute=lambda self: self._compute_linked_attachment_id("x_file_id", "x_file"),
        depends=["x_file"],
        copy=False,
        readonly=True,
        export_string_translation=False,
    )
    sale_order_ids = fields.Many2many("sale.order", string="Sale Order")
    purchase_order_id = fields.Many2one("purchase.order", string="Purchase Order")
    e_invoice_type_code = fields.Selection(
        [
            ("01", "Invoice"),
            ("02", "Credit Note"),
            ("03", "Debit Note"),
            ("04", "Refund Note"),
            ("11", "Self-billed Invoice"),
            ("12", "Self-billed Credit Note"),
            ("13", "Self-billed Debit Note"),
            ("14", "Self-billed Refund Note"),
        ],
        default="01",
        string="E-Invoice Type Code",
        tracking=True,
        track_visibility="onchange",
    )
    x_display_document_type = fields.Char(
        string="Document Label",
    )
    x_cancel_reason = fields.Char("Cancel E-Invoice Reason")
    x_file = fields.Binary(
        string="MyInvois XML File",
        copy=False,
        readonly=True,
        export_string_translation=False,
    )
    x_display_tax_exemption_reason = fields.Boolean(
        compute="_compute_x_display_tax_exemption_reason",
        string="Display Tax Exemption Reason",
        export_string_translation=False,
    )
    x_exemption_reason = fields.Char(
        string="Tax Exemption Reason",
        help="Buyer’s sales tax exemption certificate number, special exemption as per gazette orders, etc.\n"
             "Only applicable if you are using a tax with a type 'Exempt'.",
    )

    # False => Not sent yet.
    x_is_consolidate_invoice = fields.Boolean(
        string="Is Consolidate Invoice", default=False
    )
    x_einvoice_state = fields.Char(
        string="MyInvois State",
        default="draft",
        copy=False,
        readonly=True,
        help="""
            Status of the invoice:
            - Draft: Initial state, not yet submitted.
            - Valid: e-invoice has been reviewed and accepted.
            - Invalid: e-invoice was reviewed and rejected.
            - Submit: The e-invoice has been submitted and is currently being processed.
    """,
    )
    x_my_einvoice_longid = fields.Char(string="LongId")
    x_my_einvoice_link_to_portal = fields.Char(string="Link to portal")
    x_client_provided_link = fields.Char(string="Client Provided Link")

    # Users have 72h after the validation of an invoice to cancel it.
    # Passed that time, they need to issue a credit or debit note.
    x_validation_time = fields.Datetime(
        string="Validation Time",
        copy=False,
        readonly=True,
        export_string_translation=False,
    )
    x_submission_uid = fields.Char(
        string="Submission UID",
        help="Unique ID assigned to a batch of invoices when sent to MyInvois.",
        copy=False,
        readonly=True,
    )

    x_custom_form_reference = fields.Char(
        string="Customs Form Reference Number",
        help="Reference Number of Customs Form No.1, 9, etc.",
    )

    x_type = fields.Selection(
        [
            ("self-bill-refund-note", "Self-bill Refund Note"),
            ("self-bill-debit-note", "Self-bill Debit Note"),
            ("self-bill-credit-note", "Self-bill Credit Note"),
            ("credit-note", "Credit Note"),
            ("debit-note", "Debit Note"),
            ("refund-note", "Refund Note"),
        ],
        string="Type",
    )

    x_recall_times = fields.Integer("Recall Times", default=0)
    x_is_bill_e_invoice_received = fields.Boolean(
        string="Vendor Bill's Received", default=False
    )
    x_manual_check = fields.Boolean("Manual Check", default=False)
    x_sale_tax_amount = fields.Float(string="Sale Tax Amount", default=0)
    x_service_tax_amount = fields.Float(string="Service Tax Amount", default=0)
    x_tourism_tax_amount = fields.Float(string="Tourism Tax Amount", default=0)
    x_high_value_goods_tax_amount = fields.Float(
        string="High Value Goods Tax Amount", default=0
    )
    x_low_value_goods_tax_amount = fields.Float(
        string="Low Value Goods Tax Amount", default=0
    )
    x_not_applicaple_tax_amount = fields.Float(
        string="Not Applicable Tax Amount", default=0
    )
    x_tax_exemtion_amount = fields.Float(string="Tax Exemtion Amount", default=0)
    x_invoice_credit_note_count = fields.Integer(
        string="Invoice credit note count", compute="_compute_invoice_credit_note_count"
    )
    x_invoice_debit_note_count = fields.Integer(
        string="Invoice debit not count", compute="_compute_invoice_debit_note_count"
    )
    x_invoice_refund_note_count = fields.Integer(
        string="Invoice refund note count", compute="_compute_invoice_refund_note_count"
    )

    x_bill_credit_note_count = fields.Integer(
        string="Bill credit note count", compute="_compute_bill_credit_note_count"
    )
    x_bill_debit_note_count = fields.Integer(
        string="Bill debit not count", compute="_compute_bill_debit_note_count"
    )
    x_bill_refund_note_count = fields.Integer(
        string="Bill refund note count", compute="_compute_bill_refund_note_count"
    )

    def _compute_bill_debit_note_count(self):
        """
        Calculates the number of related debit notes for each move.
        """
        for move in self:

            if move.state == "posted":
                domain = [
                    ("debit_origin_id", "=", move.id),
                    ("move_type", "=", "in_invoice"),
                    "|",
                    ("x_type", "=", "self-bill-debit-note"),
                    ("x_type", "=", False),
                ]
                count = self.env["account.move"].search_count(domain)
                move.x_bill_debit_note_count = count
            else:
                move.x_bill_debit_note_count = 0

    def _compute_invoice_debit_note_count(self):
        """
        Calculates the number of related debit notes for each move.
        """
        for move in self:
            if move.state == "posted":
                domain = [
                    ("debit_origin_id", "=", move.id),
                    ("move_type", "=", "out_invoice"),
                    "|",
                    ("x_type", "=", "debit-note"),
                    ("x_type", "=", False),
                ]
                count = self.env["account.move"].search_count(domain)
                move.x_invoice_debit_note_count = count
            else:
                move.x_invoice_debit_note_count = 0

    def _get_last_sequence_domain(self, relaxed=False):
        where_string, param = super()._get_last_sequence_domain(relaxed)
        if self.journal_id.debit_sequence:
            where_string += " AND debit_origin_id IS " + (
                "NOT NULL" if self.debit_origin_id else "NULL"
            )
        return where_string, param

    # def _get_starting_sequence(self):
    #     starting_sequence = super()._get_starting_sequence()
    #     if (
    #         self.journal_id.debit_sequence
    #         and self.debit_origin_id
    #         and self.type in ("in_invoice", "out_invoice")
    #     ):
    #         starting_sequence = "D" + starting_sequence
    #     return starting_sequence

    def _compute_bill_credit_note_count(self):
        """
        Calculates the number of related credit notes for each move.
        """
        for move in self:

            if move.state == "posted":
                # Find all relevant credit notes for this bill.
                # The domain is constructed as follows:
                # 1. The move must be a Customer Credit Note ('in_refund').
                # 2. The custom 'x_type' must be either:
                #    a) 'sell-bill-credit-note' (our custom type for this wizard).
                #    b) Not 'self-bill-refund-note' (this includes standard Odoo-generated credit notes
                #       which may not have our x_type set, while excluding a specific type).
                domain = [
                    ("reversed_entry_id", "=", move.id),
                    ("move_type", "=", "in_refund"),
                    "|",
                    ("x_type", "=", "self-bill-credit-note"),
                    ("x_type", "!=", "self-bill-refund-note"),
                ]
                count = self.env["account.move"].search_count(domain)
                move.x_bill_credit_note_count = count
            else:
                move.x_bill_credit_note_count = 0

    def _compute_invoice_credit_note_count(self):
        """
        Calculates the number of related credit notes for each move.
        """
        for move in self:

            if move.state == "posted":
                # Find all relevant credit notes for this invoice.
                # The domain is constructed as follows:
                # 1. The move must be a Customer Credit Note ('out_refund').
                # 2. The custom 'x_type' must be either:
                #    a) 'credit-note' (our custom type for this wizard).
                #    b) Not 'refund-note' (this includes standard Odoo-generated credit notes
                #       which may not have our x_type set, while excluding a specific type).
                domain = [
                    ("reversed_entry_id", "=", move.id),
                    ("move_type", "=", "out_refund"),
                    "|",
                    ("x_type", "=", "credit-note"),
                    ("x_type", "!=", "refund-note"),
                ]
                count = self.env["account.move"].search_count(domain)
                move.x_invoice_credit_note_count = count
            else:
                move.x_invoice_credit_note_count = 0

    def _compute_invoice_refund_note_count(self):
        """
        Calculates the number of related invoice refund notes for each move.
        """
        for move in self:
            if move.state == "posted":
                domain = [
                    ("reversed_entry_id", "=", move.id),
                    ("move_type", "=", "out_refund"),
                    ("x_type", "=", "refund-note"),
                ]
                count = self.env["account.move"].search_count(domain)
                move.x_invoice_refund_note_count = count
            else:
                move.x_invoice_refund_note_count = 0

    def _compute_bill_refund_note_count(self):
        """
        Calculates the number of related bill refund notes for each move.
        """
        for move in self:
            if move.state == "posted":
                domain = [
                    ("reversed_entry_id", "=", move.id),
                    ("move_type", "=", "in_refund"),
                    ("x_type", "=", "self-bill-refund-note"),
                ]
                count = self.env["account.move"].search_count(domain)
                move.x_bill_refund_note_count = count
            else:
                move.x_bill_refund_note_count = 0

    @api.depends("company_id", "invoice_line_ids.tax_ids")
    def _compute_x_display_tax_exemption_reason(self):
        """Some users will never use tax-exempt taxes, so it's better to only show the field when necessary."""
        for move in self:
            should_display = any(
                tax.x_my_tax_type == "E" for tax in move.invoice_line_ids.tax_ids
            )
            move.x_display_tax_exemption_reason = should_display

    def send_email(self):
        template_id = self.env.ref("a1_einvoice_to_gov.email_template_e_invoice").id
        for invoice in self:
            email_values = {
                "email_to": invoice.partner_id.email,
            }

            self.env["mail.template"].browse(template_id).with_context(
                email_values
            ).send_mail(invoice.id, force_send=True)

    def action_adjustment_bill(self):
        action = self.env.ref("a1_einvoice_to_gov.action_adjustment_bill").read()[0]
        action["context"] = {"default_move_id": self.id}
        return action

    def action_adjustment_invoice(self):
        action = self.env.ref("a1_einvoice_to_gov.action_adjustment_invoice").read()[0]
        action["context"] = {"default_move_id": self.id}
        return action

    @api.model
    def default_get(self, fields):
        res = super(AccountMove, self).default_get(fields)
        if (
                "sale_order_ids" in fields
                and self._context.get("active_model") == "sale.order"
        ):
            active_ids = self._context.get("active_ids", [])
            if active_ids:
                res["sale_order_ids"] = [(6, 0, active_ids)]
                if len(active_ids) > 1:
                    res["x_is_consolidate_invoice"] = True
                if not res.get("invoice_date"):
                    res["invoice_date"] = datetime.now().strftime("%Y-%m-%d")
        elif (
                "purchase_order_id" in fields
                and self._context.get("active_model") == "purchase.order"
        ):
            active_id = self._context.get("active_id")
            if active_id:
                res["purchase_order_id"] = active_id
                res["e_invoice_type_code"] = "11"
        return res

    @api.depends("company_id", "invoice_line_ids.tax_ids")
    def _compute_x_display_tax_exemption_reason(self):
        """Some users will never use tax-exempt taxes, so it's better to only show the field when necessary."""
        for move in self:
            should_display = any(
                tax.x_my_tax_type == "E" for tax in move.invoice_line_ids.tax_ids
            )
            move.x_display_tax_exemption_reason = should_display

    def get_partner_info(self, partner, is_supplier=True, is_invoice=False):
        """
        usage:
            - get partner's info,
            - is_supplier used to distinguish between supplier or buyer
        params: partner, is_supplier
        return: partner's info
        """

        def get_address(partner):
            return (
                partner.street
                if partner.street
                else (partner.street2 if partner.street2 else "NA")
            )

        country_subentity_code = (
            partner.state_id.einvois_code if partner.state_id.einvois_code else "NA"
        )
        if partner.identification_type == "PASSPORT" and partner.country_id.id != 157:
            partner_vat = "EI00000000020" if is_invoice else "EI00000000030"
        else:
            partner_vat = partner.vat or "NA"

        partner_info = [
            {
                "Party": [
                    {
                        "PartyIdentification": [
                            {"ID": [{"_": partner_vat, "schemeID": "TIN"}]},
                            {
                                "ID": [
                                    {
                                        "_": partner.sst_registration_number or "NA",
                                        "schemeID": "SST",
                                    }
                                ]
                            },
                            {
                                "ID": [
                                    {
                                        "_": partner.ttx_registration_number or "NA",
                                        "schemeID": "TTX",
                                    }
                                ]
                            },
                            {
                                "ID": [
                                    {
                                        "_": partner.identification_number or "NA",
                                        "schemeID": partner.identification_type
                                                    or "BRN",
                                    }
                                ]
                            },
                        ],
                        "PostalAddress": [
                            {
                                "CityName": [{"_": partner.state_id.name or "NA"}],
                                # "PostalZone": [{"_": partner.zip or "NA"}],
                                "CountrySubentityCode": [
                                    {
                                        "_": country_subentity_code,
                                    }
                                ],
                                "AddressLine": [
                                    {"Line": [{"_": get_address(partner)}]},
                                ],
                                "Country": [
                                    {
                                        "IdentificationCode": [
                                            {
                                                "_": COUNTRY_CODE_MAP[
                                                    partner.country_id.code
                                                ],
                                                "listID": "ISO3166-1",
                                                "listAgencyID": "6",
                                            }
                                        ]
                                    }
                                ],
                            }
                        ],
                        "PartyLegalEntity": [
                            {"RegistrationName": [{"_": partner.name}]}
                        ],
                        "Contact": [
                            {
                                "Telephone": [{"_": partner.phone}],
                                # Optional
                                "ElectronicMail": [{"_": partner.email}],
                            }
                        ],
                    }
                ],
            }
        ]
        if is_supplier:
            partner_info[0]["Party"][0]["IndustryClassificationCode"] = [
                {
                    "_": partner.a1_einvoice_config_industrial_classification.code
                         or "00000",
                    "name": partner.a1_einvoice_config_industrial_classification.name
                            or "NOT APPLICABLE",
                }
            ]
        return partner_info

    def _get_last_sequence_domain(self, relaxed=False):
        where_string, param = super()._get_last_sequence_domain(relaxed)
        if self.journal_id.debit_sequence:
            where_string += " AND debit_origin_id IS " + (
                "NOT NULL" if self.debit_origin_id else "NULL"
            )
        return where_string, param

    def generate_line_tax_payload(self, tax_type, schemeID, taxable_amount, line):
        amount = getattr(line, tax_type, 0.0)
        currency_code = self.currency_id.display_name
        tax_section = {}
        if amount or tax_type == "x_tax_exemtion_amount":
            tax_section.update(
                {
                    "TaxableAmount": [
                        {
                            "_": taxable_amount,
                            "currencyID": currency_code,
                        }
                    ],
                    "TaxAmount": [
                        {
                            "_": amount,
                            "currencyID": currency_code,
                        }
                    ],
                    "TaxCategory": [
                        {
                            "ID": [{"_": schemeID[0]}],
                            "TaxScheme": [
                                {
                                    "ID": [
                                        {
                                            "_": schemeID[1],
                                            "schemeID": "UN/ECE 5153",
                                            "schemeAgencyID": "6",
                                        }
                                    ]
                                }
                            ],
                        }
                    ],
                }
            )
        if (
                tax_type == "x_not_applicaple_tax_amount"
                and tax_type == "x_tax_exemtion_amount"
        ):
            tax_amount = tax_section["TaxAmount"]
            tax_amount[0]["_"] = 0

        if tax_type == "x_tax_exemtion_amount":
            tax_category = tax_section["TaxCategory"]
            tax_category[0]["TaxExemptionReason"] = [
                {"_": self.x_exemption_reason or "NA"}
            ]

        if tax_section and amount != 0 or tax_type == "x_tax_exemtion_amount":
            return tax_section
        return

    def generate_tax_payload(self, line, taxable_amount=0):
        result = []
        tax_types = {
            "x_tax_exemtion_amount": ["E", "EXE"],
            "x_sale_tax_amount": ["01", "SST"],
            "x_service_tax_amount": ["02", "SVT"],
            "x_tourism_tax_amount": ["03", "OTH"],
            "x_high_value_goods_tax_amount": ["04", "OTH"],
            "x_low_value_goods_tax_amount": ["05", "OTH"],
            "x_not_applicaple_tax_amount": ["06", "ZRE"],
        }
        if line:
            taxable_amount = line.price_subtotal
        else:
            taxable_amount = self.amount_untaxed
        for tax_type, schemeID in tax_types.items():
            lines_to_process = [line] if line else self.invoice_line_ids

            for current_line in lines_to_process:

                tax_line = self.generate_line_tax_payload(
                    tax_type=tax_type,
                    schemeID=schemeID,
                    taxable_amount=taxable_amount,
                    line=current_line,
                )

                # Add to result if tax line was generated
                if tax_line:
                    result.append(tax_line)
        return result

    def prepare_invoice_line(self):
        dict_line = []
        invoice_sale_tax_amount = 0
        invoice_service_tax_amount = 0
        invoice_tourism_tax_amount = 0
        invoice_high_value_goods_tax_amount = 0
        invoice_low_value_goods_tax_amount = 0

        currency_code = self.currency_id.display_name
        for line in self.invoice_line_ids:
            taxes_data = line.tax_ids.compute_all(
                currency=line.move_id.currency_id,
                price_unit=line.price_unit,
                quantity=line.quantity,
                partner=line.partner_id,
                product=line.product_id,
                is_refund=line.move_id.type in ("out_refund", "in_refund"),
            )
            taxes = taxes_data["taxes"]
            if taxes == []:
                line.x_sale_tax_amount = 0
                line.x_sale_tax_amount = 0
                line.x_service_tax_amount = 0
                line.x_tourism_tax_amount = 0
                line.x_high_value_goods_tax_amount = 0
                line.x_low_value_goods_tax_amount = 0
            else:
                for tax in taxes_data["taxes"]:
                    tax_data = self.env["account.tax"].browse(tax["id"])
                    tax_type = tax_data.x_my_tax_type
                    tax_amount = tax["amount"]
                    if tax_type == "01":
                        line.x_sale_tax_amount = tax_amount
                        invoice_sale_tax_amount += tax_amount
                    elif tax_type == "02":
                        line.x_service_tax_amount = tax_amount
                        invoice_service_tax_amount += tax_amount
                    elif tax_type == "03":
                        line.x_tourism_tax_amount = tax_amount
                        invoice_tourism_tax_amount += tax_amount
                    elif tax_type == "04":
                        line.x_high_value_goods_tax_amount = tax_amount
                        invoice_high_value_goods_tax_amount += tax_amount
                    elif tax_type == "05":
                        line.x_low_value_goods_tax_amount = tax_amount
                        invoice_low_value_goods_tax_amount += tax_amount
            line_tax_amount = (
                    line.price_subtotal * sum(t["amount"] for t in line.tax_ids) / 100
            )
            if not self.x_is_consolidate_invoice:
                if line.x_manual_classification_code:
                    product_code = line.x_manual_classification_code
                else:
                    product_code = line.x_classification_code
            else:
                product_code = '004'
            item_data = {
                "ID": [{"_": str(line.id)}],
                # Optional
                "InvoicedQuantity": [{"_": line.quantity, "unitCode": "C62"}],
                # Mandatory
                "LineExtensionAmount": [
                    {"_": line.price_subtotal, "currencyID": currency_code}
                ],
                "TaxTotal": [
                    {  # Mandatory
                        "TaxAmount": [{"_": line_tax_amount, "currencyID": currency_code}],
                        "TaxSubtotal": self.generate_tax_payload(
                            line,
                            taxable_amount=line.price_subtotal,
                        ),
                    }
                ],
                "Item": [
                    {
                        "CommodityClassification": [
                            {  # Mandatory
                                "ItemClassificationCode": [
                                    # Since this is the consolidate invoice the type will always be ''
                                    {"_": product_code, "listID": "CLASS"}
                                ]
                            }
                        ],
                        "Description": [{"_": line.product_id.name}],
                    }
                ],
                "Price": [
                    {"PriceAmount": [{"_": line.price_unit, "currencyID": currency_code}], }
                ],
                "ItemPriceExtension": [
                    {"Amount": [{"_": line.price_subtotal, "currencyID": currency_code}], }
                ],
            }
            dict_line.append(item_data)
        return dict_line

    def create_json_data(self, type_code, is_invoice=True):
        """
        usage: prepare data in order up to MyInvois portal
            there are 3 main parts
            1. General info invoice like total tax, amount, date invoice ...
            2. Line of invoice like products, product classification, price, tax ..
            3. Supplier and buyer's info like TIN, SST, TTx address, name ..
        return:
            data of 3 main parts
        """

        if is_invoice:
            AccountingSupplierParty = self.get_partner_info(
                partner=self.env.company.partner_id, is_invoice=True
            )
            AccountingCustomerParty = self.get_partner_info(
                partner=self.partner_id, is_invoice=True
            )
        else:
            AccountingSupplierParty = self.get_partner_info(partner=self.partner_id)
            AccountingCustomerParty = self.get_partner_info(
                partner=self.env.company.partner_id
            )
        currency_code = self.currency_id.display_name

        invoice_line_data = self.prepare_invoice_line()
        data = {
            "_D": "urn:oasis:names:specification:ubl:schema:xsd:Invoice-2",
            "_A": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
            "_B": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
            "Invoice": [
                {
                    "ID": [{"_": self.name}],
                    "IssueDate": [{"_": str(self.invoice_date)[0:10]}],
                    "IssueTime": [
                        {"_": f"{str(datetime.now()).split(' ')[1].split('.')[0]}Z"}
                    ],
                    "InvoiceTypeCode": [
                        {
                            "_": type_code,
                            "listVersionID": "1.0",
                        }
                    ],
                    "DocumentCurrencyCode": [{"_": currency_code}],
                    "AccountingSupplierParty": AccountingSupplierParty,
                    "AccountingCustomerParty": AccountingCustomerParty,
                    "TaxTotal": [
                        {
                            # Tong tien thue
                            "TaxAmount": [
                                {
                                    "_": self.compute_tax_amount(include_tax=False),
                                    "currencyID": currency_code,
                                }
                            ],
                            "TaxSubtotal": self.generate_tax_payload(
                                line=False, taxable_amount=self.amount_untaxed
                            ),
                        }
                    ],
                    "LegalMonetaryTotal": [
                        {
                            "TaxExclusiveAmount": [
                                {
                                    "_": self.amount_untaxed,
                                    "currencyID": currency_code,
                                }
                            ],
                            "TaxInclusiveAmount": [
                                {
                                    "_": self.compute_tax_amount(include_tax=True),
                                    "currencyID": currency_code,
                                }
                            ],
                            "PayableAmount": [
                                {
                                    "_": self.compute_tax_amount(include_tax=True),
                                    "currencyID": currency_code,
                                }
                            ],
                        }
                    ],
                }
            ],
        }
        data["Invoice"][0]["InvoiceLine"] = invoice_line_data

        # type 02, 03, 12, 13 is debit note or credit note
        if type_code in ["02", "03", "04", "12", "13", "14"]:
            data["Invoice"][0]["BillingReference"] = [
                {
                    "InvoiceDocumentReference": [
                        {
                            "UUID": [
                                {"_": self.reversed_entry_id.x_submission_uid or "NA"}
                            ],
                            "ID": [{"_": self.reversed_entry_id.name or "NA"}],
                        }
                    ]
                }
            ]

        return data

    def compute_tax_amount(self, include_tax=True):
        """
        usage: compute amount include tax or not
        return: amount
        """
        total_tax_amount = 0
        total_amount = 0
        for line in self.invoice_line_ids:
            line_tax_amount = (
                    line.price_subtotal * sum(t["amount"] for t in line.tax_ids) / 100
            )
            total_tax_amount += line_tax_amount
            total_amount += line.price_subtotal + line_tax_amount
        if not include_tax:
            return total_tax_amount
        else:
            return total_amount

    def post_invoice_api(self, api_url, base64_str, access_token):
        """
        post info to MyInvoice Portal
        """
        for rec in self:
            url = f"https://{api_url}/api/v1.0/documentsubmissions"
            headers = {
                "Authorization": "Bearer %s" % access_token,
                "Content-Type": "application/json",
            }
            documentHash = document_hash_sha256(base64_str)
            payload = json.dumps(
                {
                    "documents": [
                        {
                            "format": "JSON",
                            "documentHash": documentHash,
                            "codeNumber": self.name,
                            "document": base64_str,
                        }
                    ]
                }
            )
            response = requests.request("POST", url, headers=headers, data=payload)
            self.create_einvoice_log(
                url,
                str(response.status_code) if response and response.status_code else "",
                payload,
                rec.id,
            )
            return response.json()

    def action_submit(self):
        """
        usage:
            This is main function of e-invoice
            There are 6 types of e-invoice:
                invoice, credit note, debit note, self-billed, self-billed credit note, self-bill debit note
            Update info to odoo when have response
            Track info error or success
        """
        for rec in self:
            api_config_id = self.env["api.myinvoice.config"].search(
                [("company_id", "=", self.company_id.id), ("is_active", "=", True)], limit=1
            )
            if not api_config_id:
                raise ValidationError(_("Firstly you need to config API!"))

            if rec.x_type:
                if rec.x_type == "self-bill-refund-note":
                    type_code = "14"
                    is_invoice = False
                elif rec.x_type == "self-bill-debit-note":
                    type_code = "13"
                    is_invoice = False
                elif rec.x_type == "self-bill-credit-note":
                    type_code = "12"
                    is_invoice = False
                elif rec.x_type == "credit-note":
                    type_code = "02"
                    is_invoice = True
                elif rec.x_type == "debit-note":
                    type_code = "03"
                    is_invoice = True
                else:
                    type_code = "04"
                    is_invoice = True
            else:
                if rec.type == "out_invoice":
                    type_code = "01"
                    is_invoice = True
                else:
                    type_code = "11"
                    is_invoice = False

            json_str = json.dumps(
                rec.create_json_data(type_code=type_code, is_invoice=is_invoice),
                separators=(",", ":"),
            )
            base64_str = base64_encode_json(json_str).decode("utf8")
            api_config_id.action_get_access_token()
            access_token = api_config_id.access_token
            response = rec.post_invoice_api(api_url, base64_str, access_token)
            rec.message_post(body=_("API have sent successful!"))
            err = response.get("error")
            if err:
                error_message = err.get("message")
                if not error_message:
                    for detail in err.get("details", []):
                        msg = detail.get("message")
                        if msg:
                            error_message = msg
                            break
                if not error_message:
                    error_message = _("Error from MyInvois API")
                raise UserError(_("E-invoice submission failed:\n%s") % error_message)
            accepted = response.get("acceptedDocuments") or []
            if accepted:
                rec.update(
                    {
                        "x_einvoice_state": "submit",
                        "x_submission_uid": response["acceptedDocuments"][0]["uuid"],
                    }
                )
                rec.action_get_submission_detail()
            rejected = response.get("rejectedDocuments") or []
            if rejected:
                err = rejected[0].get("error", {})
                message_detail = (
                        err.get("details", [{}])[0].get("message")
                        or err.get("message")
                        or ""
                )
                if "ArrayItemNotValid" in message_detail:
                    raise UserError(
                        _(
                            "Submission Failed!\n"
                            "Message Error: There is something wrong with your Product Item.\n"
                            "Please check these fields (classification code, price, etc.) and try again."
                        )
                    )
                raise UserError(
                    _("Submission Failed!\n" "Message Error: %s")
                    % self.format_key_value(message_detail)
                )
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "title": _("E-Invoice Sent"),
                    "type": "success",
                },
            }

    def action_cancel(self):
        api_config_id = self.env["api.myinvoice.config"].search(
            [("company_id", "=", self.company_id.id), ("is_active", "=", True)], limit=1
        )
        if not api_config_id:
            raise ValidationError(_("API configuration not found"))
        api_config_id.action_get_access_token()
        access_token = api_config_id.access_token
        if not access_token:
            raise ValidationError(_("Failed to retrieve access token"))
        url = (
            f"https://{api_url}/api/v1.0/documents/state/{self.x_submission_uid}/state"
        )

        payload = json.dumps({"status": "cancelled", "reason": self.x_cancel_reason})
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        try:
            response = requests.put(url, headers=headers, data=payload)
            response.raise_for_status()
            self.x_einvoice_state = "cancel"

        except requests.exceptions.RequestException as e:
            error_message = f"Request failed: {str(e)}"
            raise ValidationError(
                _("Error when cancelling invoice: %s" % error_message)
            )
        except Exception as e:
            error_message = str(e)
            raise ValidationError(
                _("Error when cancelling invoice: %s" % error_message)
            )

    def button_cancel(self):
        if self.x_einvoice_state in ["submit", "valid"]:
            raise UserError(_("You have to cancel E-invoice first."))
        return super(AccountMove, self).button_cancel()

    def action_create_consolidate_invoice(self):
        action = self.env.ref(
            "a1_einvoice_to_gov.action_create_consolidate_invoice"
        ).read()[0]
        action["context"] = {"default_move_id": self.id}
        return action

    def action_open_wizard_cancel_reason(self):
        validation_date = fields.Datetime.from_string(self.x_validation_time)
        time_gap = datetime.now() - validation_date

        if time_gap > timedelta(hours=72):
            raise UserError(
                _(
                    "The E-Invoice cannot be cancel as it was sent more than 72 hours ago."
                )
            )
        action = (
            self.sudo()
            .env.ref("a1_einvoice_to_gov.action_write_cancel_einvoice_reason")
            .read([])[0]
        )
        return action

    def create_einvoice_log(self, name, error_code, json_data, e_invoice_id):
        self.env["api.myinvoice.log"].sudo().create(
            {
                "name": name,
                "error_code": error_code,
                "data": json_data,
                "e_invoice_id": e_invoice_id,
            }
        )

    def action_get_submission_detail(self):
        """
        usage: get detail info of e-invoice when we have uuid
        uuid is id of invoice on MyInvoice Portal
        """
        api_config_id = self.env["api.myinvoice.config"].search(
            [("company_id", "=", self.company_id.id), ("is_active", "=", True)], limit=1
        )
        api_base_url = api_url
        api_config_id.action_get_access_token()
        access_token = api_config_id.access_token
        url = "https://%s/api/v1.0/documents/%s/details" % (
            api_base_url,
            self.x_submission_uid,
        )

        payload = {}
        headers = {"Authorization": "Bearer %s" % access_token}
        time.sleep(3)
        response = requests.request("GET", url, headers=headers, data=payload)
        json_result = response.json()
        self.create_einvoice_log(
            url,
            str(response.status_code) if response and response.status_code else "",
            payload,
            self.id,
        )
        self.x_recall_times += 1
        try:
            if response.status_code == 200:
                if json_result["validationResults"]:
                    if json_result["validationResults"]["status"] == "Invalid":
                        invalid_steps = []
                        for step in json_result["validationResults"]["validationSteps"]:
                            if step["status"] == "Invalid":
                                invalid_steps.append(step)
                        self.message_post(
                            body=_("API Get Submission Details: %s" % invalid_steps)
                        )
                    else:
                        self.message_post(
                            body=_("API Get Submission Details: Document Valid.")
                        )
                document_status = json_result["status"]
                if document_status:
                    if document_status == "Submitted":
                        self.x_einvoice_state = "submit"
                    elif document_status == "Valid":
                        self.write(
                            {
                                "x_validation_time": datetime.strptime(
                                    json_result["dateTimeValidated"],
                                    "%Y-%m-%dT%H:%M:%SZ",
                                ),
                                "x_einvoice_state": "valid",
                                "x_my_einvoice_longid": json_result["longId"],
                                "x_my_einvoice_link_to_portal": f"https://{share_url}/{self.x_submission_uid}/share/{json_result['longId']}",
                            }
                        )
                        self.action_send_email()
                    elif document_status == "Invalid":
                        self.write(
                            {
                                "x_einvoice_state": "invalid",
                                "x_my_einvoice_link_to_portal": f"https://{share_url}/documents/{json_result['uuid']}",
                            }
                        )
                    else:
                        self.x_einvoice_state = "cancel"
            else:
                raise ValidationError(
                    _(
                        "Error when cancel invoice: %s" % json_result["message"]
                        if "message" in response
                        else json_result["error"]["message"]
                    )
                )
        except Exception:
            raise ValidationError(
                _(
                    "Error when cancel invoice: %s" % json_result["message"]
                    if "message" in response
                    else json_result["error"]["message"]
                )
            )

    def cron_get_einvoice_submission_detail(self):
        # Fetch config recall times
        api_config_id = self.env["api.myinvoice.config"].search(
            [("company_id", "=", self.company_id.id), ("is_active", "=", True)], limit=1
        )
        config_recall_times = api_config_id.recall_times
        if config_recall_times == 0:
            config_recall_times = 3
        # Search e-invoice that over times to get submisson
        move_over_ids = self.search(
            [
                ("x_recall_times", ">", config_recall_times),
                ("x_einvoice_state", "in", ["submit", "invalid"]),
                ("x_manual_check", "=", False),
            ]
        )

        move_over_ids.write({"x_manual_check": True})
        # Search for e-invoices that meet the criteria
        move_ids_recall = self.search(
            [
                ("x_recall_times", "<=", config_recall_times),
                ("x_einvoice_state", "in", ["submit", "invalid"]),
            ]
        )
        # Process each e-invoice
        for invoice in move_ids_recall:
            invoice.action_get_submission_detail()

    def action_send_email(self):
        template_id = self.env.ref(
            "a1_einvoice_to_gov.email_template_e_invoice"
        ).id
        for invoice in self:
            email_values = {
                "email_to": invoice.partner_id.email,
            }

            self.env["mail.template"].browse(template_id).with_context(
                email_values
            ).send_mail(invoice.id, force_send=True)

    def action_submit_and_get_status(self):
        self.action_submit()
        if self.name != "New":
            self.action_get_submission_detail()

    def get_user_friendly_datetime(self, dt):
        if dt:
            user_datetime = fields.Datetime.context_timestamp(
                self, fields.Datetime.from_string(dt)
            )
            return user_datetime.strftime("%d-%m-%Y %H:%M:%S")
        return None

    def format_key_value(self, data, indent=0):
        indent_space = "-" * indent
        result = []
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    result.append(
                        "{indent_space}- {key}:".format(
                            indent_space=indent_space, key=key
                        )
                    )
                    result.append(self.format_key_value(value, indent + 2))
                else:
                    result.append(
                        "{indent_space}- {key}: {value}".format(
                            indent_space=indent_space, key=key, value=value
                        )
                    )
        elif isinstance(data, list):
            for item in data:
                result.append(self.format_key_value(item, indent))
        else:
            result.append(
                "{indent_space}- {data}".format(indent_space=indent_space, data=data)
            )
        return "\n".join(result)

    def action_view_self_bill_credit_note(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Self Billed's Credit Note Button",
            "res_model": "account.move",
            "view_mode": "tree,form",
            "views": [
                (
                    self.env.ref(
                        "a1_einvoice_to_gov.view_account_move_refund_note_list"
                    ).id,
                    "list",
                ),
                (self.env.ref("account.view_move_form").id, "form"),
            ],
            "domain": [
                ("x_type", "=", "refund-note"),
                ("reversed_entry_id", "=", self.id),
            ],
            "context": {"default_type": "entry"},
            "target": "current",
        }

    def action_view_refund_note(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Invoice's Refund Note Button",
            "res_model": "account.move",
            "view_mode": "tree,form",
            "views": [
                (
                    self.env.ref(
                        "a1_einvoice_to_gov.view_account_move_refund_note_list"
                    ).id,
                    "list",
                ),
                (self.env.ref("account.view_move_form").id, "form"),
            ],
            "domain": [
                ("x_type", "=", "refund-note"),
                ("reversed_entry_id", "=", self.id),
            ],
            "context": {"default_type": "entry"},
            "target": "current",
        }

    def action_view_debit_note(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Invoice's Debit Note Button",
            "res_model": "account.move",
            "view_mode": "tree,form",
            "views": [
                (
                    self.env.ref(
                        "a1_einvoice_to_gov.view_account_move_debit_note_list"
                    ).id,
                    "list",
                ),
                (self.env.ref("account.view_move_form").id, "form"),
            ],
            "domain": [
                ("x_type", "=", "debit-note"),
                ("reversed_entry_id", "=", self.id),
            ],
            "context": {"default_type": "entry"},
            "target": "current",
        }

    def action_view_credit_note(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Invoice's Debit Note ButtonEntries",
            "res_model": "account.move",
            "view_mode": "tree,form",
            "views": [
                (self.env.ref("account.view_invoice_tree").id, "list"),
                (self.env.ref("account.view_move_form").id, "form"),
            ],
            "domain": [
                ("x_type", "=", "credit-note"),
                ("reversed_entry_id", "=", self.id),
            ],
            "context": {"default_type": "entry"},
            "target": "current",
        }

    def action_view_bill_debit_note(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Bill's Debit Note Button",
            "res_model": "account.move",
            "view_mode": "tree,form",
            "views": [
                (
                    self.env.ref(
                        "a1_einvoice_to_gov.view_account_move_bill_debit_note_list"
                    ).id,
                    "list",
                ),
                (self.env.ref("account.view_move_form").id, "form"),
            ],
            "domain": [
                ("x_type", "=", "self-bill-debit-note"),
                ("reversed_entry_id", "=", self.id),
            ],
            "context": {"default_type": "entry"},
            "target": "current",
        }

    def action_view_bill_credit_note(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Bill's Credit Note Button",
            "res_model": "account.move",
            "view_mode": "tree,form",
            "views": [
                (
                    self.env.ref(
                        "a1_einvoice_to_gov.view_account_move_bill_credit_note_list"
                    ).id,
                    "list",
                ),
                (self.env.ref("account.view_move_form").id, "form"),
            ],
            "domain": [
                ("x_type", "=", "self-bill-credit-note"),
                ("reversed_entry_id", "=", self.id),
            ],
            "context": {"default_type": "entry"},
            "target": "current",
        }

    def action_view_bill_refund_note(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Bill's Refund Note Button",
            "res_model": "account.move",
            "view_mode": "tree,form",
            "views": [
                (
                    self.env.ref(
                        "a1_einvoice_to_gov.view_account_move_bill_refund_note_list"
                    ).id,
                    "list",
                ),
                (self.env.ref("account.view_move_form").id, "form"),
            ],
            "domain": [
                ("x_type", "=", "self-bill-refund-note"),
                ("reversed_entry_id", "=", self.id),
            ],
            "context": {"default_type": "entry"},
            "target": "current",
        }
