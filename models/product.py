from odoo import fields,models

class ProductTemplates(models.Model):
  _inherit = 'product.template' # Extender modelo
  
  # Campo Boolean
  esta_regulado = fields.Boolean(
    string='Regulado en Cuba',
    help='Indica si el producto está regulado por normativas cubanas (ej. precios controlados)'
  )