{
    'name': 'Venturific Discount',
    'version': '13.6',
    'category': 'Sales Discount',
    'depends': ['sale','sale_coupon','product','base'],
    'data': [
        #'security/sale_security.xml',
        'views/discount.xml',
        'wizard/sale_discount.xml',
    ],
    'installable': True,
    'auto_install': False
}