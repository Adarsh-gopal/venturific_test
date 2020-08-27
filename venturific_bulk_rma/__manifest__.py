# -*- coding: utf-8 -*-
{
    'name': "venturific_bulk_rma",

    'summary': """
        Recieving back the sold products in bulk to warehouse using barcode scan """,

    'description': """
        Long description of module's purpose
    """,

    'author': "Prixgen Tech Solutions Pvt Ltd",
    'website': "http://www.prixgen.com",
    'category': 'Uncategorized',
    'depends': ['bi_rma'],
    'version': '13.0.0.6',

    'data': [
        'wizards/picking_wizard.xml',
        'security/ir.model.access.csv',
        'data/bulk_rma_sequence.xml',
        'views/bulk_rma_views.xml',
        'views/rma_config.xml',
    ],

}
