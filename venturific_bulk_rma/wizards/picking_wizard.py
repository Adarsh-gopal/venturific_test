# -*- coding: utf-8 -*-

import logging
from odoo import models,_
from odoo.exceptions import UserError
import pdb

_logger = logging.getLogger(__name__)

class PickingValidate(models.TransientModel):
    _name = 'picking.order.vallidate'
    _description = "Wizard - Picking order vallidate"

    def validate(self):

        context = dict(self._context or {})
        pick = self.env['stock.picking'].browse(context.get('active_ids'))
        validate = pick.filtered(lambda x: x.state in ['draft','waiting','confirmed','assigned'])
        if not validate:
            raise UserError(_('There are no RMA Orders in the draft state to Validate.'))
        for rec in validate:
            rma_lines = [x.bulk_rma_line_id for x in rec.move_lines]
            if not rec.bulkrma_id:
                raise UserError(_('This is not RMA Process'))
            if rec.state == 'draft':
                rec.action_confirm()
                if rec.state != 'assigned':
                    rec.action_assign()
                    if rec.state != 'assigned':
                        raise UserError(_("Could not reserve all requested products. Please use the \'Mark as Todo\' button to handle the reservation manually."))
            for move in rec.move_lines.filtered(lambda m: m.state not in ['done', 'cancel']):
                for move_line in move.move_line_ids:
                    move_line.qty_done = move_line.product_uom_qty
            for rm in rma_lines:
                rm.write({'grn_ref':rec.id})
                    # move.bulk_rma_line_id.write({'grn_ref':rec.id})
            rec.bulkrma_id.write({'state':'processing'})
            if rec:
                rec.action_done()
        return {'type': 'ir.actions.act_window_close'}

