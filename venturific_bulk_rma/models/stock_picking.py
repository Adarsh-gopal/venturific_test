from odoo import fields, models, api, _
from datetime import date, time, datetime
from odoo.exceptions import UserError,Warning,ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero, float_round

class StockMove(models.Model):
    _inherit = "stock.move"

    bulk_rma_line_id = fields.Many2one('bulk.rma.lines')


class BulkRmaStockPicking(models.Model):

    _inherit = "stock.picking"

    bulkrma_id = fields.Many2one('bulk.rma',string='Bulk RMA ID')

class RefundAccInvoiceBulkRMA(models.Model):

    _inherit = 'account.move'

    bulkrma_id = fields.Many2one('bulk.rma',string='Bulk RMA ID')

class BulkRmaSaleOrder(models.Model):

    _inherit = 'sale.order'

    bulkrma_id = fields.Many2one('bulk.rma',string='Bulk RMA ID')
