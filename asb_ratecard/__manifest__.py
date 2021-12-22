# -*- coding: utf-8 -*-
{
    'name': "Ratecard",

    'summary': """
        Ratecard Module""",

    'description': """
        Ratecard Module
    """,

    'author': "PT Arkana Solusi Digital",
    'website': "http://www.arkana.co.id",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': '',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'hr', 'web'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/sequence_data_views.xml',
        'views/ratecard_views.xml',
        'views/sale_order_views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'qweb': [
        'static/src/xml/ratecard_dashboard_views.xml'
    ],
}
