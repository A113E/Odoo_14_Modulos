from odoo import api,fields,models

class ProjectTask(models.Model):
  """Modelo para tarea"""
  _name = 'project.task'
  _description = 'Task'
  
  # Campos básicos
  # Campos de texto
  name = fields.Char(
    string='Task Name',
    help='Name of the Task',
    required=True
  )
  
  description = fields.Text(
    string='Description',
    help='Description of the task'
  )
  
  # Campos numéricos
  estimated_hours = fields.Float(
    string='Estimated hours'
  )
  
  actual_hours = fields.Float(
    string='Actual hours'
  )
  
  # Calculado
  hour_difference = fields.Float(
    string='Hour Difference',
    compute='_compute_hour_difference', # Método computado
    store=True # Este si se guarda en BD 
  )
  
  # Campos relacionales
  # Many2one -> Muchas tareas en un projecto
  project_id = fields.Many2one(
    'project.project',
    string='Project',
    required=True,
    ondelete='cascade' # Si se borra el proyecto, se borran sus tareas
  )
  
  # Many2one -> Muchas tareas para un empleado
  user_id = fields.Many2one(
    'res.users',
    string='Assigned to'
  )
  
  # Métodos 
  # Computados
  @api.depends('estimated_hours','actual_hours')
  def _compute_hour_difference(self):
    """Calcula la diferencia de horas"""
    for task in self:
      task.hour_difference = (task.actual_hours or 0.0) - (task.estimated_hours or 0.0)
  