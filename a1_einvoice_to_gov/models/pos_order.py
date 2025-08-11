from odoo import api, models

class PosOrder(models.Model):
    _inherit = 'pos.order'
    
    @api.model
    def create(self, vals):
        """Automatically create a Sale Order with 
        Default Customer for each POS Order"""
        pos_order = super(PosOrder, self).create(vals)
        
        default_customer = self.env['res.partner'].search([
            ('is_company', '=', True), 
            ('name', '=', 'General Public')], limit=1)
        if not default_customer:
            all_states = self.env['res.country.state'].search([
                ('name', '=', 'All States'), 
                ('country_id.code', '=', 'MY')], limit=1)
            
            # create All State option if not exist
            if not all_states:
                all_states = self.env['res.country.state'].create({
                    'name': 'All States',
                    'code': 'ALL',
                    'einvois_code': '17',
                    'country_id': self.env['res.country'].search(
                        [('code', '=', 'MY')], 
                        limit=1).id,
                })
            
            # Create Default Customer
            default_customer = self.env['res.partner'].create({
                'name': 'General Public',
                'is_company': True,
                'vat': 'C11062158010',
                'customer_rank': 1, 
                'city': 'NA',
                'street': 'NA',
                'sst_registration_number': 'NA',
                'identification_type': 'BRN',
                'identification_number': '0000000000',
                'tin_validation_state': 'valid',
                'state_id': all_states.id,
                'phone': '60000000000',
                'mobile': '60000000000',
                'email': 'generalpublic@gmail.com',
                'country_id': self.env['res.country'].search(
                    [('code', '=', 'MY')], 
                    limit=1).id,
            })

        # Get product lines in POS Order
        order_lines = vals.get('lines', [])
        sale_order_lines = []
        for line in order_lines or []:
            product = self.env['product.product'].browse(
                line[2].get('product_id'))
            
            sale_order_lines.append((0, 0, {
                'product_id': product.id,
                'product_uom_qty': line[2].get('qty', 1),
                'price_unit': line[2].get('price_unit', product.list_price),
            }))

        # Create Sale Order with Default Customer
        if sale_order_lines:
            sale_order = self.env['sale.order'].create({
                'pos_order_id': pos_order.id,
                'partner_id': default_customer.id,
                'company_id': pos_order.company_id.id,
                'state': 'sale',
                'x_is_pos_order': True,
                'order_line': sale_order_lines,
            })
        
            picking = sale_order.picking_ids.filtered(lambda p: p.state not in ['done', 'cancel'])
            
            if picking:
                picking.action_assign()  
                for move in picking.move_lines:
                    move.quantity_done = move.product_uom_qty 
                picking.button_validate()

        return pos_order
