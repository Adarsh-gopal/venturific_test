# -*- coding: utf-8 -*-
{
    'name': 'sh_barcode_scanner',
    'version': '13.0.0.9',
    'category': 'Inventory',
    'author': 'Prixgen Tech Solutions Pvt. Ltd.',
    'company': 'Prixgen Tech Solutions Pvt. Ltd.',
    'website': 'https://www.prixgen.com',
    
    "depends": [
        
                'purchase',
                'sale_management',
                'barcodes',
                'account',
                'stock',
                # 'mrp',
                'sale',
                'sh_product_qrcode_generator',
                
                ],
    
    "data": [
        
    "views/res_config_settings_views.xml",
    "views/sale_view.xml",
    "views/purchase_view.xml",
    "views/stock_view.xml",
    "views/account_view.xml",
    # "views/mrp_view.xml",
    "views/assets.xml",
    
    
    ],    
    'images': ['static/description/background.png',],            
    
    "installable": True,    
    "application": True,    
    "autoinstall": False,
    "price": 35,
    "currency": "EUR"        
}
