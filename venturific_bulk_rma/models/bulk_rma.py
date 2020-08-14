from odoo import fields, models, api, _
from datetime import date, time, datetime
from odoo.exceptions import UserError,Warning,ValidationError

class RmaBulk(models.Model):

    _name = 'bulk.rma'
    _description = "process RMA for bulk orders"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    def _get_default_days_diff(self):
        config_id = self.env['rma.config'].sudo().search([],order='id desc', limit=1)
        return config_id.refund_days if config_id else None

    name = fields.Char('Name',default=lambda self: _('New'),store=True)
    date = fields.Datetime('Date',default=datetime.now() ,required=True)
    rma_note = fields.Text('RMA Note')
    priority = fields.Selection([('0','Low'), ('1','Normal'), ('2','High')], 'Priority')
    rma_line_ids = fields.One2many('bulk.rma.lines','bulk_rma_id','RMA Lines',store=True)
    reject_reason = fields.Char('Reject Reason')
    partner = fields.Many2one('res.partner','Customer', store=True)
    refund_days = fields.Integer(default=_get_default_days_diff, store=True)

    in_delivery_count = fields.Integer(string='Incoming Orders', compute='_compute_incoming_picking_ids')
    # out_delivery_count = fields.Integer(string='Outgoing Orders', compute='_compute_outgoing_picking_ids')
    refund_inv_count = fields.Integer(string='Refund Invoice', compute='_compute_refund_inv_ids')
    # sale_order_count = fields.Integer(string='Sale Order',compute='_compute_sale_order_ids')

    company_id = fields.Many2one('res.company',string="Company",default=lambda self: self.env.user.company_id)
        
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Validate GRN'),
        ('processing', 'Credit Note'),
        ('close', 'Closed'),
        ('reject','Rejected'),
        ], string='Status', default='draft')

    mark_all = fields.Boolean( string="Select All", store=True)


    @api.onchange('mark_all')
    def select_all(self):
        if self.mark_all == True:
            for lines in self.rma_line_ids:
                lines.return_approve =True
            # self.rma_line_ids.mapped().write({'return_approve':True})
        else:
            for lines in self.rma_line_ids:
                lines.return_approve =False

    def _compute_incoming_picking_ids(self):
        for order in self:
            stock_picking_ids = self.env['stock.picking'].search([('bulkrma_id','=',order.id)])
            order.in_delivery_count = len(stock_picking_ids)

    def _compute_refund_inv_ids(self):
        for inv in self:
            refund_inv_ids = self.env['account.move'].search([('bulkrma_id','=',inv.id)])
            inv.refund_inv_count = len(refund_inv_ids)

    def action_view_refund_invoice(self): 
        self.ensure_one()
        return { 
            'name': 'Refund Invoice', 
            'type': 'ir.actions.act_window', 
            'view_mode': 'tree,form', 
            'res_model': 'account.move', 
            'domain': [('bulkrma_id','=',self.id)], 
        }




    @api.model
    def create(self,vals):
        vals.update({
            'name': self.env['ir.sequence'].next_by_code('bulk.rma'),
        })
        return super(RmaBulk, self).create(vals)

    def action_move_to_draft(self):
        self.write({'state':'draft'})
        return

    def action_close(self):
        self.write({'state':'close'})
        return

    # def action_approve(self):
    #     self.write({'state':'approved'})
    #     return

    @api.constrains('rma_line_ids')
    def _check_exist_product_in_line(self):
      for rec in self:
          exist_product_list = []
          for line in rec.rma_line_ids:
             if line.barcode in exist_product_list:
                raise ValidationError(_('Product should be one per line.'))
             exist_product_list.append(line.barcode)


    def validate_grn(self):

        self.write({'state':'approved'})

        stock_picking_obj = self.env['stock.picking']

        # for r in self.rma_line_ids:
        #     if(r.action == 'replace'):
        #         r.show_prod_setting = True
        orders = []
        for line in self.rma_line_ids:
            if line.return_approve:
                orders.append(line.delivery_order)
        order_list = list(set(orders))

        if order_list:
            for rec in order_list:
                config_id = self.env['rma.config'].sudo().search([],order='id desc', limit=1)

                vals= {
                    'bulkrma_id' : self.id,
                    'partner_id' : self.partner.id,
                    'location_id' : config_id.b2b_source_picking_type_id.default_location_src_id.id,
                    'location_dest_id' : config_id.b2b_source_picking_type_id.default_location_dest_id.id,
                    'origin' :  _("Return of %s") % rec.name,
                    'scheduled_date' : self.date,
                    'picking_type_code' : 'incoming',
                    'picking_type_id' : config_id.b2b_source_picking_type_id.id,

                }
                stock_picking = stock_picking_obj.create(vals)            
                stock_move_obj = self.env['stock.move']
                for lines in self.rma_line_ids:
                    # print(lines.delivery_order.id,rec.id)
                    if lines.delivery_order.id == rec.id and lines.return_approve == True:      
                        product_vals = {
                            'name' : lines.product_id.name,
                            'product_id' : lines.product_id.id,
                            'product_uom_qty' : float(lines.delivered_qty),
                            'product_uom' : lines.product_id.uom_id.id,
                            'picking_id' : stock_picking.id,
                            'location_id' : config_id.b2b_source_picking_type_id.default_location_src_id.id,
                            'location_dest_id' : config_id.b2b_source_picking_type_id.default_location_dest_id.id,
                            'picking_type_id' : config_id.b2b_source_picking_type_id.id,
                            'bulk_rma_line_id':lines.id,
                        }
                        stock_move_obj.create(product_vals)
        else:
            raise Warning(_('No record found in line'))     

        return

    def generate_credit_note(self):

        # self.write({'state':'approved'})

        account_move_obj = self.env['account.move']
        account = []
        for line in self.rma_line_ids:
            if line.grn_ref:
                account.append(line.invoice_number)
        account_invoice_list = list(set(account))



        if account_invoice_list:
            for rec in account_invoice_list:


                vals= {
                    'bulkrma_id' : self.id,
                    'partner_id' : rec.partner_id.id,
                    'type' : 'out_refund',
                    'ref' :  _("Reversal of  %s") % rec.name,
                    'reversed_entry_id' : rec.id,
                    'state':'draft',
                    'invoice_origin':self.name,

                }
                account_move = account_move_obj.create(vals)            
                account_move_line_obj = self.env['account.move.line']
                for lines in self.rma_line_ids:
                    if lines.invoice_number.id == rec.id and lines.grn_ref:
                        move_rec = account_move_obj.search([('id','=',lines.invoice_number.id)],limit=1)
                        for each_l in move_rec.invoice_line_ids:
                            if each_l.product_id.id == lines.product_id.id:
                                prod_price = each_l.price_unit
                        account = lines.product_id.property_account_income_id or lines.product_id.categ_id.property_account_income_categ_id
        
                        if not account:
                            raise UserError(_('Please define income account for this product: "%s" (id:%d) - or for its category: "%s".') %
                            (lines.product_id.name, lines.product_id.id, lines.product_id.categ_id.name))

                        product_vals = {
                            'name' : lines.product_id.name,
                            'product_id' : lines.product_id.id,
                            'quantity' : lines.delivered_qty,
                            'product_uom_id' : lines.product_id.uom_id.id,
                            'account_id' : account.id,
                            'price_unit':prod_price,
                            
                        }
                        account_move.write({'invoice_line_ids': [(0,0,product_vals)] })
        else:
            raise Warning(_('No record found in line'))     

        return

    def action_view_receipt(self): 
        self.ensure_one()
        return { 
            'name': 'Picking', 
            'type': 'ir.actions.act_window', 
            'view_mode': 'tree,form', 
            'res_model': 'stock.picking', 
            'domain': [('bulkrma_id','=',self.id)], 
        }



