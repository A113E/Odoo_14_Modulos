# -*- coding: utf-8 -*-
{
    'name': 'Library Management',
    
    'version': '14.0.1.0.0',
    
    'summary': 'Sistema completo de gestión de biblioteca corporativa',
    
    'description': """
        Library Management System
        =========================
        
        Sistema profesional para gestión de bibliotecas empresariales.
        
        Funcionalidades Principales:
        ----------------------------
        * Gestión de catálogo de libros
        * Control de préstamos y devoluciones
        * Sistema de reservas
        * Historial de lecturas por usuario
        * Reportes estadísticos
        * Notificaciones automáticas
        
        Casos de Uso:
        -------------
        - Bibliotecas corporativas
        - Centros educativos
        - Gestión de recursos documentales
        
        Módulo desarrollado con fines educativos para aprender
        desarrollo profesional en Odoo 14.
    """,
    
    'author': 'A113E',
    'website': 'https://github.com/A113E',
    'category': 'Productivity',
    'license': 'LGPL-3',
    
    # Dependencias
    'depends': [
        'base',      # Módulo base (modelos fundamentales como res.partner)
        'mail',      # Sistema de mensajería y chatter
    ],
    
    # Archivos de datos (por ahora vacío, lo llenaremos en clases futuras)
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/menu_views.xml',
    ],
    
    # Configuración
    'application': True,      # Es una App principal
    'installable': True,      # Se puede instalar
    'auto_install': False,    # No se instala automáticamente
    'sequence': 10,           # Orden en el listado
    
    # Metadatos visuales
    'images': [],
}