# -*- coding: utf-8 -*-
from odoo import api,fields,models

class LibraryBook(models.Model):
  """Modelo libro"""
  _name = 'library.book',
  _description = 'Library Book'
  
  name = fields.Char(
    string='Title',
    help='Titulo completo del libro',
    required=True
  )
  
  isbn = fields.Char(
    string='ISBN',
    help='Código isbn del libro (10 0 13 caracteres)'
  )
  
  publisher = fields.Char(
    string='Publisher',
    help='Editorial'
  )
  
  publication_year = fields.Integer(
    string='Publication Year',
    help='Año en que se publicó el libro'
  )
  
  pages = fields.Integer(
    string='Pages',
    help='Total de páginas del libro'
  )
  
  notes = fields.Text(
    string='Notes',
    help='Notas adicionales del libro'
  )