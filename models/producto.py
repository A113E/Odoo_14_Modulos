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

  es_fragil = fields.Boolean(
    string='Es fragil',
    default=False,
    help='El producto requiere manejo especial por fragilidad'
  )

  requiere_refrigeracion = fields.Boolean(
    string='Requiere Refrigeracion',
    default=False,
    help='El producto debe mantenerse refrigerado'
  )

  tiene_garantia = fields.Boolean(
    string='Tiene garantía',
    default=False,
    help='El producto incluye garantía del fabricante'
  )

  # Selection * Avanzado *
  estado = fields.Selection(
    selection = [
      ('borrador', 'Borrador'),
      ('en_revision', 'En revision'),
      ('aprobado', 'Aprobado'),
      ('rechazado', 'Rechazado'),
      ('archivado', 'Archivado')
    ], 
    string='Estado del producto',
    default='borrador',
    required=True,
    copy=False, # No copiar estado duplicado
    tracking=True, # Registrar cambios en chatter
    help='Estado actual en el flujo de aprobación del producto'
  )

  # Campos condicionales 
  # que aparecen segun el estado
  motivo_rechazo = fields.Text(
    string='Motivo del rechazo',
    help='Explicación detallada del rechazo del producto',
    copy=False # No copiar motivo duplicado
  )

  fecha_aprobacion = fields.Datetime(
    string='Fecha de aprobación',
    copy=False, # No copiar fecha en duplicados
    readonly=True
  )

  # Campos relacionales 
  # *DEPENDE DEL ESTADO* Cada producto puede ser aprobado por un usuario - un usuario puede aprobar varios productos
  aprobado_por = fields.Many2one(
    'res.users',
    string='Aprobado por',
    copy=False, # No copiar valor del campo al duplicar
    readonly=True # No modificable
  )

  # Depende del campo garantia
  duracion_garantia_mes = fields.Integer(
    string='Duración garantía (meses)',
    default=12,
    help='Duración de la garantía en meses',
    copy=False # no copiar el valor del campo al duplicar
  )

  # Depende del campo refrigeracion
  temperatura_refrigeracion = fields.Float(
    string='Temperatura Refrigeración (°C)',
    digits=('3,1'), # 3 digitos en total : 18.5
    help='Temperatura óptima de refrigeración',
    copy=False # no copiar el valor del campo al duplicar
  )

  # Depende del campo fragilidad
  instrucciones_fragilidad = fields.Text(
    string='Instrucciones fragilidad',
    help='Instrucciones específicas para manejo de producto frágil',
    copy=False # no copiar el valor del campo al duplicar
  )

  # Campos Dinámicos
  color_estado = fields.Integer(
    string='Color del estado',
    compute='compute_color_estado',
    store=False, # No se guarda en la BD
    help='Color para mostrar en la vista kanban'
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
  
  # Validaciones combinadas
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
    
  # Validar estado y precio_venta
  @api.constrains('estado','precio_venta')
  def _check_estado_precio(self):
    """Validar que productos aprobados tenga precio de venta"""
    for record in self:
      if record.estado == 'aprobado' and record.precio_venta < 0:
        raise ValidationError(
          _('Los productos aprobados deben de tener un precio de venta')
        )
  
  # Validar estado y motivo de rechazo
  @api.constrains('estado', 'motivo_rechazo')
  def _check_estado_motivo(self):
    """Validar que los productos rechazados tengan un motivo"""
    for record in self:
      if record.estado == 'rechazado' and not record.motivo_rechazo:
        raise ValidationError(
          _('Los productos rechazados deben de tener un motivo')
        )
      
  # Validar garantia y duracion de garantia
  @api.constrains('tiene_garantia','duracion_garantia_mes')
  def _check_garantia_duracion(self):
    """Validar duracion de garantia si tiene"""
    for record in self:
      if record.tiene_garantia and record.duracion_garantia_mes <= 0:
        raise ValidationError(
          _('La duración de la garantía debe ser mayor que 0')
        )
  
  # Validar refrigeracion y temperatura
  @api.constrains('requiere_refrigeracion', 'temperatura_refrigeracion')
  def _check_temperatura(self):
    """Validar la temperatura correcta"""
    for record in self:
      if record.requiere_refrigeracion:
        if not (-50 <= record.temperatura_refrigeracion <= 10):
          raise ValidationError(
            _('La temperatura de refrigeracion debe estar entre -50 y 10°C')
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
  
  # Método para cambiar el estado (Transiciones controladas)
  # Enviar a revisión
  def action_enviar_revision(self):
    """Enviar producto a revisión"""
    valid_states = ['borrador', 'rechazado']

    for record in self:
      if record.estado not in valid_states:
        raise ValidationError(
          _('Solo productos con estado: "Borrador" o "Rechazado" pueden enviarse a revisión')
        )
      
      # Cambiar el estado a revisión
      record.write({
        'estado': 'en_revision',
        'motivo_rechazo': False # Limpiar el motivo de rechazo si había
      })

    return True
  
  # Aceptar producto
  def action_aprobar(self):
    """Aprobar producto (Necesita precio de venta)"""
    valid_states = ['en_revision']

    for record in self:
      if record.estado not in valid_states:
        raise ValidationError(
          _('Solo productos con estado "En revisión" pueden aprobarse')
        )
      
      if record.precio_venta <= 0:
        raise ValidationError(
          _('Solo se pueden aprobar productos con precio de venta')
        )
      
      # Aprobar
      record.write({
        'estado': 'aprobado',
        'fecha_aprobacion': fields.Datetime.now(),
        'aprobado_por': self.env.user.id
      })
    
    return True
  
  # Rechazar producto
  def action_rechazar(self):
    """Rechazar producto (Necesita motivo)"""
    valid_states = ['aprobado', 'en_revision']

    for record in self:
      if record.estado not in valid_states:
        raise ValidationError(
          _('Solo se pueden rechazar productos aprobados o en revisión')
        )
      
      if not record.motivo_rechazo:
        raise ValidationError(
          _('Debe especificar un motivo')
        )
      
      # Rechazar producto
      record.write({
        'estado': 'rechazado'
      })
    
    return True
  
  # Archivar el producto
  def action_archivar(self):
    """Archivar producto"""
    valid_states = ['aprobado', 'rechazado']

    for record in self:
      if record.estado not in valid_states:
        raise ValidationError(
          _('Solo se pueden archivar productos aprobados o rechazados')
        )
      
      # Archivar productos
      record.write({
        'estado': 'archivado',
        'esta_activo': False # Lo desactiva
      })
    
    return True
  
  # Reactivar desde archivo
  def action_reactivar_producto_archivo(self):
    """Reactivar producto desde archivo a borrador"""
    for record in self:
      if record.estado != 'archivado':
        raise ValidationError(
          _('Solo productos archivados pueden reactivarse')
        )
      
      # Reactivar
      record.write({
        'estado': 'borrador',
        'esta_activo': True, # Activa el producto
        'motivo_rechazo': False
      })
    
    return True
  
  # Método para guardar von notificacion
  def action_guardar(self):
        """Método para el botón Guardar Cambios"""
        # self.ensure_one()  # Usar para asegurar que se guarde solo un registro
        
        # Validaciones adicionales antes de guardar
        if self.estado == 'aprobado' and self.precio_venta <= 0:
            raise ValidationError(
                _('Un producto aprobado debe tener precio de venta mayor a 0.')
            )
        
        message = f'Producto {self.name} guardado exitosamente!'
        
        # Mostrar notificación
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Guardado exitoso',
                'message': message,
                'sticky': False,
                'type': 'success',
                'next': {'type': 'ir.actions.act_window_close'},  # Cerrar wizard si hay
            }
        }
  
  # Métodos computados
  @api.depends('estado')
  def _compute_color_estado(self):
    """Asigna un color segun el estado"""
    colores = {
      'borrador': 0, # Gris
      'en_revision': 1, # Azul
      'aprobado': 10, # Verde
      'rechazado': 2, # Rojo
      'archivado': 3 # Morado
    }

    for record in self:
      record.color_estado = colores.get(record.estado, 0) # Gris por defecto
  
  # Métodos Onchange (Cambios en tiempos real)
  # Reset duracion si no tiene garantia
  @api.onchange('tiene_garantia')
  def _onchange_tiene_garantia(self):
    """Resetear duración de garantía si se desactiva garantia"""
    for record in self:
      if not record.tiene_garantia:
        record.duracion_garantia_mes = 0
  
  # Reset temperatura si no requiere refrigeracion
  @api.onchange('requiere_refrigeracion')
  def _onchange_requiere_refrigeracion(self):
    """Resetear temperatura si no requiere refrigeracion"""
    for record in self:
      if not record.requiere_refrigeracion:
        record.temperatura_refrigeracion = 0.0

  # Resetear instrucciones si no es fragil
  @api.onchange('es_fragil')
  def _onchange_es_fragil(self):
    """Resetear instrucciones si no es fragil"""
    for record in self:
      if not record.es_fragil:
        record.instrucciones_fragilidad = False
        

