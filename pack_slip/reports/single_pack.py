from collections import OrderedDict

from odoo import api, models, _
from odoo.fields import Datetime
from odoo.exceptions import UserError


class SinglePackPrint(models.AbstractModel):
    _name = 'report.pack_slip.sale_order_report_single_packslip_print'
    _description = 'Single Pack Print Abstract Model'


    def _get_report_data(self, data):
        pack_id = self.env['stock.quant.package'].browse(data['pack_id'])
        order = self.env['sale.order'].browse(data['active_id'])

        return {
            'pack_id': pack_id,
            'order': order,
        }

    @api.model
    def _get_report_values(self, docids, data=None):
        return {'report_data': self._get_report_data(data)}