# -*- coding: utf-8 -*-
{
    'name': "Vehicle Details",

    'summary': """
        Product Template Custom Fields """,

    'description': """
        This module adds custom fields to the inventory product Model and a new tab to the Product template form view
    """,

    'author': "Hyperthink Systems Kenya",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Hidden',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock', 'product'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/vehicle_details_assets.xml',
        'views/vehicle_details_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
}
