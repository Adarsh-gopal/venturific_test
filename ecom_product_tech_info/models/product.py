from odoo import api, exceptions, fields, models, _

class ProductTemplate(models.Model):
    _inherit = "product.template"


    product_tech_line_ids = fields.One2many('product.tech.line','product_tem_id')

class ProductTemplate(models.Model):
    _inherit = "product.product"

    product_tech_line_ids = fields.One2many('product.tech.line','product_id')


class TechDetails(models.Model):
    _name = 'product.tech.line'
    _description = "Contains Each product technical details"


    name = fields.Char()
    product_id = fields.Many2one('product.product')
    product_tem_id = fields.Many2one('product.template')
    description = fields.Text()