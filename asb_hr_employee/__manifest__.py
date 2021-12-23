# -*- coding: utf-8 -*-
{
    'name': "Custom Module Employee",

    'summary': """
        Custom Module Employee""",

    'description': """
        To Custom Module Employee For Arina
    """,

    'author': "PT Arkana Solusi Bisnis",
    'website': "http://www.arkana.co.id",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': '',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hr', 'asb_hr_recruitment', 'asb_ratecard', 'asb_quota'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/hr_employee.xml',
        'views/hr_employee_blacklist.xml',
        'views/hr_employee_change.xml',
        'views/hr_employee_resign.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'qweb': [

    ],
}
