from hashlib import new

from odoo import _, api, fields, models


class AdjustmentInvoice(models.TransientModel):
    _name = "adjustment.invoice"
    _description = "Wizard to create refund/debit/credit notes for existing invoices"

    move_id = fields.Many2one("account.move", string="Original Invoice", required=True)

    type_invoice = fields.Selection(
        [
            ("refund-note", "Refund"),
            ("debit-note", "Debit Note"),
            ("credit-note", "Credit Note"),
        ],
        string="Invoice Type",
        required=True,
    )

    def action_create_invoice(self):
        self.ensure_one()
        # prepare values for the reversed move
        defaults = {
            "invoice_date": fields.Date.context_today(self),
            "journal_id": self.move_id.journal_id.id,
            "x_type": self.type_invoice,
        }

        type_invoice = self.type_invoice
        # map wizard choice to move_type
        if type_invoice == "debit-note":
            defaults["move_type"] = "out_invoice"
            defaults["e_invoice_type_code"] = "03"
            defaults["debit_origin_id"] = self.move_id.id
        elif type_invoice == "credit-note":
            defaults["type"] = "out_refund"
            defaults["e_invoice_type_code"] = "02"
            defaults["reversed_entry_id"] = self.move_id.id
        else:
            defaults["type"] = "out_refund"
            defaults["e_invoice_type_code"] = "04"
            defaults["reversed_entry_id"] = self.move_id.id

        if type_invoice == "debit-note":
            # use Odoo's built-in copy helper to copy lines in invoice when create debit note
            # new_move = self.move_id.copy(default=defaults)
            move = self.move_id
            new_move = {}
            account_debit_instance = self.env["account.debit.note"].create(
                {
                    "move_ids": [(6, 0, move.ids)],  # Link to the original invoice
                    "copy_lines": True,
                    "reason": "Debit note from adjustment",  # You can add other fields
                    "date": fields.Date.today(),
                }
            )
            debit_move = account_debit_instance.create_debit()
            move_id = self.env["account.move"].browse(debit_move.get("res_id"))
            move_id.x_type = "debit-note"
            move_id.e_invoice_type_code = "03"
            return self.open_new_invoice(move_id=debit_move["res_id"])

        else:
            # use Odoo's built-in reverse helper to invert lines and balance the move
            reversed_moves = self.move_id._reverse_moves(default_values_list=[defaults])
            new_move = reversed_moves and reversed_moves[0]
            return self.open_new_invoice(move_id=new_move.id)

    def open_new_invoice(self, move_id):
        return {
            "name": _("Adjustment Invoice"),
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "view_mode": "form",
            "res_id": move_id,
            "view_id": self.env.ref("account.view_move_form").id,
            "target": "current",
        }
