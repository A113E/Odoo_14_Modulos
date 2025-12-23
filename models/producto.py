# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError
import re # Para expresiones regulares

# Modelo
class Producto(models.Model):
  """Modelo para la Gestión de Productos"""
  _name = 'gestion.producto'
  _description = 'Producto del catálogo'
  _order = 'codigo ASC' # orden por defecto
  

  # Campos
  # Char
  name = fields.Char(
    string='Nombre del producto',
    required=True,
    index=True, # Indice en BD para búsquedas rápidas
    copy=True, # Se copia al duplicar registro
    trim=True, # Elimina espacios al inicio y final
    translate=False, # Si se puede traducir (MultiIdiomas)
    help='Nombre del producto - Mínimo 3 caracteres',
    size=100 # Longitud máxima en BD
  )

  codigo = fields.Char(
    string='Código SKU',
    required=True,
    index=True,
    copy=False, # No se puede copiar al duplicar (único)
    readonly=False, # Pero si se puede hacer con estado
    help='Código único de stock (SKU). Formato: PROD-00001',
    default=lambda self: self._generar_codigo_sku() # Función lambda que llama a la acción
  )

  # Integer
  cantidad_stock = fields.Integer(
    string='Cantidad en stock',
    default=0,
    help='Cantidad disponible en inventario',
    readonly=False,
    store=True, # Se guarda en la BD
    group_operator='sum' # En agrupaciones, suma los valores
  )

  vida_util_meses = fields.Integer(
    string='Vida útil en meses',
    default=12,
    help='Vida útil estimada en meses',
    readonly=False
  )

  # Float
  precio_compra = fields.Float(
    string='Precio de la compra',
    digits='Product Price', # Precisión predefinida en Odoo para precios
    help='Precio estandar en el que se compra el producto (son IVA)',
    default=0.0
  )

  precio_venta = fields.Float(
    string='Precio de venta del producto',
    digits='Product Price',
    help='Precio al que vendemos el producto (sin IVA)',
    default=0.0
  )

  peso_kg = fields.Float(
    string='Peso del producto',
    digits='6,3', # 6 digitos totales . 3 decimales (999.999)
    help='Peso del producto en Kgs',
    default=0.0
  )

  # Textos descriptivos
  descripcion = fields.Text(
    string='Descripcion detallada',
    help='Descripción completa del producto, características, usos, etc.'
  )

  # Date
  fecha_creacion = fields.Datetime(
    string='Fecha de Creación',
    default=lambda self: fields.Datetime.now(),
    readonly=True # No puede editarse desde el formulario
  )

  # Boolean
  esta_activo = fields.Boolean(
    string='Activo',
    default=True,
    help='Indica si el producto está activo en el catalogo'
  )

  # Métodos 
  # Internos _ no deben ser llamados desde la UI
  # Métodos CHAR
  @api.model
  def _generar_codigo_sku(self):
    """Genarar Código automático"""
    # Busca el último código usado
    ultimo_producto = self.search([], order='codigo desc', limit=1) # Método del ORM de Odoo - Consulta la base de datos - Devuelve varios registros - [] Domain sin filtros - Devuelve descendente - limit a un resultado

    if ultimo_producto and ultimo_producto.codigo:
      # Extraer número del último código
      import re
      match = re.search(r'PROD-(\d+)', ultimo_producto.codigo)
      if match:
        ultimo_numero = int(match.group(1))
        nuevo_numero = ultimo_numero + 1
      else:
        nuevo_numero = 1
    else:
      nuevo_numero = 1
    # Formatear 0 a la izquierda: PROD-00001
    return f'PROD-{nuevo_numero:05d}'
  
  # Validaciones
  # Validar el nombre
  @api.constrains('name')
  def _check_longitud_nombre(self):
    """Validar que el nombre tenga al menos 3 caracteres"""
    for record in self:
      if len(record.name or '') < 3:
        raise ValidationError(
          _('El nombre del producto debe de tener al menos 3 caracteres')  # _ marca el textp como traducible - Parte del sistema i18n de Odoo
        )
  
  # Validar el codigo
  @api.constrains('codigo')
  def _check_codigo_formato(self):
    """Validar el formato del Código SKU"""
    for record in self: # Odoo siempre trabaja con recordsets (Obligatorio en constrains)
      if record.codigo:
        # Verificar formato 
        if not re.match(r'^PROD-\d{5}$', record.codigo):
          raise ValidationError(
            _('Formato de Código Sku inválido: Use: PROD-00001')
          )
        # Verificar unicidad excluyendo el registro actual
        existentes = self.search([
          ('codigo', '=', record.codigo), # Busca registros con el mismo código 
          ('id','!=', record.id) # Evita que el propio registro se detecte a si mismo
        ])
        if existentes:
          raise ValidationError(
            # Bloque la acción - Muestra el codigo duplicado 
            _('El código SKU %s ya existe. Debe de ser único') % record.codigo # Regla de negocio fuerte
          )
        
  # Validar la cantidad del stock
  @api.constrains('cantidad_stock')
  def _check_cantidad_stock(self):
    """Valida que la cantidad de stock no sea negativa"""
    for record in self:
      if record.cantidad_stock < 0:
        raise ValidationError(
          _('La cantidad en stock no puede ser negativa.')
        )
  
  # Validar precio compra y precio de venta
  @api.constrains('precio_compra', 'precio_venta')
  def _check_precios(self):
    """Valida que los precios sean positivos"""
    for record in self:
      if record.precio_compra < 0:
        raise ValidationError(
          _('El precio de compra no puede ser negativo')
        )
      if record.precio_venta < 0:
        raise ValidationError(
          _('El precio de venta no puede ser negativo')
        )
      # Validar que sean lógicos
      if record.precio_venta > 0 and record.precio_compra > record.precio_venta:
        # Advertencia
        # En producción puede ser error
        pass # Genera un log aquí
  
  # Validar peso
  @api.constrains('peso_kg')
  def _check_peso_kg(self):
    """Validar que el peso sea lógico"""
    for record in self:
      if record.peso_kg < 0:
        raise ValidationError(
          _('El peso no puede ser negativo')
        )
      if record.peso_kg > 10000:
        raise ValidationError(
          _('El peso no puede exceder de 10000 toneladas. Revise el peso')
        )
  
  # Métodos de Acción básico
  # No llevan _, son pensados para botones xml etc.
  # Método write (editar) para activar el producto
  def action_activar(self):
    """Activa el producto"""
    self.write({'esta_activo': True})
    return True # Si el metodo no abre ventanas, devuelve vistas, no notificaciones, se ponse return True
  
  # Método write (editar) para desactivar el producto
  def action_desactivar(self):
    """Desactiva el producto"""
    self.write({'esta_activo': False})
    return True
  
  # Método para ajustar el stock del producto
  def action_ajustar_stock(self, cantidad):
    """Ajustar el stock"""
    self.cantidad_stock += cantidad
    return True
