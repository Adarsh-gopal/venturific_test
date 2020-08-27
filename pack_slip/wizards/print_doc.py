import uuid

from odoo import api, fields, models, _
from odoo.fields import Date
from odoo.exceptions import ValidationError


class PrintDocWiz(models.TransientModel):
    _name = 'pack.print.wiz'
    _description = 'Print Package Based On Box Id'

    # @api.model
    # def default_get(self, fields):
    #     result = super(PrintDocWiz, self).default_get(fields)
    #     model = self.env.context.get('active_model')
    #     order_id = self.env.context.get('active_id')
    #     sale_order = self.env['sale.order'].sudo().browse(order_id)

    #     result['sale_order'] = sale_order.id
    #     # result['box'] = sale_order.box.id

    #     return result
    # sale_order = fields.Many2one('sale.order')

    def get_domain(self):
        order_id = self.env.context.get('active_id')
        sale_order = self.env['sale.order'].sudo().browse(order_id)
        list1 = []
        for lines in sale_order.order_line:
            list1.append(lines.boxs.id)
        package_group = list(set(list1))

        return package_group

    box = fields.Many2one('stock.quant.package',string='Box',domain=lambda self: [('id','in',self.get_domain())])



    def print_pack_slip(self):
        active_id = self.env.context.get('active_id')
        order = self.env['sale.order'].browse(self.env.context.get('active_id'))
        data = {
        'pack_id': self.box.id,
        'active_id': active_id,
        'order_id':order.id,
        'order_line': order.order_line,
        }
        return self.env.ref('pack_slip.sale_order_report_pack_slip_single').report_action(self, data=data)
        # return self.env.ref('pack_slip.sale_order_report_pack_slip').report_action(self)



