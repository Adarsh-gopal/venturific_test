# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import SUPERUSER_ID, http, tools, _
from odoo import models, fields, api, _
from odoo.http import request
from datetime import datetime
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.exceptions import UserError, AccessError
import json

class bi_website_rma(CustomerPortal):

	def _prepare_portal_layout_values(self):
		values = super(bi_website_rma, self)._prepare_portal_layout_values()
		partner = request.env.user.partner_id

		Rma = request.env['rma.main']
		
		rma_count = Rma.search_count([
			('partner', '=', partner.commercial_partner_id.id),
			('state', 'in', ['draft', 'confirmed', 'approved', 'return'])
		])

		values.update({
			'rma_count': rma_count,
		})
		return values


	@http.route('/rma/return/<model("stock.picking"):picking>',type='http', auth="public", website=True)
	def product_rma_return(self,picking,**kw):
		context = dict(request.env.context or {})
		context.update(active_id=picking.id)
		Sales = request.env['sale.order'].sudo().search([('id','=',kw['sale_order_id'])])

		picking = request.env['stock.picking'].sudo().browse(picking.id)

		delivery_order = []
		for item in picking:
			delivery_order.append(item)

		lines = []
		for line in picking.move_ids_without_package:
			lines.append(line)

		return request.render("bi_website_rma.product_return_rma",{'sales_order':Sales,'picking':picking,'lines':lines})


	@http.route(['/my/rma', '/my/rma/page/<int:page>'], type='http', auth="user", website=True)
	def portal_my_rma(self, page=1, date_begin=None, date_end=None, **kw):
		values = self._prepare_portal_layout_values()
		partner = request.env.user.partner_id
		RmaOrder = request.env['rma.main']
		

		domain = []
		
		archive_groups = self._get_archive_groups('rma.main', domain)
		if date_begin and date_end:
			domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]
		
		# count for pager
		rma_count = RmaOrder.search_count(domain)
		# pager
		pager = request.website.pager(
			url="/my/rma",
			url_args={'date_begin': date_begin, 'date_end': date_end},
			total=rma_count,
			step=self._items_per_page
		)
		# content according to pager and archive selected
		rma = RmaOrder.search(domain, limit=self._items_per_page, offset=pager['offset'])
		values.update({
			'date': date_begin,
			'rma': rma,
			'page_name': 'rma',
			'pager': pager,
			'archive_groups': archive_groups,
			'default_url': '/my/rma',
		})
		return request.render("bi_website_rma.portal_my_rma", values)

	
	@http.route('/thankyou', type='json', auth="public", methods=['POST'], website=True)
	def thanks(self,sale_order,delivery_order,ord_line,ret_qty,rma_reason,ret_dict,**post):
		if sale_order:

			selected_line_dict = {}
			order_list = []
			delivery_order = int(delivery_order)
			user_brw = request.env['res.users'].sudo().browse(request._uid)
			rma_order_obj = request.env['rma.main']
			s_order = request.env['sale.order'].sudo().search([('id','=',sale_order)])
			d_order = request.env['stock.picking'].sudo().search([('id','=',delivery_order)])

			for o_line in d_order.move_ids_without_package:
				for selected_line in ret_dict:
					if int(o_line.id) == int(selected_line['ord_line']):
						order_dict = {
							'product_id':o_line.product_id.id,
							'delivery_qty':o_line.quantity_done,
							'return_qty':selected_line['ret_qty'],
							'reason' : selected_line['rma_reason'],
							}
						order_list.append((0,0,order_dict))
			vals = {
				'partner': user_brw.partner_id.id,
				'email': user_brw.partner_id.email,
				'phone': user_brw.partner_id.phone,
				'date': datetime.now(), 
				'sale_order': s_order.id, 
				'rma_line_ids' : order_list,
				'responsible': s_order.user_id.id,
				'delivery_order': d_order.id,
				'sales_channel': s_order.team_id.id, 
			}

			rma_order_create = rma_order_obj.sudo().create(vals)
			name = rma_order_create

			request.session['rma_id'] = name.id
			request.session['rma_name'] = name.name
			return {
				'rma_id' : name.id,
				'rma_name':name.name
			}
		else:
			return False

	@http.route(['/rma/thankyou'], type='http', auth="public", website=True)
	def website_rma(self,name=None,**post):
		if post:
			return request.render("bi_website_rma.rma_thankyou")
		else:
			return request.render("bi_website_rma.rma_failed")


	@http.route(['/rma/view/detail/<model("rma.main"):rma_order>'],type='http',auth="portal",website=True)
	def rma_view(self, rma_order, category='', search='', **kwargs):
		context = dict(request.env.context or {})
		rma_obj = request.env['rma.main']
		context.update(active_id=rma_order.id)
		rma_data_list = []
		rma_data = rma_obj.browse(int(rma_order))
		
		for items in rma_data:
			rma_data_list.append(items)
			
		return http.request.render('bi_website_rma.portal_my_rma_detail_view',{
			'rma_data_list': rma_order
		})