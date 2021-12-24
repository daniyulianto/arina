# -*- coding: utf-8 -*-
{
    'name': "Custome HR Recuitment",

    'summary': """
        HR Recuitment Module Test""",

    'description': """
        HR Ratecard Module For PT Arina Multi Karya
    """,

    'author': "Rizqi - PT Arkana Solusi Bisnis",
    'website': "http://www.arkana.co.id",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Technical',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hr_recruitment','website_hr_recruitment', 'asb_ratecard', 'asb_quota'],

    # always loaded
    'data': [
        'security/hr_recruitment_security.xml',
        'security/ir.model.access.csv',
        'views/hr_recruitment.xml',
        'views/website_hr_recruitment_templates.xml',
        'views/hr_template_pkwt.xml',
        'data/ir_sequence.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