class BulkRmaLines(models.Model):

    _name = 'bulk.rma.lines'
    _description = 'ram lines for bulk process'

    def _get_default_days_diff(self):
        config_id = self.env['rma.config'].sudo().search([],order='id desc', limit=1)
        return config_id.refund_days if config_id else None

    # def _get_default_partner(self):
    #     # for l in self:
    #     for line in self.bulk_rma_id:
    #         return  line.partner.id



    bulk_rma_id = fields.Many2one('bulk.rma','RMA Id')
    barcode = fields.Char('Barcode')
    product_id = fields.Many2one('product.product','Product',compute="get_values",store=True)
    product_class = fields.Selection([('premium','Premium'),('non_premium','Non-Premium')],compute="get_values",store=True)
    partner = fields.Many2one('res.partner','Customer',compute='get_partner', store=True)
    return_date = fields.Datetime(default=datetime.now())
    delivery_order = fields.Many2one('stock.picking',compute="get_values",store=True)
    delivery_date = fields.Date(compute="get_values",store=True)
    invoice_number = fields.Many2one('account.move',compute="get_values",store=True)
    invoice_date = fields.Date(compute="get_values",store=True)
    delivered_qty = fields.Float(compute="get_values",store=True)
    num_of_days = fields.Integer('Number of Days \nfrom Invoice Date',compute="get_values", store=True)
    invoice_status = fields.Selection([('paid','Paid'),('not_paid','Not Paid')],default=None,compute="get_values",store=True)
    grn_ref = fields.Many2one('stock.picking','GRN Ref')
    # credit_note = fields.Boolean(store=True)
    return_approve = fields.Boolean( compute="get_values", store=True)
    sale_order = fields.Many2one('sale.order',compute="get_values",store=True)
    refund_days = fields.Integer(default=_get_default_days_diff, store=True)

    @api.depends('barcode')
    def get_partner(self):
        for l in self:
            for line in l.bulk_rma_id:
                l.partner = line.partner.id 


    @api.depends('barcode')
    def get_values(self):
        for lines in  self:
            if lines.barcode:
                products = self.env['product.product'].search([('barcode','=',lines.barcode)])
                lot = self.env['stock.production.lot'].search([('name','=',lines.barcode)])
                if products:
                    lines.product_id = products.id
                    lines.product_class = products.product_class
                    stock_move_line = self.env['stock.move.line'].search([('product_id','=',products.id),('reference','ilike','OUT')])
                    if stock_move_line:

                        lines.product_id= stock_move_line.product_id.id
                        lines.delivered_qty = stock_move_line.qty_done
                        lines.product_class = stock_move_line.product_id.product_class
                        lines.delivery_order = stock_move_line.picking_id.id
                        lines.delivery_date = stock_move_line.picking_id.date_done
                        if stock_move_line.picking_id.origin:
                            invoice = self.env['account.move'].search([('invoice_origin','=',stock_move_line.picking_id.origin)])
                            inv_list=[]
                            for each_invoice in invoice:
                                for each_line in each_invoice.invoice_line_ids:
                                    if each_line.product_id.id == stock_move_line.product_id.id:
                                        # inv_list.append(each_invoice)
                                        lines.invoice_number = each_invoice.id
                                        lines.invoice_date = each_invoice.invoice_date
                                        if lines.invoice_number.amount_residual > 0:
                                            lines.invoice_status='not_paid'
                                        elif lines.invoice_number.amount_residual == 0:
                                            lines.invoice_status='paid'
                                        else:
                                            lines.invoice_status = None
                                        break




                            sale_order = self.env['sale.order'].search([('name','=',stock_move_line.picking_id.origin)])
                            if sale_order:
                                lines.sale_order = sale_order.id
                            if lines.invoice_date:
                                lines.num_of_days = (date.today() - lines.invoice_date).days 

                            else:
                                lines.num_of_days = None
                            if lines.num_of_days !=None and lines.refund_days !=None:
                                if lines.num_of_days <= lines.refund_days:
                                    # lines.credit_note = True
                                    lines.return_approve = True
                                else:
                                    # lines.credit_note = False
                                    lines.return_approve = False
                    else:
                        raise UserError(_('Thers is no Delivery Order for this product'))
                elif lot:
                    stock_move_line = self.env['stock.move.line'].search([('lot_id','=',lot.id),('lot_name','=',None)])
                    if stock_move_line:

                        lines.product_id= stock_move_line.product_id.id
                        lines.delivered_qty = stock_move_line.qty_done
                        lines.product_class = stock_move_line.product_id.product_class
                        lines.delivery_order = stock_move_line.picking_id.id
                        lines.delivery_date = stock_move_line.picking_id.date_done
                        if stock_move_line.picking_id.origin:
                            invoice = self.env['account.move'].search([('invoice_origin','=',stock_move_line.picking_id.origin)])
                            inv_list=[]
                            for each_invoice in invoice:
                                for each_line in each_invoice.invoice_line_ids:
                                    if each_line.product_id.id == stock_move_line.product_id.id:
                                        # inv_list.append(each_invoice)
                                        lines.invoice_number = each_invoice.id
                                        lines.invoice_date = each_invoice.invoice_date
                                        if lines.invoice_number.amount_residual > 0:
                                            lines.invoice_status='not_paid'
                                        elif lines.invoice_number.amount_residual == 0:
                                            lines.invoice_status='paid'
                                        else:
                                            lines.invoice_status = None
                                        break




                            sale_order = self.env['sale.order'].search([('name','=',stock_move_line.picking_id.origin)])
                            if sale_order:
                                lines.sale_order = sale_order.id
                            if lines.invoice_date:
                                lines.num_of_days = (date.today() - lines.invoice_date).days 

                            else:
                                lines.num_of_days = None
                            if lines.num_of_days and lines.refund_days:
                                if lines.num_of_days < lines.refund_days:
                                    # lines.credit_note = True
                                    lines.return_approve = True
                                else:
                                    # lines.credit_note = False
                                    lines.return_approve = False
                    else:
                        raise UserError(_('There is no Delivery Order for this product'))

                else:
                    raise UserError(_('No Product found!'))


    # @api.depends('invoice_date')
    # def get_days_diff(self):
    #     for line in self:
    #         if line.invoice_date:
    #             line.num_of_days = (date.today() - line.invoice_date).days 

    #         else:
    #             line.num_of_days = None


    # @api.depends('num_of_days','refund_days')
    # def get_val(self):
    #     for rec in self:
    #         if rec.num_of_days and rec.refund_days:
    #             if rec.num_of_days <= rec.refund_days:
    #                 rec.return_approve = True
    #             else:
    #                 rec.return_approve = False
                    


    # @api.depends('invoice_number')
    # def get_status(self):
    #     for line in self:
    #         if line.invoice_number.amount_residual > 0:
    #             line.invoice_status='not_paid'
    #         elif line.invoice_number.amount_residual == 0:
    #             line.invoice_status='paid'
    #         else:
    #             line.invoice_status = None



    # @api.onchange('barcode')
    # def check_for_duplication(self):
    #     for line in self :
    #         barcodes = []
    #         if line.barcode not in barcodes:
    #             barcodes.append(line.barcode)
    #         else:
    #             raise UserError(_('Already Scanned'))

    #         print('*******************',barcodes)











    