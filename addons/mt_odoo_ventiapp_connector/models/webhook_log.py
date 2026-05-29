from odoo import models, fields

class VentiappWebhookLog(models.Model):
    _name = 'ventiapp.webhook.log'
    _description = 'Log de Webhooks recibidos desde Ventiapp'
    _order = 'received_at desc'

    name = fields.Char(string='Referencia', required=True)
    event_type = fields.Char(string='Tipo de evento', index=True)
    payload = fields.Text(string='Payload (JSON)')
    received_at = fields.Datetime(
        string='Recibido en',
        default=fields.Datetime.now,
        required=True,
    )
    status = fields.Selection([
        ('pending', 'Pendiente'),
        ('processed', 'Procesado'),
        ('failed', 'Fallido')
    ], default='pending', required=True, index=True)
    error_message = fields.Text(string='Mensaje de error')
    processing_attempts = fields.Integer(string='Intentos', default=0)