from odoo import models, fields


class WriteCancelEInvoice(models.TransientModel):
    _name = "write.cancel.einvoice.reason"

    cancel_reason = fields.Char(string="Reason", required=False)

    def action_confirm_cancel_einvoice(self):
        active_id = self._context.get("active_id", False)
        active_model = self._context.get("active_model", False)
        einvoice_myinvoice = self.env[active_model].browse(active_id)
        einvoice_myinvoice.write(
            {
                "x_cancel_reason": self.cancel_reason,
            }
        )
        einvoice_myinvoice.action_cancel()
