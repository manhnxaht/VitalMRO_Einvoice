from odoo import fields, models


class CreateConsolidateInvoice(models.TransientModel):
    _name = 'create.consolidate.invoice'
    _description = 'Wizard to consolidate POS and Sale orders into one invoice'

    creator_id = fields.Many2one('res.partner', string='Creator')
    invoice_create_date = fields.Date(string='Invoice Date', default=fields.Date.context_today)
    pos_orders = fields.Many2many('pos.order', string='Point of Sale Orders')
    sale_orders = fields.Many2many('sale.order', string='Sale Orders')
    def create_consolidate_invoice(self):
        default_user = self.env['res.partner'].search([
            ('is_company', '=', True),
            ('name', '=', 'General Public')], limit=1)
        partner_id = default_user.id
        invoice_lines = []
        for pos in self.pos_orders:
            for line in pos.lines:
                income_account = line.product_id.property_account_income_id or line.product_id.categ_id.property_account_income_categ_id
                invoice_lines.append((0, 0, {
                    'product_id': line.product_id.id,
                    'quantity': line.qty,
                    'account_id': income_account.id,
                    'price_unit': line.price_unit,
                    'name': line.display_name,
                    'tax_ids': [(6, 0, line.tax_ids.ids)] if line.tax_ids else [],
                }))
        for sale in self.sale_orders:
            for line in sale.order_line:
                income_account = line.product_id.property_account_income_id or line.product_id.categ_id.property_account_income_categ_id
                invoice_lines.append((0, 0, {
                    'product_id': line.product_id.id,
                    'account_id': income_account.id,
                    'quantity': line.product_uom_qty,
                    'price_unit': line.price_unit,
                    'name': line.display_name,
                    'tax_ids': [(6, 0, line.tax_id.ids)] if line.tax_id else [],
                }))

        invoice = self.env['account.move'].create({
            'type': 'out_invoice',
            'partner_id': partner_id,
            'invoice_date': fields.Date.context_today(self),
            'invoice_line_ids': invoice_lines,
            'x_is_consolidate_invoice': True,
        })
        # optionally:
        # invoice.action_post()

        return {
            'type': 'ir.actions.act_window',
            'name': 'Consolidated Invoice',
            'view_mode': 'form',
            'res_model': 'account.move',
            'res_id': invoice.id,
            'target': 'current',
        }

    def close_wizard(self):
        """
        Close the wizard popup/window.
        """
        return {
            'type': 'ir.actions.act_window_close'
        }
