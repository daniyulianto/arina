# -*- coding: utf-8 -*-
{
    'name': "HR Job for Ratecard and Quota",

    'summary': """
        HR Job for Ratecard and Quota""",

    'description': """
        To generate No of Ratecard and Quota
    """,

    'author': "PT Arkana Solusi Bisnis",
    'website': "http://www.arkana.co.id",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': '',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'asb_ratecard', 'asb_quota'],

    # always loaded
    'data': [
        'views/hr_job_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'qweb': [
        
    ],
}
