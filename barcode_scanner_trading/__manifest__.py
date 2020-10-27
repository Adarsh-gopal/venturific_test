# -*- coding: utf-8 -*-
{
    "name": "Barcode Scanner for Trading",

    'author': 'Prixgen Tech Solutions Pvt. Ltd.',
    'company': 'Prixgen Tech Solutions Pvt. Ltd.',
    'website': 'https://www.prixgen.com',  
        
    'version': '13.0.0.2',
        
    "category": "Extra Tools",

    "summary": """barcode scanner app odoo, package all in one barcode, sale barcode scanner, purchase in barcode module, invoice in barcode, inventory barcode, stock barcode, bom using barcode, scrap in barcode, multi barcode of one product""",   
        
    'description': """
     """,
    
    "depends": [
        
                'purchase',
                'sale_management',
                'barcodes',
                'account',
                'stock',
                'sale',
                'product_qrcode_generator_trading',
                
                ],
    
    "data": [
        
    "views/res_config_settings_views.xml",
    "views/sale_view.xml",
    "views/purchase_view.xml",
    "views/stock_view.xml",
    "views/account_view.xml",
    "views/assets.xml",
    
    
    ],    
    'images': ['static/description/background.png',],            
    
    "installable": True,    
    "application": True,    
    "autoinstall": False,
      
}
