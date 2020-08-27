from odoo import api, fields, models, _
import pdb

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

 
    total_tax = fields.Float(string='Tax Amount',store=True,track_visibility='always',compute='compute_taxable')

    @api.depends('price_tax')
    def compute_taxable(self):
        for l in self:
            l.total_tax = l.price_tax

   


class SaleOrder(models.Model):
    _inherit = "sale.order"


    def tax_inc(self):
        tax_margin_value = float(self.env['ir.config_parameter'].sudo().get_param('sale.default_tax_computation_margin'))
        for l in self:
            for line in l.order_line:
                if line.product_id.l10n_in_hsn_code.tax_compute_after_discount == True:
                    if line.price_subtotal < tax_margin_value or line.price_subtotal > tax_margin_value:
                        line.tax_id = False
                        record = self.env['account.fiscal.position'].search([('sale','=','True')])
                        if record:
                            for t in record:
                                #pdb.set_trace()
                                if l.fiscal_position_id.sale == True and line.product_id.l10n_in_hsn_code.tax_differenitation == True:
                                    if t.sale == True and line.price_subtotal < tax_margin_value:
                                        rec = self.env['account.tax'].search([('name','=','GST 5%'),('type_tax_use','=','sale')])
                                        if rec:
                                            for s in rec:
                                                line.tax_id = [(6,0,[s.id])]
                                    if t.sale == True and line.price_subtotal >= tax_margin_value:
                                        recs = self.env['account.tax'].search([('name','=','GST 18%'),('type_tax_use','=','sale')])
                                        if recs:
                                            for r in recs:
                                                line.tax_id = [(6,0,[r.id])]
                                if l.fiscal_position_id.sale == True and line.product_id.l10n_in_hsn_code.tax_differenitation == False:
                                    if t.sale == True and line.price_subtotal < tax_margin_value:
                                        rec = self.env['account.tax'].search([('name','=','GST 5%'),('type_tax_use','=','sale')])
                                        if rec:
                                            for s in rec:
                                                line.tax_id = [(6,0,[s.id])]
                                    if t.sale == True and line.price_subtotal >= tax_margin_value:
                                        recs = self.env['account.tax'].search([('name','=','GST 12%'),('type_tax_use','=','sale')])
                                        if recs:
                                            for r in recs:
                                                line.tax_id = [(6,0,[r.id])]
                        record_sale = self.env['account.fiscal.position'].search([('sale','=','False')])
                        if record_sale:
                            for si in record_sale:
                                if l.fiscal_position_id.sale == False and line.product_id.l10n_in_hsn_code.tax_differenitation == True:
                                    if l.fiscal_position_id.sale == False and line.price_subtotal < tax_margin_value:
                                        tax = self.env['account.tax'].search([('name','=','IGST 5%'),('type_tax_use','=','sale')])
                                        if tax:
                                            for s in tax:
                                                line.tax_id = [(6,0,[s.id])]
                                    if l.fiscal_position_id.sale == False and line.price_subtotal >= tax_margin_value:
                                        taxs = self.env['account.tax'].search([('name','=','IGST 18%'),('type_tax_use','=','sale')])
                                        if taxs:
                                            for r in taxs:
                                                line.tax_id = [(6,0,[r.id])]
                                if l.fiscal_position_id.sale == False and line.product_id.l10n_in_hsn_code.tax_differenitation == False:
                                    if l.fiscal_position_id.sale == False and line.price_subtotal < tax_margin_value:
                                        tax = self.env['account.tax'].search([('name','=','IGST 5%'),('type_tax_use','=','sale')])
                                        if tax:
                                            for s in tax:
                                                line.tax_id = [(6,0,[s.id])]
                                    if l.fiscal_position_id.sale == False and line.price_subtotal >= tax_margin_value:
                                        taxs = self.env['account.tax'].search([('name','=','IGST 12%'),('type_tax_use','=','sale')])
                                        if taxs:
                                            for r in taxs:
                                                line.tax_id = [(6,0,[r.id])]
                # if l.fiscal_position_id.id == 3:
                #     if line.product_id.l10n_in_hsn_code.tax_compute_after_discount == True:
                #         if line.price_subtotal >= line.product_id.l10n_in_hsn_code.net_sale_price_is_greater_than:
                #             line.tax_id = False
                #             if line.price_subtotal >= line.product_id.l10n_in_hsn_code.net_sale_price_is_greater_than:
                #                 line.tax_id = [(6,0,[line.product_id.l10n_in_hsn_code.applicable_sales_tax.id])]
                #         if line.price_subtotal < line.product_id.l10n_in_hsn_code.net_sale_price_is_lesser_than:
                #             line.tax_id = False
                #             if line.price_subtotal < line.product_id.l10n_in_hsn_code.net_sale_price_is_lesser_than:
                #                 line.tax_id = [(6,0,[line.product_id.l10n_in_hsn_code.applicable_sale_tax.id])]
                # if l.fiscal_position_id.id == 1:
                #     if line.product_id.l10n_in_hsn_code.tax_compute_after_discount == True:
                #         if line.price_subtotal >= line.product_id.l10n_in_hsn_code.net_sale_price_is_greater_than:
                #             line.tax_id = False
                #             if line.price_subtotal >= line.product_id.l10n_in_hsn_code.net_sale_price_is_greater_than:
                #                 line.tax_id = [(6,0,[line.product_id.l10n_in_hsn_code.applicable_inter_tax.id])]
                #         if line.price_subtotal < line.product_id.l10n_in_hsn_code.net_sale_price_is_lesser_than:
                #             line.tax_id = False
                #             if line.price_subtotal < line.product_id.l10n_in_hsn_code.net_sale_price_is_lesser_than:
                #                 line.tax_id = [(6,0,[line.product_id.l10n_in_hsn_code.applicable_inter_state_tax.id])]

                