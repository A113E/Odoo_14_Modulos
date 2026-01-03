from odoo import api,fields,models

class ProjectMilestone(models.Model):
  """Modelo para hito"""
  _name = 'project.milestone'
  _description = 'Milestone'
  
  # Campos básicos
  name = fields.Char(
    string='Name',
    copy=True, # se copia el valor al duplicar
    help='Milestone Name',
    required=True,
    trim=True, # Quitar espacios al inicio/fin
    translate=True # Se puede traducir (multilenguaje)
  )
  
  state = fields.Selection([
    ('planned','Planned'),
    ('in_progress','In-progress'),
    ('completed','Completed'),
    ('delayed','Delayed')
  ], string='State', default='planned')
  
  is_critical = fields.Boolean(
    string='Is critical',
    help='Is critical?',
    default=False
  )
  
  estimated_date = fields.Date(
    string='Estimated Date'
  )
  
  comentarys = fields.Text(
    string='Comentarys',
    help='Details and comentarys'
  )