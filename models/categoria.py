# -*- coding: utf-8 -*-
from odoo import api,fields,models
from odoo.exceptions import ValidationError
import re
from odoo import _

class Categoria(models.Model):
  """Modelo jerárquico para las categorias para los productos"""
  _name = 'categoria.producto'
  _description = 'Categoría de producto'
  _order = 'sequence,name' # Ordenara por sequencia y luego por nombre
  _parent_store = True # Para jerarquías (siempre debe ir acompañado de parent_id y parent_path)

  # Campos de texto
  name = fields.Char(
    string='Nombre de Categoría',
    required=True,
    index=True, # Búsqueda rápida
    help='Nombre de la categoría (ej: "Electrónica", "Alimentos" etc)',
    translate=True # Se puede traducir a otros idiomas
  )

  codigo = fields.Char(
    string='Código de Categoría',
    help='Código único de la categoría (ej: "CAT-001", "ALIM", etc.)',
    index=True,
    required=True,
    default=lambda self: self._generar_codigo() # Función reutilizable para llamar a generar codigo
  )

  descripcion = fields.Text(
    string='Descripción',
    help='Descripción detallada de la categoría'
  )
  
  # Campos Booleanos
  active = fields.Boolean(
    string='Activo',
    default=True,
    help='Si no está activa, la categoría no estará disponible'
  )

  # Campos Numéricos
  sequence = fields.Integer(
    string='Secuencia',
    default=10,
    help='Orden de aparición (menor numero = primero)'
  )

  # Campos relacionales
  producto_ids = fields.One2many(
    'gestion.producto',
    'categoria_id',
    string='Productos',
    help='Productos pertenecientes a esta categoría'
  )

  # Campos para jerarquía
  # Categoria superior
  parent_id = fields.Many2one(
    'categoria.producto',
    string='Categoria padre',
    help='Categoría superior en la jerarquía',
    index=True,
    ondelete='cascade', # Si se elimina padre, se eliminan hijos
  )

  # Guarda la estructura jerarquica (para parent_store)
  parent_path = fields.Char(
    index=True
  )

  # Subcategorias
  child_ids = fields.One2many(
    'categoria.producto',
    'parent_id',
    string='Subcategorias',
    help='Categorias hijas de la categoria superior'
  )

  # Campos computados
  cantidad_productos = fields.Integer(
    string='Cantidad de productos',
    help='Cantidad de productos en esta categoria',
    store=True, # se guarda en bd
    compute='_compute_cantidad_productos'
  )

  # Metodos internos (No se llaman desde la UI)
  # Generar codigo automatico
  @api.model
  def _generar_codigo(self):
    """Generar codigo automatico"""
    # Busca la ultima categoia
    ultima_categoria = self.search([], order='id desc', limit=1)

    if ultima_categoria and ultima_categoria.codigo:
      # Extraer numero del codigo
      match = re.search(f'CAT-(\d+)', ultima_categoria.codigo)
      if match:
        ultimo_numero = int(match.group(1))
        nuevo_numero = ultimo_numero + 1
      else:
        nuevo_numero = 1
    else:
      nuevo_numero = 1
    
    return f'CAT-{nuevo_numero:03d}' # CAT-001, CAT-002 ...
  
  # Metodos computados
  # Metodo que determina la cantidad de productos (Se crea despues)
  @api.depends('producto_ids')
  def _compute_cantidad_productos(self):
    """Calcular cantidad de productos de una categoria"""
    # Conectar luego
    for categoria in self:
      categoria.cantidad_productos = len(categoria.producto_ids)
  
  # Validaciones
  # Evita que una categoria padre no puede ser hija
  @api.constrains('parent_id')
  def _check_parent_recursion(self):
    """Evita recursion infinita en jerarquia (categoria padre no puede ser hija)"""
    for categoria in self:
      if categoria.parent_id:
        # Obtener todos los ancestros
        ancestros = categoria.parent_id
        while ancestros:
          if ancestros == categoria:
            raise ValidationError(
              _('No se puede crear una jerarquia circular. Una categoria no puede ser padre de sus ancestros')
            )
          ancestros = ancestros.parent_id
  
  # Verifica que el nombre sea unico
  @api.constrains('name')
  def _check_nombre_unico(self):
    """Valida que el nombre sea unico por categoria padre"""
    for categoria in self:
      if categoria.name:
        domains = [
          ('name','=',categoria.name),
          ('parent_id','=',categoria.parent_id.id),
          ('id','!=',categoria.id)
        ]
        existentes = self.search(domains)
        if existentes:
          raise ValidationError(
            _('Ya existe una categoria con el nombre "%s" en el mismo nivel') % categoria.name # Regla de negocio fuerte
          )
  
  # Métodos de acción
  # Método para ver productos de una categoria
  def action_ver_productos(self):
    """Acción para ver productos de una categoria"""
    return {
      'type':'ir.actions.act_window',
      'name': f'Productos en {self.name}',
      'res_model': 'gestion.producto',
      'view_mode': 'tree,form',
      'domain': [('categoria_id', '=', self.id)],
      'context': {'default_categoria_id': self.id}
    }