import traceback, logging
from django.http import JsonResponse

logger = logging.getLogger(__name__)


def build_response(status: str, user_message: str, data: dict = None, code: int = 200, log_message: str = None, exc: Exception = None):
    # * Función auxiliar para estandarizar todas las respuestas JSON
    # @ params {
    # @     status -> info | success | warning | error
    # @     user_message -> mensaje claro para el usuario final
    # @     data -> información adicional (opcional)
    # @     log_message -> mensaje técnico para logs (si no se pasa, usa el user_message)
    # @     code -> Estado HTTP de la respuesta del servidor
    # @     exc -> excepción capturada (si existe, imprime stacktrace)
    # @ }

    # Logging técnico
    if log_message or exc:
        tech_message = log_message or user_message
        if exc:
            logger.error(f"{tech_message}\n{traceback.format_exc()}")
        else:
            logger.warning(tech_message)

    # Respuesta para el usuario
    response = {
        "status": status,
        "message": user_message
    }
    if data is not None:
        response["data"] = data

    return JsonResponse(response, status=code)


def success(user_message: str, data: dict = None, log_message: str = None, code: int = 200):
    # * Respuesta para operaciones exitosas.
    return build_response(
        status="success",
        user_message=user_message,
        data=data,
        code=code,
        log_message=log_message
    )


def error(user_message: str, code: int = 500, log_message: str = None, exc: Exception = None):
    # * Respuesta para errores graves o excepciones.
    return build_response(
        status="error",
        user_message=user_message,
        code=code,
        log_message=log_message,
        exc=exc
    )


def warning(user_message: str, code: int = 400, log_message: str = None):
    # * Respuesta para advertencias o validaciones incumplidas.
    return build_response(
        status="warning",
        user_message=user_message,
        code=code,
        log_message=log_message
    )


def info(user_message: str, data: dict = None, code: int = 200, log_message: str = None):
    # * Respuesta para información general o mensajes neutrales.
    return build_response(
        status="info",
        user_message=user_message,
        data=data,
        code=code,
        log_message=log_message
    )


def obtenerInfoUserRequest(request):
    pass
