{
    'name': "Project Tracking",
    'version': '14.0.1.0.0',
    'author': "A113E",
    'category': 'Services/Project',
    'summary': "Tracking projects and tasks",
    'description': """
    Project Tracking
    =========================
    Features:
    - Projects
    - Tasks
    """,
    'depends': ['base'],
    'data': [
      # Security
      'security/ir.model.access.csv',
      # Vistas
      'views/project_views.xml',
      'views/task_views.xml',
      'views/menu_views.xml'  ,
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}