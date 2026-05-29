import json
import logging
from datetime import datetime

# 'http' nos da el decorador @http.route para definir URLs.
# 'request' es el objeto global que representa la peticion HTTP entrante
# (parecido al 'req' de Express o el 'request' de Flask/Django).
from odoo import http
from odoo.http import request

# Logger estandar de Odoo. Todo lo que pongas aqui aparece en los logs
# del contenedor (docker compose logs web). Es tu mejor amigo para debug.
_logger = logging.getLogger(__name__)


# Toda clase que define rutas HTTP en Odoo hereda de http.Controller.
# El nombre de la clase es libre, pero por convencion usamos PascalCase
# y un nombre descriptivo.
class VentiappWebhookController(http.Controller):

    # El decorador @http.route es lo que convierte un metodo normal de Python
    # en un endpoint HTTP accesible desde el navegador o por POST externo.
    @http.route(
        '/ventiapp/webhook',     # La URL: https://tu-odoo.com/ventiapp/webhook
        type='http',             # 'http' = control total sobre request/response (lo mejor para webhooks externos)
        auth='public',           # 'public' = no requiere login (Ventiapp no tiene credenciales de Odoo)
        methods=['POST'],        # Solo aceptamos POST; GET devolveria 404
        csrf=False,              # Desactivamos CSRF porque NO es un form web; es una API externa
    )
    def receive_webhook(self, **kwargs):
        """
        Recibe cualquier webhook de Ventiapp.
        - Guarda el payload crudo en la tabla ventiapp.webhook.log.
        - Responde 200 OK rapidamente (Ventiapp reintenta si tarda).
        - NO procesa la logica todavia (eso lo agregaremos despues).
        """

        # === PASO 1: Leer el body raw de la peticion ===
        # request.httprequest es el objeto Werkzeug original (Odoo usa Werkzeug por debajo).
        # .data es el body en bytes; lo decodificamos a string UTF-8.
        try:
            raw_body = request.httprequest.data.decode('utf-8') or ''
        except Exception as e:
            # Si ni siquiera podemos leer el body, dejamos string vacio y logueamos.
            _logger.warning('No se pudo decodificar el body del webhook: %s', e)
            raw_body = ''

        # === PASO 2: Intentar parsear como JSON para extraer el tipo de evento ===
        # Hacemos esto BEST EFFORT: si falla, no rompemos. Igual guardamos el body crudo.
        event_type = ''
        try:
            payload_dict = json.loads(raw_body) if raw_body else {}
            # Probamos varias claves comunes donde puede venir el tipo de evento.
            # No sabemos exactamente cual usa Ventiapp; cuando lleguen webhooks reales
            # veremos el formato y ajustamos.
            event_type = (
                payload_dict.get('event_type')
                or payload_dict.get('type')
                or payload_dict.get('event')
                or ''
            )
        except json.JSONDecodeError:
            # No es JSON valido. Lo loguemos pero igual seguimos.
            _logger.warning('Body del webhook no es JSON valido. Se guardara raw.')

        # === PASO 3: Guardar el log SIEMPRE ===
        # .sudo() bypasea las reglas de acceso del usuario actual.
        # Necesario porque auth='public' significa que no hay usuario logueado,
        # entonces sin sudo() no tendriamos permisos para escribir en la tabla.
        log = request.env['ventiapp.webhook.log'].sudo().create({
            'name': f'Webhook {event_type or "(sin tipo)"} - {datetime.now().isoformat(timespec="seconds")}',
            'event_type': event_type,
            'payload': raw_body,
            'status': 'pending',
        })

        _logger.info(
            'Ventiapp webhook recibido. log_id=%s, event_type=%s, bytes=%s',
            log.id, event_type, len(raw_body),
        )

        # === PASO 4: Responder 200 OK con un JSON simple ===
        # Con type='http' tenemos que construir la respuesta manualmente.
        # Devolvemos JSON para que Ventiapp pueda parsear la respuesta si quiere.
        return request.make_response(
            json.dumps({'ok': True, 'log_id': log.id}),
            headers=[('Content-Type', 'application/json')],
        )
