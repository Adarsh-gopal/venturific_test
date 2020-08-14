{
    'name': 'Product Brand in Sale',
    'version': '13.0.0.2',
    'category': 'Sales',
    'summary': 'Product Brand in Sales',
    'description': 'Product Brand in Sales,brand,sale, odoo13',
    'author': 'Prixgen Tech Solutions',
    'company': 'Prixgen Tech Solutions',
    'maintainer': 'Prixgen Tech Solutions',

    'website': 'https://www.prixgen.com',
    'depends': ['sale_management','stock'],
    'data': [
        'views/brand_views.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,

}
