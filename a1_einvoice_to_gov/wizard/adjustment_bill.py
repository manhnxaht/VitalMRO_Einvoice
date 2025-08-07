from odoo import _, api, fields, models


class AdjustmentBill(models.TransientModel):
    _name = "adjustment.bill"
    _description = "Wizard to create a self-bill credit/debit note"

    type_bill = fields.Selection(
        [
            ("self-bill-refund-note", "Self-billed Refund Note"),
            ("self-bill-debit-note", "Self-billed Debit Note"),
            ("self-bill-credit-note", "Self-billed Credit Note"),
        ],
        string="Type",
        required=True,
    )

    move_id = fields.Many2one(
        "account.move",
        string="Original Vendor Bill",
        required=True,
        domain="[('move_type', 'in', ('in_invoice','in_refund'))]",
    )

    @api.onchange("move_id")
    def _onchange_move_id(self):
        if self.move_id and self.move_id.move_type not in ("in_invoice", "in_refund"):
            return {
                "warning": {
                    "title": "Invalid Selection",
                    "message": "Please select a Vendor Bill or Vendor Credit Note.",
                }
            }

    def action_create_bill(self):
        type_bill = self.type_bill
        defaults = {
            "invoice_date": fields.Date.context_today(self),
            "journal_id": self.move_id.journal_id.id,
            "x_type": type_bill,
        }

        # map wizard choice to move_type
        if self.type_bill == "self-bill-credit-note":
            defaults["type"] = "in_refund"
            defaults["e_invoice_type_code"] = "12"
            defaults["reversed_entry_id"] = self.move_id.id

        elif self.type_bill == "self-bill-refund-note":
            defaults["type"] = "in_refund"
            defaults["e_invoice_type_code"] = "14"
            defaults["reversed_entry_id"] = self.move_id.id


        if type_bill == "self-bill-debit-note":
            # use Odoo's built-in copy helper to copy lines in invoice when create debit note
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
            move_id.e_invoice_type_code = "13"
            move_id.x_type = "self-bill-debit-note"
            return self.open_new_bill(move_id=debit_move["res_id"])

        else:
            # use Odoo's built-in reverse helper to invert lines and balance the move
            reversed_moves = self.move_id._reverse_moves(default_values_list=[defaults])
            new_move = reversed_moves and reversed_moves[0]

        return self.open_new_bill(move_id=new_move.id)

    def open_new_bill(self, move_id):

        return {
            "name": _("Adjustment Invoice"),
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "account.move",
            "res_id": move_id,
            "view_id": self.env.ref("account.view_move_form").id,
            "target": "current",
        }
