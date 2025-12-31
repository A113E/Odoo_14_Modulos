from odoo import fields,models

class ResPartner(models.Model):
  _inherit = 'res.partner' # Extender el modelo base
  # Acceso a res.partner y res.users

  # Campos básicos
  nit_cubano = fields.Char(
    string='NIT Cubano',
    help='Código de identificación fiscal según normativas cubanas'
  )