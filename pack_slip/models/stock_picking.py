from odoo import models, fields, api
from datetime import date

class DraftReset(models.Model):
    _inherit = 'stock.picking'
    _description = 'Pack Print'


    def get_package_group(self):
        list1 = []
        for lines in self.move_line_ids_without_package:
            list1.append(lines.result_package_id)
        package_group = list(set(list1))

        return package_group


class StockQuantsPackage(models.Model):
    _inherit = 'stock.quant.package'
    _order = 'sequence,name'

    sequence = fields.Integer("Sequence", default=1, help="Gives the sequence order")

    @api.model
    def create(self, vals):
        if vals.get('sequence', 1) == 1:
            vals['sequence'] = self.env['ir.sequence'].next_by_code('package.sequence') or 1       

        result = super(StockQuantsPackage, self).create(vals)       

        return result