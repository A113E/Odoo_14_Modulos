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