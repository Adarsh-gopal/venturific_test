from odoo import models, fields, api,_
from datetime import date
from odoo.exceptions import Warning, UserError

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    boxs = fields.Many2one('stock.quant.package',string='Box')

