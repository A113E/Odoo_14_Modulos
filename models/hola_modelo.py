# Inicializador del paquete Models
# -*- coding: utf-8 -*-

from odoo import api, fields, models

# Clase Principal
# Todos los modelos en Odoo heredan de models.Model
# Esto permite:
# Persistencia automática en base de datos
# ORM (Mapeo Objeto-Relacional)
# Métodos CRUD (Create, Read, Update, Delete)
class HolaModelo(models.Model):
  # Nombre técnico del Modelo
  # Debe de ser único
  _name = 'hola.mundo' # Snake convierte el punto en guión bajo

  # Descripción amigable (Opcional)
  _description = 'Modelo Hola Mundo'

  # Campos
  # Campos Char
  nombre = fields.Char(
    string='Nombre',
    required=True,
    help='Nombre del usuario'
  )

  descripcion = fields.Text(
    string='Descripción',
    help='Descripción detallada'
  )

  # Campos numéricos
  edad = fields.Integer(
    string='Edad',
    help='Edad en años'
  )

  altura = fields.Float(
    string='Altura (m)',
    digits=(3,2), # 3 digitos totales, 2 decimales
    help='Altura en metros'
  )

  # Campos fecha
  fecha_nacimiento = fields.Date(
    help='Fecha de nacimiento'
  )

  fecha_registro = fields.Datetime(
    string='Fecha de registro',
    default = lambda self: fields.Datetime.now(), # Función reutilizable para calcular la fecha y hora actual
    help='Fecha y hora actual'
  )

  # Campos booleanos
  esta_activo = fields.Boolean(
    string='Está activo',
    default=True
  )

  # Campos selección
  estado = fields.Selection(
    selection=[
      ('borrador', 'Borrador'),
      ('revisado', 'Revisado'),
      ('aprobado', 'Aprobado'),
      ('archivado', 'Archivado')
    ],
    string='Estado',
    default='borrador',
    help='Estado del registro'
  )

  # Campos calculados/computados
  anio_nacimiento = fields.Integer(
    string='Año de nacimiento',
    compute='_compute_anio_nacimiento',
    store=False, # No se guarda en la BD
    help='Año de nacimiento calculado'
  )

  @api.depends('fecha_nacimiento')
  def _compute_anio_nacimiento(self):
    """Calcula el Año de Nacimiento a partir de la fecha"""
    for record in self:
      if record.fecha_nacimiento:
        record.anio_nacimiento = record.fecha_nacimiento.year # Obtiene solo el año
      else:
        record.anio_nacimiento = 0
  
  # Métodos de acción 
  # Guardar registro
  def action_guardar(self):
    """Método de ejemplo para guardar"""
    # self.ensure_one() asegura que solo haya un registro
    message = f'Registro {self.nombre} guardado exitosamente!'

    # Retornar una acción de notificación
    return {
      'type': 'ir.actions.client',
      'tag': 'display_notification',
      'params': {
        'title': 'Guardado exitoso',
        'message': message,
        'sticky': False,
        'type': 'success',
      }
    }