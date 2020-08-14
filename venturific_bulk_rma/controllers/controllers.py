# -*- coding: utf-8 -*-
# from odoo import http


# class VenturificBulkRma(http.Controller):
#     @http.route('/venturific_bulk_rma/venturific_bulk_rma/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/venturific_bulk_rma/venturific_bulk_rma/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('venturific_bulk_rma.listing', {
#             'root': '/venturific_bulk_rma/venturific_bulk_rma',
#             'objects': http.request.env['venturific_bulk_rma.venturific_bulk_rma'].search([]),
#         })

#     @http.route('/venturific_bulk_rma/venturific_bulk_rma/objects/<model("venturific_bulk_rma.venturific_bulk_rma"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('venturific_bulk_rma.object', {
#             'object': obj
#         })
