# -*- coding: utf-8 -*-
{
    'sequence': -1,
    'name': "Rest API",
    'summary': 'Restful Api Service',
    'description': 'API for integration GSI Mobile Apps',
    'author': 'PT. Arkana Solusi Digital, ' 'Rizqi <rizqi@arkana.co.id>',
    'website': "http://www.arkana.co.id",
    'category': 'Backend',
    'version': '14.0.0',
    'license': 'OPL-1',
    'depends': [
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/view_refresh_token.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': True,
}
