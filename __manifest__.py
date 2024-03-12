# -*- coding: utf-8 -*-
{
    'name': "odoo_basico",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account'],

    # always loaded
    'data': [
        'views/informacion.xml',
        'views/suceso.xml',
        'views/pedido.xml',
        'views/lineapedido.xml',
        'views/persoa.xml',
        'views/templates.xml',
        'reports/report_header.xml',
        'reports/report_informacion.xml',
        'accions_planificadas/accion_planificada.xml',
        'security/xestion_usuarios.xml',
        'views/menu.xml',
        'security/ir.model.access.csv',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
