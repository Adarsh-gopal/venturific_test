# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Website Image 360',
    'summary': 'This module helps to rotate the product image in 360 dimension view',
    'website': 'http://www.aktivsoftware.com',
    'license': 'AGPL-3',
    'author': 'Aktiv Software',
    'category': 'Website',
    'version': '13.0.1.0.0',
    'depends': ['website_sale'],
    'data': [
        'data/example_data_view.xml',
        'views/website_image_360.xml',
        'views/template.xml',
        'security/ir.model.access.csv',
    ],
    'images': ['static/description/banner.jpg'],
    'installable': True,
}
