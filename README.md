** Proyecto de Prueba Contexto Cubano **
1-Navegar hasta el entorno
cd C:\Odoo14
venv\Scripts\activate
cd server
python odoo-bin scaffold --help // Comprueba si Odoo funciona
python odoo-bin -c odoo.conf --dev=xml // Inicia en modo dev
python odoo-bin -d dev_db -c odoo.conf --dev=xml // Especificar bd al iniciar
2-Crear directorio
cd server/custom-addons
mkdir desoft-prueba
cd desoft-prueba
Crear archivo **manifest**.py y **init**.py
3-Instalar y Activar
venv\Scripts\activate
python odoo-bin -c odoo.conf -d dev_db --dev=xml -u all // Iniciar actualizando todos los modulos
python odoo-bin -c odoo.conf -d dev_db --dev=xml -u desoft_prueba // Iniciar actualizando solo un modulo
