def get_default_user(self):
    return self.env['res.partner'].search([
        ('is_company', '=', True),
        ('name', '=', 'General Public')], limit=1)

