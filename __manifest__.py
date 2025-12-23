{
    'name': "Gestión de Productos Básica",
    'version': '14.0.1.0.0',
    'author': "A113E",
    'website': "",
    'category': 'Inventory',
    'summary': "Gestión básica de catálogo de productos",
    'description': """
        Módulo para gestión básica de productos.
        Incluye:
        - Información básica de productos
        - Control de precios y existencias
        - Categorización simple
        
        Desarrollado por Alberto Mártir González.
    """,
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',

        'views/producto_views.xml',
        'views/menu_views.xml',

        'data/producto_demo.xml',
    ],
    'demo': [
        'data/producto_demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}