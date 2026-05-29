{
    'name': 'Ventiapp Connector',
    'version': '17.0.1.0.0',
    'summary': 'Recibe webhooks de Ventiapp (VTEX) y los traduce a Odoo',
    'description': """
Ventiapp Connector
==================

Este módulo recibe webhooks desde Ventiapp (que a su vez está conectado a VTEX)
y los procesa para crear/actualizar:

- Órdenes de venta
- Productos
- Clientes
- Movimientos de stock

También envía notificaciones de vuelta a Ventiapp cuando ciertos eventos
ocurren en Odoo (ej. picking validado).
""",
    'author': 'Manuable',
    'website': 'https://manuable.com',
    'category': 'Sales/Connector',
    'depends': [
        'base',
        'sale',
        'stock',
        'product',
        'contacts',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/webhook_log_views.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
