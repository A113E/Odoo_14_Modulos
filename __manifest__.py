# RAÍZ DEL PROYECTO

{
  'name': "Hola Mundo",
  'version': "14.0.1.0.0",
  'author': "A113E",
  'website': "",
  'category': "Tools",
  'summary': "Mi primer Módulo - Hola Mundo",
  'description': """
      Este es mi primer Módulo
      Estoy comenzando las bases del desarrollo
  """,
  'depends': ['base'],
  'data': [
    # Aquí van los archivos xml
    # ORDEN IMPORTANTE: Seguridad primero, luego vistas
    # Seguridad
    'security/ir.model.access.csv',
    # Vistas
    'views/menus_views.xml',
  ],
  'demo': [
    # Datos de demostración (Opcional)
  ],
  'installable': True, # Si puede instalarse
  'application': True, # Si es una aplicación
  'auto_install': False, # Si se instala automáticamente
}