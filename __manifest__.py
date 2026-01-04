# -*- coding: utf-8 -*-
{
    # ========== IDENTIFICACIÓN ==========
    'name': 'Library Management System',
    
    'version': '14.0.1.0.0',
    
    'summary': 'Sistema profesional de gestión de biblioteca corporativa',
    
    'description': """
        Library Management System - Professional Edition
        ================================================
        
        Sistema completo para gestión de bibliotecas empresariales,
        desarrollado con mejores prácticas de Odoo.
        
        Funcionalidades Principales:
        ----------------------------
        * **Gestión de Catálogo**
          - Control completo de libros y recursos
          - Categorización por género, autor, editorial
          - ISBN y búsqueda avanzada
          
        * **Control de Préstamos**
          - Sistema de préstamos y devoluciones
          - Historial completo por usuario
          - Notificaciones de vencimiento
          - Renovaciones automáticas
          
        * **Gestión de Usuarios**
          - Perfiles de lectores
          - Historial de lectura
          - Estadísticas personalizadas
          
        * **Reportes y Análisis**
          - Dashboard ejecutivo
          - Reportes de préstamos activos
          - Estadísticas de uso
          - Análisis de popularidad
          
        * **Sistema de Reservas**
          - Cola de espera para libros prestados
          - Notificaciones de disponibilidad
          
        Casos de Uso:
        -------------
        ✓ Bibliotecas corporativas de empresas
        ✓ Centros educativos y universidades
        ✓ Centros de documentación
        ✓ Gestión de recursos compartidos
        
        Tecnologías:
        ------------
        - Odoo 14 Community/Enterprise
        - Python 3.7+
        - PostgreSQL 10+
        
        Autor:
        ------
        Desarrollado por [Tu Nombre] como proyecto educativo
        para dominar el desarrollo profesional en Odoo 14.
        
        Soporte:
        --------
        Para consultas: soporte@tuempresa.com
        Documentación: https://docs.tuempresa.com/library
    """,
    
    # ========== AUTORÍA ==========
    'author': 'A113E',
    'maintainer': 'Alberto',
    'website': 'https://github.com/A113E',
    'support': 'amg11amg2@gmail.com',
    
    # ========== CLASIFICACIÓN ==========
    'category': 'Productivity/Documents',
    'license': 'LGPL-3',
    
    # ========== DEPENDENCIAS ==========
    'depends': [
        'base',           # Módulo base (res.partner, ir.model, etc.)
        'mail',           # Chatter, actividades, notificaciones
        'portal',         # Portal de clientes (para futura integración)
    ],
    
    # ========== DATOS ==========
    'data': [
        # Seguridad (siempre primero)
        # 'security/library_security.xml',
        # 'security/ir.model.access.csv',
        
        # Vistas
        # 'views/menu_views.xml',
        # 'views/library_book_views.xml',
        
        # Datos iniciales
        # 'data/library_data.xml',
        
        # Reportes
        # 'reports/library_report_templates.xml',
    ],
    
    # Datos de demostración
    'demo': [
        # 'demo/library_demo.xml',
    ],
    
    # ========== RECURSOS WEB ==========
    'assets': {
        # 'web.assets_backend': [
        #     'library_management/static/src/js/library_widget.js',
        #     'library_management/static/src/css/library_styles.css',
        # ],
    },
    
    # ========== CONFIGURACIÓN ==========
    'application': True,       # Es una App principal
    'installable': True,       # Puede instalarse
    'auto_install': False,     # No se autoinstala
    'sequence': 10,            # Orden en lista de apps
    
    # ========== RECURSOS VISUALES ==========
    'images': [
        
        # 'static/description/banner.png',
        # 'static/description/screenshot1.png',
    ],
    
    # ========== METADATOS COMERCIALES (Opcional) ==========
    # 'price': 0.00,
    # 'currency': 'EUR',
    # 'live_test_url': 'https://demo.library.com',
}