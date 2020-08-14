from odoo import models, fields, api,_
from datetime import date
from odoo.exceptions import Warning, UserError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    customer_code = fields.Char()


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    customer_code = fields.Char(related='partner_id.customer_code',store=True)
    box = fields.Many2one('stock.quant.package',string='Box')


    def get_package_group(self):
        list1 = []
        for lines in self.order_line:
            list1.append(lines.boxs)
        package_group = list(set(list1))

        return package_group


    def action_confirm(self):
        check = super(SaleOrder, self).action_confirm()
        for l in self:
            for s in l.order_line:
                rec = self.env['stock.picking'].search([('sale_id','=',l.id)])
                for r in rec:
                    for line in rec.move_line_ids_without_package:
                        if s.product_id.id == line.product_id.id:
                            line.result_package_id = s.boxs.id

        return check

    def get_next_box(self):
        next_box_sequence = self.box.sequence + 1
        if self.box:
            data = {
            'pack_id': self.box.id,
            'active_id': self.id,
            }
            if next_box_sequence:
                pack = self.env['stock.quant.package'].search([('sequence','=',next_box_sequence)],limit=1)
                self.write({'box':pack.id})
            return self.env.ref('pack_slip.sale_order_report_pack_slip_single').report_action(self, data=data)
        else:
            if next_box_sequence:
                pack = self.env['stock.quant.package'].search([('sequence','=',next_box_sequence)],limit=1)
                self.write({'box':pack.id})
            raise Warning(_('There is no Box Selected For Print'))



class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    boxs = fields.Many2one('stock.quant.package',string='Box')

    @api.onchange('product_id')
    def Onchange_box(self):
        for l in self:
            for line in l.order_id:
                l.boxs = line.box.id


    def _prepare_invoice_line(self):
        res = super(SaleOrderLine, self)._prepare_invoice_line()
        res.update({'boxs': self.boxs.id})
        return res
