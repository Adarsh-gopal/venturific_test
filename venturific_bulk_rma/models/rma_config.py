from odoo import fields, models, api, _
from datetime import date, time, datetime
from odoo.exceptions import UserError,Warning

class RmaConfig(models.Model):

    _inherit = 'rma.config'


    @api.model 
    def default_get(self, fields): 
        result = super(RmaConfig, self).default_get(fields)

        config_id = self.sudo().search([],order='id desc', limit=1)
        result.update({ 'b2b_source_picking_type_id': config_id.b2b_source_picking_type_id.id, 
                        'b2b_destination_picking_type_id': config_id.b2b_destination_picking_type_id.id, 
                        'refund_days': config_id.refund_days, 
                        }) 
        return result


    refund_days = fields.Integer(store=True)