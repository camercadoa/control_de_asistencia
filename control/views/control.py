import traceback
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from control.models import Empleado, Sede, RegistroAsistencia
from .helpers import _success, _error, _warning, _info, _parse_request_body
from control.api import RegistroAsistenciaSerializer


# ---------------------
# Definir sede
# ---------------------

@csrf_exempt
@require_POST
def defineLocation(request):
    # Info: Define la sede en la que se almacenarán los registros de asistencia
    # Params:
    #   - request (HttpRequest) -> Objeto de solicitud HTTP

    try:
        # Info: Parsear body
        data, response = _parse_request_body(request, "defineLocation")
        if response:
            # Return: Respuesta JSON de error si el body es inválido
            return response

        # Info: Validar sede
        sede_id, response = _validate_sede(data)
        if response:
            # Return: Respuesta JSON de advertencia si no se envió sede
            return response

        # Info: Guardar en sesión
        # Return: Respuesta JSON de éxito
        return _save_sede_in_session(request, sede_id)

    except Exception as e:
        # Warn: Captura cualquier excepción inesperada
        traceback.print_exc()  # Debug: remover en producción
        # Return: Respuesta JSON de error con código 500
        return _error(
            user_message="Ocurrió un problema inesperado. Contacte a Soporte",
            code=500,
            log_message="Excepción en defineLocation",
            exc=e
        )


# ---------------------
# Guardar registro
# ---------------------

@csrf_exempt
@require_POST
def saveRecord(request):
    # Info: Guarda registros de ingreso o salida de empleados
    # Params:
    #   - request (HttpRequest) -> Objeto de solicitud HTTP

    try:
        # Info: Parsear body
        data, response = _parse_request_body(request, "saveRecord")
        if response:
            # Return: Respuesta JSON de error si el body es inválido
            return response

        # Info: Extraer datos principales
        codigo = data.get("codigo")
        sede_id = request.session.get("sede_id")

        # Info: Validar sede en sesión
        response = _validate_sede_in_session(sede_id)
        if response:
            # Return: Respuesta JSON de advertencia si no hay sede en sesión
            return response

        # Info: Validar código de empleado
        response = _validate_codigo(codigo)
        if response:
            # Return: Respuesta JSON de advertencia si el código no es válido
            return response

        # Info: Buscar empleado
        empleado, response = _get_empleado(codigo)
        if response:
            # Return: Respuesta JSON de error si el empleado no existe
            return response

        # Info: Validar estado activo
        response = _validate_empleado_activo(empleado)
        if response:
            # Return: Respuesta JSON de advertencia si el empleado está inactivo
            return response

        # Info: Guardar registro
        registro, empleado_info = _save_asistencia(empleado, sede_id)

        # Return: Respuesta JSON de éxito
        return _success(
            user_message="Registro guardado correctamente",
            data={"empleado": empleado_info},
            log_message=f"Registro de asistencia guardado para empleado {codigo} en sede {sede_id}"
        )

    except Exception as e:
        # Warn: Captura cualquier excepción inesperada
        traceback.print_exc()  # Debug: remover en producción
        # Return: Respuesta JSON de error con código 500
        return _error(
            user_message="Ocurrió un problema inesperado al guardar el registro",
            code=500,
            log_message="Excepción en saveRecord",
            exc=e
        )


# ---------------------
# Helpers
# ---------------------


def _validate_sede(data):
    # Info: Valida que se envíe un ID de sede
    sede_id = data.get("sede")
    if not sede_id:
        # Warn: Parámetro sede faltante
        # Return: Respuesta JSON de advertencia con código 400
        return None, _warning(
            user_message="Debes seleccionar una sede antes de continuar",
            code=400,
            log_message="Parámetro 'sede' faltante en defineLocation"
        )
    return sede_id, None


def _save_sede_in_session(request, sede_id):
    # Info: Guarda la sede en la sesión
    request.session["sede_id"] = sede_id
    # Return: Respuesta JSON de éxito
    return _success(
        user_message="La sede se ha definido correctamente",
        data={"sede_id": sede_id},
        log_message=f"Sede {sede_id} definida en la sesión."
    )


def _validate_sede_in_session(sede_id):
    # Info: Valida que haya una sede definida en sesión
    if not sede_id:
        # Warn: No hay sede en sesión
        # Return: Respuesta JSON de advertencia con código 400
        return _warning(
            user_message="Debes seleccionar una sede antes de registrar asistencias",
            code=400,
            log_message="Intento de saveRecord sin sede en sesión"
        )
    return None


def _validate_codigo(codigo):
    # Info: Valida que el código de empleado sea correcto
    if not codigo:
        # Warn: Código faltante
        # Return: Respuesta JSON de advertencia con código 400
        return _warning(
            user_message="Debes ingresar un código de empleado",
            code=400,
            log_message="Código de empleado faltante en saveRecord"
        )

    if not str(codigo).isdigit():
        # Warn: Código no numérico
        # Return: Respuesta JSON de advertencia con código 400
        return _warning(
            user_message=f"El código ingresado no es válido, debe ser numérico <br><br>"
                        f"<strong class='fs-5'>Código recibido:</strong> {codigo}",
            code=400,
            log_message=f"Código no numérico recibido en saveRecord: {codigo}"
        )
    return None


def _get_empleado(codigo):
    # Info: Obtiene un empleado por código
    try:
        return Empleado.objects.get(numero_documento=codigo), None
    except Empleado.DoesNotExist:
        # Warn: Empleado no encontrado
        # Return: Respuesta JSON de error con código 404
        return None, _error(
            user_message=f"No se ha encontrado un empleado vinculado <br><br>"
                        f"<strong class='fs-5'>Código recibido:</strong> {codigo}",
            code=404,
            log_message=f"Empleado no encontrado con código {codigo}"
        )


def _validate_empleado_activo(empleado):
    # Info: Verifica si el empleado está activo
    if not empleado.activo:
        # Warn: Empleado inactivo
        # Return: Respuesta JSON de advertencia con código 403
        return _warning(
            user_message="El empleado está inactivo y no puede registrar asistencias",
            code=403,
            log_message=f"Intento de registro de asistencia para empleado inactivo {empleado.numero_documento}"
        )
    return None


def _save_asistencia(empleado, sede_id):
    # Info: Crea un registro de asistencia y construye la respuesta
    sede = Sede.objects.get(id=sede_id)
    registro = RegistroAsistencia.objects.create(
        fk_empleado=empleado,
        descripcion_registro="Salida",
        fecha_hora_registro=timezone.now(),
        lugar_registro=sede
    )

    # Info: Serializar registro guardado
    serializer = RegistroAsistenciaSerializer(registro)
    payload = serializer.data

    # Info: Construir información del empleado
    empleado_info = {
        "nombre_completo": f"{empleado.primer_nombre.upper()} "
                        f"{empleado.segundo_nombre.upper() or ''} "
                        f"{empleado.primer_apellido.upper()} "
                        f"{empleado.segundo_apellido.upper() or ''}",
        "cargo": empleado.cargo.upper(),
        "fecha_registro": payload["fecha"],
        "hora_registro": payload["hora"],
        "descripcion_registro": "Salida"
    }

    # Return: Objeto de registro y datos del empleado
    return registro, empleado_info
