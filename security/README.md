# IR.MODEL.ACCESS.CSV

# id:

- Id único
- No se muestra al usuario
- No debe repetirse
- Puede ponerse cualquier nombre: "acces_hola_mundo_admin"

# name:

- Nombre descriptivo
- Puede ponerse cualquier texto
- Solo informativo

# model_id/id:

- NO ES EL NOMBRE DEL MODELO
- Es una referencia XML al modelo
- Toma el nombre del modelo: "hola.mundo" y lo convierte en snake
- La estructura es model_nombre_modelo

# group_id/id

- Indica que usuarios tendrán permisos
  - base.group_user -> Usuarios internos
  - base.group_admin -> Administradores
  - Vacio -> Todos

# Permisos

perm_read → leer registros
perm_write → modificar registros
perm_create → crear registros
perm_unlink → borrar registros
