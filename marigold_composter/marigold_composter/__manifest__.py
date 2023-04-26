# -*- coding: utf-8 -*-
{
    'name': "Marigold Composter",

    'summary': """
        Hassle-free composting for a better tomorrow""",

    'description': """
        We work towards a cleaner and greener future by providing effective, affordable and sustainable waste solutions.
    """,

    'author': "Marigold",
    'website': "http://marigoldcomposters.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account','sale','sale_management'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/contacts_views.xml',
        'views/tracker_views.xml',
        'views/snippets.xml',
    ],
    'assets': { 
        'web.assets_frontend': [
            'marigold_composter/static/js/snippets.js'
        ]},
    
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}