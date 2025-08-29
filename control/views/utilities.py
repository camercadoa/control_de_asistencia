import logging
from django.http import JsonResponse

# Configuración del logging (puedes ajustarlo a tus necesidades)
logging.basicConfig(level=logging.DEBUG,
                    format=' %(levelname)s - %(message)s')


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

    # Si hay log_message, se registra en los logs según estatus
    if log_message and status == 'info':
        logging.info(f"Log message: {log_message}")
    elif log_message and status == 'success':
        logging.info(f"Log message: {log_message}")
    elif log_message and status == 'warning':
        logging.warning(f"Log message: {log_message}")
    elif log_message and status == 'error':
        logging.error(f"Log message: {log_message}")
        if exc:
            logging.exception(f'Excepción: {str(exc)}')

    # Respuesta para el usuario
    response = {
        "status": status,
        "message": user_message
    }
    if data is not None:
        response["data"] = data

    return JsonResponse(response, status=code)


def success(user_message: str, data: dict = None, log_message: str = None, code: int = 200):
    return build_response(
        status="success",
        user_message=user_message,
        data=data,
        code=code,
        log_message=log_message
    )


def error(user_message: str, code: int = 500, log_message: str = None, exc: Exception = None):
    return build_response(
        status="error",
        user_message=user_message,
        code=code,
        log_message=log_message,
        exc=exc
    )


def warning(user_message: str, code: int = 400, log_message: str = None):
    return build_response(
        status="warning",
        user_message=user_message,
        code=code,
        log_message=log_message
    )


def info(user_message: str, data: dict = None, code: int = 200, log_message: str = None):
    return build_response(
        status="info",
        user_message=user_message,
        data=data,
        code=code,
        log_message=log_message
    )
