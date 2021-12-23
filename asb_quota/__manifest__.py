# -*- coding: utf-8 -*-
{
    'name': "Quota",

    'summary': """
        Quota Module""",

    'description': """
        Quota Module
    """,

    'author': "PT Arkana Solusi Digital",
    'website': "http://www.arkana.co.id",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': '',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'asb_ratecard', 'hr'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/sequence_data_views.xml',
        'views/quota_views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'qweb': [
        'static/src/xml/quota_dashboard_views.xml'
    ],
}
