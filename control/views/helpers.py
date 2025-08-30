import logging
from django.http import JsonResponse
from django.shortcuts import redirect

logger = logging.getLogger(__name__)


# Info: Función auxiliar para estandarizar todas las respuestas JSON
# Params:
#   status (str) -> Estado de la respuesta: "info" | "success" | "warning" | "error"
#   user_message (str) -> Mensaje claro para el usuario final
#   data (dict | None) -> Información adicional para incluir en la respuesta
#   code (int) -> Código de estado HTTP (default=200)
#   log_message (str | None) -> Mensaje técnico para logs (si no se pasa, usa user_message)
#   exc (Exception | None) -> Excepción capturada (si existe, imprime stacktrace)
# Return: JsonResponse con la estructura {"status", "message", "data?"}
# Example: return build_response("success", "Datos guardados correctamente", data={"id": 1})
def build_response(status: str, user_message: str, data: dict = None, code: int = 200, log_message: str = None, exc: Exception = None):
    # Info: Logging según el tipo de status recibido
    if log_message and status == 'info':
        logger.info(f"INFO: {log_message}")
    elif log_message and status == 'success':
        logger.info(f"SUCCESS: {log_message}")
    elif log_message and status == 'warning':
        logger.warning(f"WARNING: {log_message}")
    elif log_message and status == 'error':
        logger.error(f"ERROR: {log_message}")
        if exc:
            logger.exception(f'EXCEPTION: {str(exc)}')

    # Info: Construcción del cuerpo de la respuesta
    response = {
        "status": status,
        "message": user_message
    }
    if data is not None:
        response["data"] = data

    return JsonResponse(response, status=code)


# Info: Helper para respuestas exitosas
# Params:
#   user_message (str) -> Mensaje claro para el usuario
#   data (dict | None) -> Información adicional opcional
#   log_message (str | None) -> Mensaje técnico para logs
#   code (int) -> Código HTTP (default=200)
# Return: JsonResponse con status="success"
# Example: return success("Operación realizada con éxito", data={"id": 1})
def success(user_message: str, data: dict = None, log_message: str = None, code: int = 200):
    return build_response(
        status="success",
        user_message=user_message,
        data=data,
        code=code,
        log_message=log_message
    )


# Info: Helper para respuestas de error
# Params:
#   user_message (str) -> Mensaje de error para el usuario
#   code (int) -> Código HTTP (default=500)
#   log_message (str | None) -> Mensaje técnico para logs
#   exc (Exception | None) -> Excepción capturada para logging detallado
# Return: JsonResponse con status="error"
# Example: return error("No se pudo guardar la información", exc=e)
def error(user_message: str, code: int = 500, log_message: str = None, exc: Exception = None):
    return build_response(
        status="error",
        user_message=user_message,
        code=code,
        log_message=log_message,
        exc=exc
    )


# Info: Helper para advertencias
# Params:
#   user_message (str) -> Mensaje de advertencia
#   code (int) -> Código HTTP (default=400)
#   log_message (str | None) -> Mensaje técnico para logs
# Return: JsonResponse con status="warning"
# Example: return warning("El registro ya existe")
def warning(user_message: str, code: int = 400, log_message: str = None):
    return build_response(
        status="warning",
        user_message=user_message,
        code=code,
        log_message=log_message
    )


# Info: Helper para mensajes informativos
# Params:
#   user_message (str) -> Mensaje de información
#   data (dict | None) -> Información adicional opcional
#   code (int) -> Código HTTP (default=200)
#   log_message (str | None) -> Mensaje técnico para logs
# Return: JsonResponse con status="info"
# Example: return info("Sesión iniciada correctamente", data={"user": "Carlos"})
def info(user_message: str, data: dict = None, code: int = 200, log_message: str = None):
    return build_response(
        status="info",
        user_message=user_message,
        data=data,
        code=code,
        log_message=log_message
    )


# Info: Redirección condicional según autenticación o sesión
# Warn: Si el usuario está autenticado, lo redirige directamente al Dashboard
# Warn: Si existe "sede_id" en la sesión, lo redirige al QR Reader
# Return: redirect() o None si no aplica
# Example: return redirect_if_authenticated_or_sede(request)
def redirect_if_authenticated_or_sede(request):
    if request.user.is_authenticated:
        return redirect('appDashboardRender')

    if 'sede_id' in request.session:
        return redirect('appQrReaderRender')

    return None
