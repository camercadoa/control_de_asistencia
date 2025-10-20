from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_POST
from .helpers import _success, _error, _warning, _parse_request_body


# ---------------------
# Definir sede
# ---------------------


@require_POST
def defineLocation(request: HttpRequest) -> JsonResponse:
    '''
    Info:
        Define la sede en la que se almacenarán los registros de asistencia mediante una solicitud POST.

    Params:
        request (HttpRequest): Objeto de solicitud HTTP para obtener información de la URL.

    Return:
        JsonResponse: Respuesta JSON con estructura {"status", "message", "data?"} que indica el resultado de la operación.
    '''

    try:
        # Info: Parsear y validar el cuerpo de la solicitud
        data, response = _parse_request_body(request, "defineLocation")
        if response:
            return response

        # Info: Validar ID de sede proporcionado
        sede_id, response = _validate_sede(data)
        if response:
            return response

        # Info: Guardar sede en sesión y retornar confirmación
        return _save_sede_in_session(request, sede_id)

    except Exception as e:
        # Warn: Captura cualquier excepción inesperada durante el proceso
        return _error(
            user_message="Ocurrió un problema inesperado. Contacte a Soporte",
            code=500,
            log_message="Excepción en defineLocation",
            exc=e
        )


# ---------------------
# Helpers
# ---------------------


def _validate_sede(data: dict) -> tuple[str | None, JsonResponse | None]:
    '''
    Info:
        Valida la presencia del ID de sede en los datos recibidos.

    Params:
        data (dict): Diccionario con los datos de la solicitud que contiene el parámetro 'sede'.

    Return:
        tuple: Tupla (sede_id, response) donde:
            - sede_id (str): ID de sede validado si existe
            - response (JsonResponse): Respuesta de advertencia si falta el parámetro, o None si es válido
    '''

    # Info: Extraer y validar parámetro sede
    if not (sede_id := data.get("sede")):
        # Warn: Parámetro sede faltante - interrumpe flujo principal
        return None, _warning(
            user_message="Debes seleccionar una sede antes de continuar",
            code=400,
            log_message="Parámetro 'sede' faltante en defineLocation"
        )

    return sede_id, None


def _save_sede_in_session(request: HttpRequest, sede_id: str) -> JsonResponse:
    '''
    Info:
        Almacena el ID de sede en la sesión del usuario y retorna confirmación exitosa.

    Params:
        request (HttpRequest): Objeto de solicitud HTTP para obtener información de la URL.
        sede_id (str): Identificador de la sede a almacenar en sesión.

    Return:
        JsonResponse: Respuesta JSON exitosa con estructura {"status", "message", "data"} confirmando la operación.
    '''

    # Info: Guardar sede_id en sesión y retornar confirmación
    request.session["sede_id"] = sede_id
    return _success(
        user_message="La sede se ha definido correctamente",
        data={"sede_id": sede_id},
        log_message=f"Sede {sede_id} definida en la sesión."
    )
