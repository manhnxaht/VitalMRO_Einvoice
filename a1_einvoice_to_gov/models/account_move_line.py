from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    x_classification_code = fields.Char(
        # string="Classification Code", compute="_compute_classification_code", store=True
        string="Classification Code", store=True
    )

    x_manual_classification_code = fields.Selection(
        string="Manual Classification Code",
        help="Use this if you want this invoice line have different Classification code",
        # compute="_compute_classification_code",
        default=False,
        selection=[
            ("001", "(001) Breastfeeding equipment "),
            ("002", "(002) Child care centres and kindergartens fees"),
            ("003", "(003) Computer, smartphone or tablet"),
            ("004", "(004) Consolidated e-Invoice "),
            (
                "005",
                "(005) Construction materials (as specified under Fourth Schedule of the Lembaga Pembangunan Industri Pembinaan Malaysia Act 1994)",
            ),
            ("006", "(006) Disbursement"),
            ("007", "(007) Donation"),
            ("008", "(008) -Commerce - e-Invoice to buyer / purchaser"),
            ("009", "(009) e-Commerce - Self-billed e-Invoice to seller, logistics, etc. "),
            ("010", "(010) Education fees"),
            ("011", "(011) Goods on consignment (Consignor)"),
            ("012", "(012) Goods on consignment (Consignee)"),
            ("013", "(013) Gym membership"),
            ("014", "(014) Insurance - Education and medical benefits"),
            ("015", "(015) Insurance - Takaful or life insurance"),
            ("016", "(016) Interest and financing expenses"),
            ("017", "(017) Internet subscription"),
            ("018", "(018) Land and building"),
            (
                "019",
                "(019) Medical examination for learning disabilities and early intervention or rehabilitation treatments of learning disabilities",
            ),
            ("020", "(020) Medical examination or vaccination expenses"),
            ("021", "(021) Medical expenses for serious diseases"),
            ("022", "(022) Others"),
            (
                "023",
                "(023) Petroleum operations (as defined in Petroleum (Income Tax) Act 1967)",
            ),
            ("024", "(024) Private retirement scheme or deferred annuity scheme"),
            ("025", "(025) Motor vehicle"),
            (
                "026",
                "(026) Subscription of books / journals / magazines / newspapers / other similar publications",
            ),
            ("027", "(027) Reimbursement"),
            ("028", "(028) Rental of motor vehicle"),
            (
                "029",
                "(029) EV charging facilities (Installation, rental, sale / purchase or subscription fees) ",
            ),
            ("030", "(030) Repair and maintenance"),
            ("031", "(031) Research and development"),
            ("032", "(032) Foreign income"),
            ("033", "(033) Self-billed - Betting and gaming"),
            ("034", "(034) Self-billed - Importation of goods"),
            ("035", "(035) Self-billed - Importation of services"),
            ("036", "(036) Self-billed - Others"),
            (
                "037",
                "(037) Self-billed - Monetary payment to agents, dealers or distributors",
            ),
            (
                "038",
                "(038) Fees related to sports equipment, facility rentals, competition registration, and training imposed by registered sports organizations under the Sports Development Act 1997",
            ),
            ("039", "(039) Supporting equipment for disabled person"),
            ("040", "(040) Voluntary contribution to approved provident fund "),
            ("041", "(041) Dental examination or treatment"),
            ("042", "(042) Fertility treatment"),
            (
                "043",
                "(043) Treatment and home care nursing, daycare centres and residential care centers",
            ),
            ("044", "(044) Vouchers, gift cards, loyalty points, etc"),
            (
                "045",
                "(045) Self-billed - Non-monetary payment to agents, dealers or distributors",
            ),
        ],
    )

    @api.onchange("x_manual_classification_code")
    def onchange_manual_classification_code(self):
        for rec in self:
            if  self.product_id.manual_classification_code and rec.x_manual_classification_code == self.product_id.manual_classification_code:
                rec.x_manual_classification_code = False
                self.product_id.manual_classification_code = False
            self.product_id.manual_classification_code = rec.x_manual_classification_code

    @api.depends("move_id.partner_id", "product_id", "x_manual_classification_code")
    def _compute_classification_code(self):
        for record in self:
            if record.product_id.manual_classification_code:
                record.x_manual_classification_code = record.product_id.manual_classification_code
            else:
                record.x_manual_classification_code = ''
            partner_id = record.move_id.partner_id
            if partner_id and record.product_id:
                if partner_id.country_id.code == "MY":
                    record.x_classification_code = record.product_id.product_tmpl_id.classification_code

                else:
                    record.x_classification_code = record.product_id.product_tmpl_id.foreign_classification_code

            else:
                record.x_classification_code = ""

