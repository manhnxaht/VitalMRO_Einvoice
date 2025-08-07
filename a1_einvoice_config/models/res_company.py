from odoo import models, fields, api


class ResCompany(models.Model):
    _inherit = "res.company"

    sst_registration_number = fields.Char(related='partner_id.sst_registration_number', readonly=False)
    ttx_registration_number = fields.Char(related='partner_id.ttx_registration_number', readonly=False)
    identification_number = fields.Char(related='partner_id.identification_number', readonly=False)
    identification_number_placeholder = fields.Char(
        compute="_compute_identification_number_placeholder")
    identification_type = fields.Selection(
        related='partner_id.identification_type',
        readonly=False,
        string="Identification Type",
    )

    a1_einvoice_config_industrial_classification = fields.Many2one(
        related='partner_id.a1_einvoice_config_industrial_classification', readonly=False)

    @api.depends('identification_number')
    def _compute_identification_number_placeholder(self):
        """ Computes a dynamic placeholder that depends on the selected type to help the user inputs their data.
        The placeholders have been taken from the MyInvois doc.
        """
        for company in self:
            placeholder = 'N/A'
            if company.identification_number == 'NRIC':
                placeholder = '830503-11-4923'
            elif company.identification_number == 'BRN':
                placeholder = '202201234565'
            elif company.identification_number == 'PASSPORT':
                placeholder = 'A00000000'
            elif company.identification_number == 'ARMY':
                placeholder = '830805-13-4983'
            company.identification_number_placeholder = placeholder
