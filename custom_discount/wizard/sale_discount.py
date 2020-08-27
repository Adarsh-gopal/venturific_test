from odoo import api, fields, models, _

class CustomSaleDiscount(models.Model):
    _name = "custom.sale.discount"
    _rec_name = 'discount'
    _description = 'Apply Sale Discount'

    discount = fields.Selection([
        ('flat_disc', 'Flat Discount'),
        ('disc', 'Discount%'),
        ('premium','Premium/Non Premium')], string='Discount')
    flat_discount = fields.Float(string='Flat Price')
    disc = fields.Float(string='Disc%')
    premium_disc = fields.Float(string='Premium Disc%')
    non_premium_disc = fields.Float(string='Non Premium Disc%')

    def process_discount(self):
        context=self._context
        record=self.env['sale.order'].search([('id','=',self._context['parent_obj'])])
        if record:
            record.button_visible = True
            for l in record:
                for line in l.order_line:
                    if self.flat_discount != 0.00:
                        line.price_unit = self.flat_discount
                    elif self.disc != 0.00:
                        line.discount = self.disc
                    elif self.premium_disc != 0.00 or self.non_premium_disc != 0.00:
                        if self.discount == line.product_class:
                            line.discount = self.premium_disc
                        if line.non_premium == True:
                            line.discount = self.non_premium_disc
            record.tax_inc()