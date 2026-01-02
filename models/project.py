from odoo import api,fields,models
from odoo.exceptions import ValidationError
from odoo import _

class ProjectProject(models.Model):
  """Modelo para projectos"""
  _name = 'project.project' # Nombre técnico único
  _description = 'Project' # Descripción humana
  
  # Campos básicos
  # Campos de texto
  name = fields.Char(
    string='Project Name', # Etiqueta para usuarios
    required=True, # Obligatorio
    help='Name of the Project' # Tooltip de ayuda
  )
  
  # Campos fecha
  start_date = fields.Date(
    string='Start Date'
  )
  
  end_date = fields.Date(
    string='End Date'
  )
  
  # Campos de selección
  state = fields.Selection([
    ('draft','Draft'),
    ('in_progress','In progress'),
    ('done','Done'),
    ('cancel','Cancelled')
  ], string='State',
     help='State of the project',
     default='draft'
                           )
  
  # Campos numéricos
  budget = fields.Float(
    string='Budget',
    help='Budget of the project',
    digits=(6,2)
  )
  
  actual_cost = fields.Float(
    string='Actual cost',
    help='Actual cost of the project',
    digits=(6,2)
  )
  
  remaining_budget = fields.Float(
    string='Remaining Budget',
    compute='_compute_remaining_budget',
    store=True # se guarda en bd
  )
  
  # Campos boolean
  is_late = fields.Boolean(
    string='Is late?',
    compute='_compute_is_late', # Método computado (se calcula, no guarda *por ahora*)
    store=True
  )
  
  # Campos relacionales
  customer_id = fields.Many2one(
    'res.partner',
    string='Customer',
    help='Customer for this project'
  )
  
  # Métodos
  # Computados (calculan valor de campos)
  def _compute_is_late(self):
    today = fields.Date.today()
    for project in self:
        project.is_late = bool(
            project.end_date and project.end_date < today
        )
  
  @api.depends('budget','actual_cost')
  def _compute_remaining_budget(self):
    """Calcula la diferencia presupuestal"""
    for project in self:
        project.remaining_budget = (project.budget or 0.0) - (project.actual_cost or 0.0)
      
        
  # Validaciones
  @api.constrains('actual_cost')
  def _check_actual_cost(self):
    """Verifica que el costo actual no sea mayor que el presupuestado"""
    for project in self:
      if project.budget:
        if project.actual_cost > project.budget * 1.5:
          raise ValidationError(
            _('El costo actual no puede superar el presupuestado')
          )