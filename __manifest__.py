# Archivo de metadatos que describe el módulo
{
    'name': 'Desoft Prueba',
    'version': '1.0', # Incrementando segun implementaciones
    'summary': 'Módulo prueba base para extensiones en Desoft',
    'description': 'Este es un módulo vacío para preparar adaptaciones a normativas cubanas en contabilidad y facturación.',
    'category': 'Tools',
    'author': 'A113E',
    'depends': ['base'],  # Dependencia básica
    'data': [
      # Seguridad primero

      # Vistas
      # Kanbam primero

      # Vistas regulares
      'views/partner_views.xml'

      # Demo
    ],  # Archivos XML a cargar
    'installable': True,
    'auto_install': False,
}