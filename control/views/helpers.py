import json
import logging
from typing import Optional, Tuple, Union
from django.http import HttpRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect


# Configuración del logger
logger = logging.getLogger(__name__)


# ---------------------
# Helpers de Respuesta JSON
# ---------------------


def _build_response(status: str, user_message: str, data: dict = None, code: int = 200, log_message: str = None, exc: Exception = None) -> JsonResponse:
    '''
    Info:
        Función auxiliar para estandarizar todas las respuestas JSON de la aplicación.

    Params:
        status (str): Estado de la respuesta: "info" | "success" | "warning" | "error".
        user_message (str): Mensaje claro y comprensible para el usuario final.
        data (dict): Información adicional opcional para incluir en la respuesta.
        code (int): Código de estado HTTP para la respuesta (default=200).
        log_message (str): Mensaje técnico opcional para registro en logs.
        exc (Exception): Excepción capturada opcional para registro de stacktrace.

    Return:
        JsonResponse: Respuesta HTTP estandarizada con estructura {"status", "message", "data?"}.
    '''

    # Info: Logging automático según el tipo de estado
    if log_message and (log_level := {
        'info': logger.info,
        'success': logger.info,
        'warning': logger.warning,
        'error': logger.error
    }.get(status)):
        log_level(f"{status.upper()} -> {log_message}")
        if status == 'error' and exc:
            logger.exception(f'EXCEPTION -> {str(exc)}')

    # Info: Construcción del cuerpo de respuesta estandarizado
    response = {
        "status": status,
        "message": user_message
    }
    if data is not None:
        response["data"] = data

    return JsonResponse(response, status=code)


def _success(user_message: str, data: dict = None, log_message: str = None, code: int = 200) -> JsonResponse:
    '''
    Info:
        Función helper especializada para generar respuestas exitosas estandarizadas.

    Params:
        user_message (str): Mensaje claro y comprensible para el usuario final.
        data (dict): Información adicional opcional para incluir en la respuesta.
        log_message (str): Mensaje técnico opcional para registro en logs del sistema.
        code (int): Código de estado HTTP para la respuesta (default=200).

    Return:
        JsonResponse: Respuesta HTTP estandarizada con status="success" y estructura definida.
    '''

    # Info: Construir la respuesta delegando al método principal
    return _build_response(
        status="success",
        user_message=user_message,
        data=data,
        code=code,
        log_message=log_message
    )


def _error(user_message: str, code: int = 500, log_message: str = None, exc: Exception = None) -> JsonResponse:
    '''
    Info:
        Función helper especializada para generar respuestas de error estandarizadas.

    Params:
        user_message (str): Mensaje de error claro y comprensible para el usuario final.
        code (int): Código de estado HTTP para la respuesta de error (default=500).
        log_message (str): Mensaje técnico opcional para registro en logs del sistema.
        exc (Exception): Excepción capturada opcional para registro de stacktrace detallado.

    Return:
        JsonResponse: Respuesta HTTP estandarizada con status="error" y estructura definida.
    '''

    # Info: Construir la respuesta delegando al método principal
    return _build_response(
        status="error",
        user_message=user_message,
        code=code,
        log_message=log_message,
        exc=exc
    )


def _warning(user_message: str, code: int = 400, log_message: str = None) -> JsonResponse:
    '''
    Info:
        Función helper especializada para generar respuestas de advertencia estandarizadas.

    Params:
        user_message (str): Mensaje de advertencia claro para el usuario final.
        code (int): Código de estado HTTP para la respuesta (default=400).
        log_message (str): Mensaje técnico opcional para registro en logs del sistema.

    Return:
        JsonResponse: Respuesta HTTP estandarizada con status="warning" y estructura definida.
    '''

    # Info: Construir la respuesta delegando al método principal
    return _build_response(
        status="warning",
        user_message=user_message,
        code=code,
        log_message=log_message
    )


def _info(user_message: str, data: dict = None, code: int = 200, log_message: str = None) -> JsonResponse:
    '''
    Info:
        Función helper especializada para generar respuestas informativas estandarizadas.

    Params:
        user_message (str): Mensaje informativo claro para el usuario final.
        data (dict): Información adicional opcional para incluir en la respuesta.
        code (int): Código de estado HTTP para la respuesta (default=200).
        log_message (str): Mensaje técnico opcional para registro en logs del sistema.

    Return:
        JsonResponse: Respuesta HTTP estandarizada con status="info" y estructura definida.
    '''

    # Info: Construir la respuesta delegando al método principal
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


def _redirect_if_authenticated(request: HttpRequest) -> Union[HttpResponseRedirect, None]:
    '''
    Info:
        Función de utilidad para manejar redirecciones condicionales basadas en autenticación.

    Params:
        request (HttpRequest): Objeto de solicitud HTTP para obtener información de la URL.

    Return:
        HttpResponseRedirect | None: Redirección al dashboard si está autenticado, None en caso contrario.
    '''

    # Warn: Redirige inmediatamente si el usuario ya está autenticado
    return redirect('appDashboardHomeRender') if request.user.is_authenticated else None


def _redirect_if_sede(request: HttpRequest) -> Union[HttpResponseRedirect, None]:
    '''
    Info:
        Función de utilidad para manejar redirecciones condicionales basadas en sesión.

    Params:
        request (HttpRequest): Objeto de solicitud HTTP para obtener información de la URL.

    Return:
        HttpResponseRedirect | None: Redirección al lector QR si existe sede en sesión, None en caso contrario.
    '''

    # Warn: Redirige inmediatamente si existe sede_id en la sesión
    return redirect('appQrReaderRender') if 'sede_id' in request.session else None


# ---------------------
# Helpers de Request
# ---------------------


def _parse_request_body(request: HttpRequest, context: str) -> Tuple[Optional[dict], Optional[JsonResponse]]:
    '''
    Info:
        Función de utilidad para parsear el cuerpo de solicitudes HTTP en formato JSON.

    Params:
        request (HttpRequest): Objeto de solicitud HTTP para obtener información de la URL.
        context (str): Nombre del contexto o función para identificar en logs de error.

    Return:
        tuple: Tupla (data, error) donde data es el JSON parseado o None, y error es JsonResponse o None.
    '''

    # Info: Intento de parseo seguro del cuerpo JSON
    try:
        return json.loads(request.body), None
    except json.JSONDecodeError as e:
        # Warn: Error crítico en formato JSON - retorna respuesta de error estandarizada
        return None, _error(
            user_message="La información enviada no es válida",
            code=400,
            log_message=f"JSON inválido en {context}",
            exc=e
        )
