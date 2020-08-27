from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.tools.translate import _
from odoo.exceptions import UserError

class HsnMaster(models.Model):
	_name = 'hsn.master'

	name = fields.Char(string='HSN/SAC Code')
	z_description = fields.Char(string='HSN/SAC Description')
	zzz_vendor_taxes = fields.Many2many('account.tax','vendor_taxes_rel','vend_id','tax_id',string='Vendor Taxes',domain=[('type_tax_use', '=', 'purchase')])
	zzz_customer_taxes = fields.Many2many('account.tax','customer_taxes_rel','cust_id','tax_id',string='Customer Taxes',domain=[('type_tax_use', '=', 'sale')])
	tax_compute_after_discount = fields.Boolean('Tax Compute After Discount')
	tax_differenitation = fields.Boolean('Tax Differnitation')
	# net_sale_price_is_greater_than = fields.Float(string='Net Sales Price is >=')
	# net_sale_price_is_lesser_than = fields.Float(string='Net Sales Price is <')
	# applicable_sales_tax = fields.Many2one('account.tax',string='Applicable Intra State Tax')
	# applicable_sale_tax = fields.Many2one('account.tax',string='Applicable Intra State Tax')
	# applicable_inter_tax = fields.Many2one('account.tax',string='Applicable Inter State Tax')
	# applicable_inter_state_tax = fields.Many2one('account.tax',string='Applicable Inter State Tax')


class ProductTemplate(models.Model):
	_inherit = "product.template"

	l10n_in_hsn_code = fields.Many2one('hsn.master',string="HSN/SAC Code", help="Harmonized System Nomenclature/Services Accounting Code")

	@api.onchange('l10n_in_hsn_code')
	def _Onchange_hsn(self):
		for line in self:
			line.l10n_in_hsn_description = line.l10n_in_hsn_code.z_description
			line.taxes_id = line.l10n_in_hsn_code.zzz_customer_taxes
			line.supplier_taxes_id = line.l10n_in_hsn_code.zzz_vendor_taxes