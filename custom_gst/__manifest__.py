{
    'name': 'Venturific GST',
    'version': '13.6',
    'category': 'Sales GST',
    'depends': ['sale','sale_coupon','product','base','account','l10n_it_edi','stock','hsn_master','custom_discount'],
    'data': [
        #'security/sale_security.xml',
        'views/gst.xml',
        'views/config_setting.xml',
    ],
    'installable': True,
    'auto_install': False
}