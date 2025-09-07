import json
import logging
from django.http import JsonResponse
from django.shortcuts import redirect

logger = logging.getLogger(__name__)


# ---------------------
# Helpers de Respuesta JSON
# ---------------------

def _build_response(status: str, user_message: str, data: dict = None, code: int = 200, log_message: str = None, exc: Exception = None):
    # Info: Función auxiliar para estandarizar todas las respuestas JSON
    # Params:
    #   - status (str) -> Estado de la respuesta: "info" | "success" | "warning" | "error"
    #   - user_message (str) -> Mensaje claro para el usuario final
    #   - data (dict | None) -> Información adicional para incluir en la respuesta
    #   - code (int) -> Código de estado HTTP (default=200)
    #   - log_message (str | None) -> Mensaje técnico para logs (si no se pasa, usa user_message)
    #   - exc (Exception | None) -> Excepción capturada (si existe, imprime stacktrace)

    # Info: Logging según el tipo de status recibido
    if log_message and status == 'info':
        logger.info(f"INFO -> {log_message}")
    elif log_message and status == 'success':
        logger.info(f"SUCCESS -> {log_message}")
    elif log_message and status == 'warning':
        logger.warning(f"WARNING -> {log_message}")
    elif log_message and status == 'error':
        logger.error(f"ERROR -> {log_message}")
        if exc:
            logger.exception(f'EXCEPTION -> {str(exc)}')

    # Info: Construcción del cuerpo de la respuesta
    response = {
        "status": status,
        "message": user_message
    }
    if data is not None:
        response["data"] = data

    # Return: JsonResponse con la estructura {"status", "message", "data?"}
    return JsonResponse(response, status=code)


def _success(user_message: str, data: dict = None, log_message: str = None, code: int = 200):
    # Info: Helper para respuestas exitosas
    # Params:
    #   - user_message (str) -> Mensaje claro para el usuario
    #   - data (dict | None) -> Información adicional opcional
    #   - log_message (str | None) -> Mensaje técnico para logs
    #   - code (int) -> Código HTTP (default=200)

    # Return: JsonResponse con status="success"
    return _build_response(
        status="success",
        user_message=user_message,
        data=data,
        code=code,
        log_message=log_message
    )


def _error(user_message: str, code: int = 500, log_message: str = None, exc: Exception = None):
    # Info: Helper para respuestas de error
    # Params:
    #   - user_message (str) -> Mensaje de error para el usuario
    #   - code (int) -> Código HTTP (default=500)
    #   - log_message (str | None) -> Mensaje técnico para logs
    #   - exc (Exception | None) -> Excepción capturada para logging detallado

    # Return: JsonResponse con status="error"
    return _build_response(
        status="error",
        user_message=user_message,
        code=code,
        log_message=log_message,
        exc=exc
    )


def _warning(user_message: str, code: int = 400, log_message: str = None):
    # Info: Helper para advertencias
    # Params:
    #   - user_message (str) -> Mensaje de advertencia
    #   - code (int) -> Código HTTP (default=400)
    #   - log_message (str | None) -> Mensaje técnico para logs

    # Return: JsonResponse con status="warning"
    return _build_response(
        status="warning",
        user_message=user_message,
        code=code,
        log_message=log_message
    )


def _info(user_message: str, data: dict = None, code: int = 200, log_message: str = None):
    # Info: Helper para mensajes informativos
    # Params:
    #   - user_message (str) -> Mensaje de información
    #   - data (dict | None) -> Información adicional opcional
    #   - code (int) -> Código HTTP (default=200)
    #   - log_message (str | None) -> Mensaje técnico para logs

    # Return: JsonResponse con status="info"
    return _build_response(
        status="info",
        user_message=user_message,
        data=data,
        code=code,
        log_message=log_message
    )


# ---------------------
# Helpers de Redirección
# ---------------------

def _redirect_if_authenticated(request):
    # Info: Redirección condicional según autenticación
    # Warn: Si el usuario está autenticado, lo redirige directamente al Dashboard
    # Params:
    #   - request (HttpRequest) -> Objeto de solicitud HTTP

    # Return: redirect() o None si no aplica
    if request.user.is_authenticated:
        return redirect('appDashboardHomeRender')
    return None


def _redirect_if_sede(request):
    # Info: Redirección condicional según sesión
    # Warn: Si existe "sede_id" en la sesión, lo redirige al QR Reader
    # Params:
    #   - request (HttpRequest) -> Objeto de solicitud HTTP

    # Return: redirect() o None si no aplica
    if 'sede_id' in request.session:
        return redirect('appQrReaderRender')
    return None


# ---------------------
# Helpers de Request
# ---------------------


def _parse_request_body(request, context):
    # Info: Convierte el body de la solicitud en JSON
    # Params:
    #   - request (HttpRequest)
    #   - context (str) -> Nombre de la función para log

    try:
        return json.loads(request.body), None
    except json.JSONDecodeError as e:
        # Warn: Error al parsear el JSON
        # Return: Respuesta JSON de error con código 400
        return None, _error(
            user_message="La información enviada no es válida",
            code=400,
            log_message=f"JSON inválido en {context}",
            exc=e
        )
