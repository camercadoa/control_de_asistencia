from datetime import datetime, timedelta
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.core.exceptions import ObjectDoesNotExist
from control.models import Empleado, Sede, RegistroAsistencia
from .helpers import _success, _error, _warning, _info, _parse_request_body
from control.api import RegistroAsistenciaSerializer


# ---------------------
# Definir sede
# ---------------------

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
        # Return: Respuesta JSON de error con código 500
        return _error(
            user_message="Ocurrió un problema inesperado. Contacte a Soporte",
            code=500,
            log_message="Excepción en defineLocation",
            exc=e
        )


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


# ---------------------
# Guardar registro
# ---------------------

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
            # Return: Respuesta JSON de advertencia si el código es inválido
            return response

        # Info: Buscar empleado
        empleado, response = _get_empleado(codigo)
        if response:
            # Return: Respuesta JSON de error si no se encuentra el empleado
            return response

        # Info: Validar estado activo
        response = _validate_empleado_activo(empleado)
        if response:
            # Return: Respuesta JSON de advertencia si el empleado está inactivo
            return response

        # Info: Guardar registro considerando Entrada/Salida y diferencia mínima de 30 min
        registro, empleado_info_or_response = _save_asistencia(
            empleado, sede_id)

        if not registro:
            # Return: Puede ser un _info si la diferencia mínima no se cumple
            return empleado_info_or_response

        # Return: Respuesta JSON de éxito con info del empleado
        return _success(
            user_message="Registro guardado correctamente",
            data={"empleado": empleado_info_or_response},
            log_message=f"Registro de asistencia guardado para empleado {codigo} en sede {sede_id}"
        )

    except Exception as e:
        # Warn: Captura cualquier excepción inesperada
        # Return: Respuesta JSON de error con código 500
        return _error(
            user_message="Ocurrió un problema inesperado al guardar el registro",
            code=500,
            log_message="Excepción en saveRecord",
            exc=e
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
    """
    # Info:
    Registra una Entrada o Salida según el último registro histórico del empleado.
    Soporta turnos que cruzan medianoche y maneja casos en los que un trabajador olvida registrar la Salida.

    # Warn:
    Si el último registro fue una Entrada y han pasado más de 12 horas,
    se crea automáticamente una Salida intermedia antes de registrar la nueva Entrada.

    # Params:
        - empleado (Empleado) -> Objeto del empleado que realiza el registro.
        - sede_id (int) -> ID de la sede donde se registra la asistencia.

    # Return:
        tuple:
            - (registro, empleado_info) si se guarda correctamente.
            - (None, response) si se detecta una condición informativa (ej. tiempo mínimo no cumplido).
    """

    # Info: Obtener fecha y hora actual
    ahora = timezone.now()

    # Info: Obtener último registro histórico (no solo del día actual)
    ultimo_registro = (
        RegistroAsistencia.objects.filter(fk_empleado=empleado)
        .order_by('-fecha_hora_registro')
        .first()
    )

    # Info: Determinar tipo de registro
    tipo_registro = _determinar_tipo_registro(ultimo_registro)

    # Warn: Si hay una Entrada sin Salida y ya pasaron más de 12h, crear Salida automática
    if ultimo_registro and ultimo_registro.descripcion_registro == "Entrada":
        diferencia = ahora - ultimo_registro.fecha_hora_registro
        diferencia_minima = timedelta(hours=12)
        if diferencia > diferencia_minima:
            _crear_salida_automatica(empleado, ultimo_registro, sede_id)
            tipo_registro = "Entrada"  # Nueva entrada tras cierre automático

    # Warn: Validar diferencia mínima solo si es una Salida normal
    if tipo_registro == "Salida" and ultimo_registro:
        response = _validate_diferencia_minima(ultimo_registro, ahora, empleado)
        if response:
            return None, response  # Return: No cumple el tiempo mínimo

    # Info: Crear registro de asistencia
    try:
        sede = Sede.objects.get(id=sede_id)
    except ObjectDoesNotExist:
        return None, _error(
            user_message="La sede seleccionada no existe",
            code=404,
            log_message=f"Sede no encontrada con ID {sede_id}"
        )

    registro = RegistroAsistencia.objects.create(
        fk_empleado=empleado,
        descripcion_registro=tipo_registro,
        fecha_hora_registro=ahora,
        lugar_registro=sede
    )

    # Info: Evaluar puntualidad
    _evaluate_puntualidad(empleado, registro, tipo_registro)

    # Return: Registro creado exitosamente
    return _build_registro_response(empleado, registro, tipo_registro)


def _determinar_tipo_registro(ultimo_registro):
    """
    # Info:
    Determina si el próximo registro será de tipo Entrada o Salida,
    según el último registro histórico existente.
    """
    if not ultimo_registro or ultimo_registro.descripcion_registro == "Salida":
        return "Entrada"
    return "Salida"


def _crear_salida_automatica(empleado, ultimo_registro, sede_id):
    """
    # Info:
    Genera un registro de Salida automática cuando el empleado olvidó marcarla
    y han pasado más de 12 horas desde su última Entrada.

    # Params:
        - empleado (Empleado) -> Objeto del empleado.
        - ultimo_registro (RegistroAsistencia) -> Último registro tipo Entrada.
        - sede_id (int) -> ID de la sede para asociar el registro automático.
    """
    try:
        sede = Sede.objects.get(id=sede_id)
    except ObjectDoesNotExist:
        return

    salida_automatica = ultimo_registro.fecha_hora_registro + timedelta(hours=8)
    RegistroAsistencia.objects.create(
        fk_empleado=empleado,
        descripcion_registro="Salida",
        fecha_hora_registro=salida_automatica,
        lugar_registro=sede,
        estado_registro="Automática"
    )


def _validate_diferencia_minima(ultimo_registro, ahora, empleado):
    """
    # Info:
    Verifica que hayan pasado al menos 30 minutos entre Entrada y Salida consecutivas.

    # Params:
        - ultimo_registro (RegistroAsistencia) -> Último registro previo.
        - ahora (datetime) -> Momento actual.
        - empleado (Empleado) -> Objeto del empleado.

    # Return:
        JsonResponse informativo si no cumple el tiempo mínimo, o None si es válido.
    """
    diferencia = ahora - ultimo_registro.fecha_hora_registro
    diferencia_minima = timedelta(minutes=30)

    if diferencia < diferencia_minima:
        return _info(
            user_message="Tiempo mínimo entre Entrada y Salida no cumplido",
            code=200,
            log_message=f"Intento de salida anticipada para empleado {empleado.numero_documento} ({diferencia})."
        )
    return None


def _evaluate_puntualidad(empleado, registro, tipo_registro):
    """
    # Info:
    Evalúa si un registro fue puntual, con retraso o anticipación,
    comparándolo con los horarios asignados al empleado.

    # Params:
        - empleado (Empleado) -> Objeto del empleado.
        - registro (RegistroAsistencia) -> Registro recién creado.
        - tipo_registro (str) -> "Entrada" o "Salida".
    """
    horarios = empleado.horarios.all()
    if not horarios.exists():
        return

    gabela = timedelta(minutes=10)
    tz = timezone.get_current_timezone()
    registro_datetime = registro.fecha_hora_registro

    mejor_horario = _get_horario_mas_cercano(
        horarios, registro_datetime, tipo_registro, tz
    )
    if not mejor_horario:
        return

    hora_programada_naive = (
        mejor_horario.hora_entrada if tipo_registro == "Entrada" else mejor_horario.hora_salida
    )
    hora_programada = timezone.make_aware(
        datetime.combine(registro_datetime.date(), hora_programada_naive), tz
    )

    delta = (
        registro_datetime - hora_programada
        if tipo_registro == "Entrada"
        else hora_programada - registro_datetime
    )

    cambios = False
    if delta > gabela:
        registro.minutos = int(delta.total_seconds() // 60)
        registro.estado_registro = (
            "Con retraso" if tipo_registro == "Entrada" else "Con anticipación"
        )
        cambios = True

    if cambios:
        registro.save()


def _get_horario_mas_cercano(horarios, registro_datetime, tipo_registro, tz):
    """
    # Info:
    Busca el horario asignado cuya hora programada esté más cercana a la hora del registro.

    # Params:
        - horarios (QuerySet[Horario]) -> Conjunto de horarios del empleado.
        - registro_datetime (datetime) -> Hora del registro actual.
        - tipo_registro (str) -> "Entrada" o "Salida".
        - tz (timezone) -> Zona horaria activa.

    # Return:
        Horario más cercano (objeto Horario) o None si no hay coincidencias.
    """
    mejor_horario = None
    menor_diferencia = None

    for horario in horarios:
        hora_naive = horario.hora_entrada if tipo_registro == "Entrada" else horario.hora_salida
        hora_aware = timezone.make_aware(datetime.combine(registro_datetime.date(), hora_naive), tz)
        delta = abs(registro_datetime - hora_aware)

        if menor_diferencia is None or delta < menor_diferencia:
            menor_diferencia = delta
            mejor_horario = horario

    return mejor_horario


def _build_registro_response(empleado, registro, tipo_registro):
    """
    # Info:
    Serializa el registro de asistencia y construye un payload
    con los datos más relevantes del empleado.

    # Params:
        - empleado (Empleado) -> Objeto del empleado.
        - registro (RegistroAsistencia) -> Registro creado.
        - tipo_registro (str) -> "Entrada" o "Salida".

    # Return:
        tuple:
            - registro (RegistroAsistencia)
            - empleado_info (dict) -> Datos resumidos del empleado.
    """
    serializer = RegistroAsistenciaSerializer(registro)
    payload = serializer.data

    nombre_completo = " ".join(filter(None, [
        empleado.primer_nombre,
        empleado.segundo_nombre,
        empleado.primer_apellido,
        empleado.segundo_apellido
    ])).upper()

    empleado_info = {
        "nombre_completo": nombre_completo,
        "cargo": empleado.cargo.upper(),
        "fecha_registro": payload["fecha"],
        "hora_registro": payload["hora"],
        "descripcion_registro": tipo_registro
    }

    return registro, empleado_info