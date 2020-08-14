{
    'name': 'Product Brand in eCommerce',
    'version': '13.0.0.2',
    'category': 'eCommerce',
    'summary': 'Product Brand in eCommerce',
    'description': 'Product Brand in eCommerce',
    'author': 'Prixgen  Tech Solutions',
    'company': 'Prixgen  Tech Solutions',
    'maintainer': 'Prixgen  Tech Solutions',
    'images': ['static/description/banner.png'],
    'website': 'https://www.prixgen.com',
    'depends': ['product_brand_sale','website_sale','website','web'],
    'data': [
        'views/template.xml',
        'views/assets.xml',
        'views/snippets.xml',
    ],
    'qweb': ['static/src/xml/*.xml'],
    'installable': True,
    'auto_install': False,
    'application': False,

}
