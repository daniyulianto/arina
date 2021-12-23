# -*- coding: utf-8 -*-
{
    'name': "Arina Config",

    'summary': """
        Arina Config For Master Data""",

    'description': """
        Arina Config For Master Data
    """,

    'author': "PT Arkana Solusi Digital",
    'website': "http://www.arkana.co.id",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': '',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/hr_employee_education.xml',
        'views/regional.xml',
        'views/representative_office.xml',
        'views/res_partner.xml',
        'views/res_partner_bank.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
