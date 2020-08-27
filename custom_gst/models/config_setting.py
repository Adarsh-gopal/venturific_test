# -*- coding: utf-8 -*-
from odoo import models, fields,api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    tax_computation_margin_default = fields.Float(
        'Tax Computation Margin',
        config_parameter='sale.default_tax_computation_margin',
        help='Enter the margin price to compute tax after discount.')