from odoo import api, fields, models, _
import pdb

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"


    product_class = fields.Selection([
        ('premium', 'Premium'),
        ('non_premium', 'Non-Premium')], string='Product Class',store=True,track_visibility='always',compute='compute_class')
    non_premium = fields.Boolean('Check Non Premium',store=True,track_visibility='always',compute='compute_non_premium')
    price = fields.Float('Standard Price',store=True,track_visibility='always',related='product_id.lst_price')
    barcode = fields.Char("Barcode",store=True,track_visibility='always',compute='compute_class')
    # boxs = fields.Many2one('stock.quant.package',string='Box')

    # @api.onchange('product_id')
    # def Onchange_box(self):
    #     for l in self:
    #         for line in l.order_id:
    #             l.boxs = line.box.id


    @api.depends('product_id')
    def compute_class(self):
        for l in self:
            l.product_class = l.product_id.product_class
            l.barcode = l.product_id.barcode

    @api.depends('product_class')
    def compute_non_premium(self):
   		self.non_premium = False
   		for l in self:
   			if l.product_class == 'non_premium':
   				l.non_premium = True

class SaleOrder(models.Model):
    _inherit = "sale.order"

    button_visible = fields.Boolean(string='Tax Compute Button Visibility')

    def discount_custom(self):
    	view_id = self.env.ref('custom_discount.sale_discount_coustom_view_form').id
    	context = self._context.copy()
    	return {
    		'name':'Sale Order',
    		'view_type':'form',
    		'view_mode':'form',
    		'views' : [(view_id,'form')],
    		'res_model':'custom.sale.discount',
    		'view_id':view_id,
    		'type':'ir.actions.act_window',
    		'target':'new',
    		'context':{'parent_obj': self.id},
    	}

    def discount_undo(self):
    	for l in self:
    		for line in l.order_line:
    			line.discount = 0.00
    			line.price_unit = line.price

    # def action_confirm(self):
    #     check = super(SaleOrder, self).action_confirm()
    #     for l in self:
    #         for s in l.order_line:
    #             rec = self.env['stock.picking'].search([('sale_id','=',l.id)])
    #             for r in rec:
    #                 for line in rec.move_line_ids_without_package:
    #                     if s.product_id.id == line.product_id.id:
    #                         line.result_package_id = s.boxs.id

    #     return check

    # def tax_inc(self):
    #     for l in self:
    #         for line in l.order_line:
    #             if line.price_subtotal < 1000 or line.price_subtotal > 1000:
    #                 line.tax_id = False
    #                 record = self.env['account.fiscal.position'].search([('sale','=','True')])
    #                 if record:
    #                     for t in record:
    #                         #pdb.set_trace()
    #                         if l.fiscal_position_id.sale == True:
    #                             if t.sale == True and line.price_subtotal < 1000:
    #                                 rec = self.env['account.tax'].search([('name','=','GST 5%')])
    #                                 if rec:
    #                                     for s in rec:
    #                                         line.tax_id = [(6,0,[s.id])]
    #                             if t.sale == True and line.price_subtotal >= 1000:
    #                                 recs = self.env['account.tax'].search([('name','=','GST 18%')])
    #                                 if recs:
    #                                     for r in recs:
    #                                         line.tax_id = [(6,0,[r.id])]
    #                 record_sale = self.env['account.fiscal.position'].search([('sale','=','False')])
    #                 if record_sale:
    #                     for si in record_sale:
    #                         if l.fiscal_position_id.sale == False:
    #                             if l.fiscal_position_id.sale == False and line.price_subtotal < 1000:
    #                                 tax = self.env['account.tax'].search([('name','=','IGST 5%')])
    #                                 if tax:
    #                                     for s in tax:
    #                                         line.tax_id = [(6,0,[s.id])]
    #                             if l.fiscal_position_id.sale == False and line.price_subtotal >= 1000:
    #                                 taxs = self.env['account.tax'].search([('name','=','IGST 18%')])
    #                                 if taxs:
    #                                     for r in taxs:
    #                                         line.tax_id = [(6,0,[r.id])]




class ProductTemplate(models.Model):
    _inherit = "product.template"
    product_class = fields.Selection([
        ('premium', 'Premium'),
        ('non_premium', 'Non-Premium')], string='Product Class')
    barcode = fields.Char('Internal Barcode', related='product_variant_ids.barcode', required=True,readonly=False)
    vendor_barcode = fields.Char(string='Vendor Barcode')

    list_price = fields.Float(required=True)


class AccountFiscalPosition(models.Model):
    _inherit ='account.fiscal.position'

    sale = fields.Boolean(string='Sale')



