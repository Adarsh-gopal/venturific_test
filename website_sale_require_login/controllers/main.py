from odoo import http
from odoo.addons.website_sale.controllers.main import WebsiteSale


class RequireLoginToCheckout(WebsiteSale):
    @http.route(auth="user")
    def checkout(self, **post):
        return super(RequireLoginToCheckout, self).checkout(**post)
