from datetime import time
from datetime import datetime, timedelta
from django.db.models import QuerySet
from django.http import HttpRequest, JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.core.exceptions import ObjectDoesNotExist
from control.models import Empleado, Sede, RegistroAsistencia, Horario
from .helpers import _success, _error, _warning, _info, _parse_request_body
from control.api import RegistroAsistenciaSerializer


# ---------------------
# Guardar registro
# ---------------------


@require_POST
def saveRecord(request: HttpRequest) -> JsonResponse:
    '''
    Info:
        Procesa una solicitud POST para guardar un registro de asistencia de empleado.

    Params:
        request (HttpRequest): Objeto de solicitud HTTP para obtener información de la URL.

    Return:
        JsonResponse: Respuesta JSON con estructura {"status", "message", "data?"} indicando el resultado de la operación.
    '''

    try:
        # Info: Parsear y validar el cuerpo de la solicitud
        data, response = _parse_request_body(request, "saveRecord")
        if response:
            return response

        employee_code = data.get("codigo")
        sede_id = request.session.get("sede_id")

        # Warn: Validar que la sede esté presente en la sesión
        if response := _validate_sede_in_session(sede_id):
            return response

        # Warn: Validar formato del código de empleado
        if response := _validate_employee_code(employee_code):
            return response

        # Info: Obtener información del empleado desde la base de datos
        employee, response = _get_employee(employee_code)
        if response:
            return response

        # Warn: Verificar que el empleado esté activo
        if response := _validate_active_employee(employee):
            return response

        # Info: Guardar registro de asistencia y obtener información
        record, response = _save_attendance(
            employee, sede_id)

        # Warn: Manejar caso donde no se pudo guardar el registro
        if not record:
            return response

        # Info: Retornar respuesta exitosa con datos del empleado
        return _success(
            user_message="Registro guardado correctamente",
            data={"empleado": response},
            log_message=f"Registro de asistencia guardado para empleado {employee_code} en sede {sede_id}"
        )

    except Exception as e:
        # Warn: Captura cualquier excepción inesperada durante el proceso
        return _error(
            user_message="Ocurrió un problema inesperado. Contacte a Soporte",
            code=500,
            log_message="Excepción en saveRecord",
            exc=e
        )


# ---------------------
# Helpers
# ---------------------


def _validate_sede_in_session(sede_id: str) -> JsonResponse | None:
    '''
    Info:
        Valida que exista un ID de sede en la sesión del usuario.

    Params:
        sede_id (str): ID de la sede obtenido de la sesión del usuario.

    Return:
        JsonResponse | None: Respuesta JSON de advertencia si no hay sede, None si la validación es exitosa.
    '''

    # Info: Validar presencia de sede en sesión
    if not sede_id:
        # Warn: Sesión sin sede definida - interrumpe flujo de registro
        return _warning(
            user_message="Debes seleccionar una sede antes de registrar asistencias",
            code=400,
            log_message="Intento de saveRecord sin sede en sesión"
        )

    return None


def _validate_employee_code(employee_code: str) -> JsonResponse | None:
    '''
    Info:
        Valida el formato y presencia del código de empleado.

    Params:
        employee_code (str): Código del empleado a validar.

    Return:
        JsonResponse | None: Respuesta JSON de advertencia si la validación falla, None si es exitosa.
    '''

    # Info: Validar presencia del código
    if not employee_code:
        # Warn: Código de empleado requerido
        return _warning(
            user_message="Debes ingresar un código de empleado",
            code=400,
            log_message="Código de empleado faltante en saveRecord"
        )

    # Info: Convertir a string y validar formato numérico
    employee_code_str = str(employee_code)
    # Warn: Código contiene caracteres no numéricos
    return _warning(
        user_message=f"El código ingresado no es válido, debe ser numérico <br><br>"
        f"<strong class='fs-5'>Código recibido:</strong> {employee_code}",
        code=400,
        log_message=f"Código no numérico recibido en saveRecord: {employee_code}"
    ) if not employee_code_str.isdigit() else None


def _get_employee(employee_code: str) -> tuple[Empleado | None, JsonResponse | None]:
    '''
    Info:
        Obtiene un empleado por su código/número de documento.

    Params:
        employee_code (str): Código o número de documento del empleado a buscar.

    Return:
        tuple: Tupla con (empleado, error_response) donde:
            - empleado: Objeto Empleado si se encuentra, None en caso contrario
            - error_response: JsonResponse de error si no se encuentra, None en caso exitoso
    '''

    # Info: Intenta obtener el empleado por su número de documento
    if employee := Empleado.objects.filter(numero_documento=employee_code).first():
        return employee, None

    # Warn: Empleado no encontrado; genera una respuesta de error estructurada
    return None, _error(
        user_message=f"No se ha encontrado un empleado vinculado <br><br>"
        f"<strong class='fs-5'>Código recibido:</strong> {employee_code}",
        code=404,
        log_message=f"Empleado no encontrado con código {employee_code}"
    )


def _validate_active_employee(employee: Empleado) -> JsonResponse | None:
    '''
    Info:
        Valida si un empleado está activo en el sistema.

    Params:
        employee (Empleado): Objeto empleado a validar.

    Return:
        JsonResponse | None: Respuesta JSON de advertencia si el empleado está inactivo, None si el empleado está activo.
    '''

    # Info: Verificar estado activo del empleado
    # Warn: Retornar advertencia si el empleado está inactivo
    return _warning(
        user_message="El empleado está inactivo y no puede registrar asistencias",
        code=403,
        log_message=f"Intento de registro de asistencia para empleado inactivo {employee.numero_documento}"
    ) if not employee.activo else None


def _save_attendance(employee: Empleado, sede_id: int) -> tuple[RegistroAsistencia | None, dict | JsonResponse]:
    '''
    Info:
        Registra una entrada o salida según el último registro histórico del empleado.

    Params:
        employee (Empleado): Objeto del empleado que realiza el registro.
        sede_id (int): ID de la sede donde se registra la asistencia.

    Return:
        tuple: Tupla con (registro, respuesta) donde:
            - registro: Objeto RegistroAsistencia si se creó exitosamente
            - respuesta: Información del empleado y registro, o respuesta de error/informativa
    '''

    # Info: Obtener fecha y hora actual
    current_time = timezone.now()

    # Info: Obtener último registro histórico
    last_record = RegistroAsistencia.objects.filter(
        fk_empleado=employee).order_by('-fecha_hora_registro').first()
    record_type = _determine_record_type(last_record)

    # Warn: Si hay una Entrada sin Salida y ya pasaron más de 18h, crear Salida automática
    if last_record and last_record.descripcion_registro == "Entrada":
        time_difference = current_time - last_record.fecha_hora_registro
        if time_difference > timedelta(hours=18):
            _create_automatic_exit(employee, last_record, sede_id)
            record_type = "Entrada"  # Nueva entrada tras cierre automática

    # Warn: Validar diferencia mínima solo si es una Salida normal.
    if record_type == "Salida" and last_record:
        if response := _validate_minimum_difference(last_record, current_time, employee):
            return None, response  # Return: No cumple el tiempo mínimo

    # Info: Obtener la sede correspondiente al ID proporcionado
    try:
        sede = Sede.objects.get(id=sede_id)
    except ObjectDoesNotExist:
        return None, _error(
            user_message="La sede seleccionada no existe",
            code=404,
            log_message=f"Sede no encontrada con ID {sede_id}"
        )

    # Info: Crear registro de asistencia
    record = RegistroAsistencia.objects.create(
        fk_empleado=employee,
        descripcion_registro=record_type,
        fecha_hora_registro=current_time,
        lugar_registro=sede
    )

    # Info: Evaluar puntualidad del empleado
    _evaluate_punctuality(employee, record, record_type)

    # Return: Registro creado exitosamente
    return _build_record_response(employee, record, record_type)


def _determine_record_type(last_record: RegistroAsistencia | None) -> str:
    '''
    Info:
        Determina el tipo de registro (Entrada/Salida) basado en el último registro histórico.

    Params:
        last_record (RegistroAsistencia | None): Último registro de asistencia del empleado.

    Return:
        str: Tipo de registro - "Entrada" si no hay registro anterior o la última fue Salida, "Salida" si el último registro fue una Entrada.
    '''

    # Info: Determinar tipo basado en último registro
    return "Entrada" if not last_record or last_record.descripcion_registro == "Salida" else "Salida"


def _create_automatic_exit(employee: Empleado, last_record: RegistroAsistencia, sede_id: int) -> None:
    '''
    Info:
        Crea un registro de salida automática cuando un empleado olvida registrar su salida.

    Params:
        employee (Empleado): Objeto del empleado para el cual se crea la salida automática.
        last_record (RegistroAsistencia): Último registro de entrada del empleado.
        sede_id (int): ID de la sede donde se registra la asistencia.

    Return:
        None: La función no retorna valor, solo crea el registro en la base de datos.
    '''

    # Info: Obtener objeto sede por ID
    try:
        sede = Sede.objects.get(id=sede_id)
    except Sede.DoesNotExist:
        return  # Return: Si la sede no existe

    # Info: Definir rangos horarios y reglas para salida automática
    entry_time = last_record.fecha_hora_registro.time()

    # Info: Rangos horarios para aplicar reglas específicas
    start_range_1, end_range_1 = time(5, 00), time(13, 30)  # 5:30 am - 1:30 pm
    start_range_2, end_range_2 = time(13, 30), time(21, 0)  # 1:30 pm - 9:00 pm
    fixed_exit_time = time(21, 30)  # 9:30 pm

    # Info: Calcular hora de salida automática según reglas establecidas
    if start_range_1 <= entry_time < end_range_1:
        # Regla 1: Salida 9 horas después de la entrada (turno mañana)
        automatic_exit = last_record.fecha_hora_registro + timedelta(hours=9)
    elif start_range_2 <= entry_time < end_range_2:
        # Regla 2: Salida fija a las 9:30 pm (turno tarde)
        automatic_exit = last_record.fecha_hora_registro.replace(
            hour=fixed_exit_time.hour,
            minute=fixed_exit_time.minute,
            second=0,
            microsecond=0
        )
    else:
        # Warn: Caso fuera de rangos definidos, aplicar regla por defecto
        automatic_exit = last_record.fecha_hora_registro + timedelta(hours=9)

    # Info: Crear registro de salida automática en base de datos
    RegistroAsistencia.objects.create(
        fk_empleado=employee,
        descripcion_registro="Salida",
        fecha_hora_registro=automatic_exit,
        lugar_registro=sede,
        estado_registro="Automática"
    )


def _validate_minimum_difference(last_record: RegistroAsistencia, current_time: datetime, employee: Empleado) -> JsonResponse | None:
    '''
    Info:
        Valida que haya pasado el tiempo mínimo requerido entre registros consecutivos.

    Params:
        last_record (RegistroAsistencia): Último registro de asistencia del empleado.
        current_time (datetime): Momento actual del registro.
        employee (Empleado): Objeto del empleado que realiza el registro.

    Return:
        JsonResponse | None: Respuesta informativa si no cumple el tiempo mínimo, None si la validación es exitosa.
    '''

    # Info: Calcular diferencia de tiempo desde el último registro
    # Warn: Retornar advertencia si no ha pasado el tiempo mínimo requerido
    if (time_difference := current_time - last_record.fecha_hora_registro) < timedelta(minutes=30):
        return _info(
            user_message="Tiempo mínimo entre Entrada y Salida no cumplido",
            code=200,
            log_message=f"Intento de salida anticipada para empleado {employee.numero_documento} ({time_difference})."
        )

    return None


def _evaluate_punctuality(employee: Empleado, record: RegistroAsistencia, record_type: str) -> None:
    '''
    Info:
        Evalúa la puntualidad de un registro comparándolo con los horarios asignados al empleado.

    Params:
        employee (Empleado): Objeto del empleado que realiza el registro.
        record (RegistroAsistencia): Registro de asistencia recién creado.
        record_type (str): Tipo de registro - "Entrada" o "Salida".

    Return:
        None: La función modifica el estado del registro pero no retorna valor.
    '''

    # Info: Obtener horarios asignados al empleado
    schedules = employee.horarios.all()
    if not schedules.exists():
        return  # Return: No hay horarios definidos para evaluar

    # Info: Configurar tolerancia y zona horaria
    tolerance = timedelta(minutes=10)
    timezone_obj = timezone.get_current_timezone()
    record_datetime = record.fecha_hora_registro

    # Info: Omitir evaluación los fines de semana
    if record_datetime.weekday() in (5, 6):
        return

    # Info: Evaluar puntualidad para registro de entrada
    if record_type == "Entrada":
        if best_schedule := _get_most_recent_entry_schedule(schedules, record_datetime, timezone_obj):
            scheduled_time = timezone.make_aware(
                datetime.combine(record_datetime.date(), best_schedule.hora_entrada), timezone_obj
            )

            # Warn: Marcar como retraso si excede la tolerancia
            if (time_difference := record_datetime - scheduled_time) > tolerance:
                record.minutos = int(time_difference.total_seconds() // 60)
                record.estado_registro = "Con retraso"
                record.save()
        return

    # Info: Evaluar puntualidad para registro de salida
    if record_type == "Salida":
        # Info: Buscar última entrada registrada del empleado
        last_entry = RegistroAsistencia.objects.filter(
            fk_empleado=employee, descripcion_registro="Entrada").order_by('-fecha_hora_registro').first()
        if not last_entry:
            return  # Return: No hay entrada previa para evaluar salida

        # Info: Obtener horario correspondiente a la entrada
        if best_entry_schedule := _get_most_recent_entry_schedule(schedules, last_entry.fecha_hora_registro, timezone_obj):
            # Info: Calcular hora programada de salida
            scheduled_exit_time = timezone.make_aware(
                datetime.combine(last_entry.fecha_hora_registro.date(), best_entry_schedule.hora_salida),
                timezone_obj
            )

            # Warn: Ajustar para turnos que cruzan medianoche
            if best_entry_schedule.hora_salida < best_entry_schedule.hora_entrada:
                scheduled_exit_time = timezone.make_aware(
                    datetime.combine(
                        last_entry.fecha_hora_registro.date() + timedelta(days=1),
                        best_entry_schedule.hora_salida
                    ), timezone_obj
                )

            # Warn: Marcar como anticipación si sale antes del tiempo permitido
            if (time_difference := record_datetime - scheduled_exit_time) < -tolerance:
                record.minutos = int(-time_difference.total_seconds() // 60)
                record.estado_registro = "Con anticipación"
                record.save()


def _get_most_recent_entry_schedule(schedules: QuerySet[Horario], record_datetime: datetime, timezone_obj: timezone) -> Horario | None:
    '''
    Info:
        Encuentra el horario asignado cuya hora de entrada programada esté más cercana al registro actual.

    Params:
        schedules (QuerySet[Horario]): Conjunto de horarios asignados al empleado.
        record_datetime (datetime): Fecha y hora del registro de asistencia.
        timezone_obj (timezone): Zona horaria activa para las conversiones.

    Return:
        Horario | None: Objeto Horario con la entrada más cercana al registro, o None si no hay horarios.
    '''

    # Info: Inicializar variables para búsqueda del horario más cercano
    best_schedule, min_difference = None, None

    # Info: Evaluar cada horario para encontrar la entrada más cercana
    for schedule in schedules:
        # Info: Convertir hora programada a datetime con zona horaria
        scheduled_time = timezone.make_aware(
            datetime.combine(record_datetime.date(), schedule.hora_entrada), timezone_obj
        )

        # Info: Calcular diferencia absoluta con el registro actual
        time_difference = abs(record_datetime - scheduled_time)

        # Info: Actualizar mejor horario si encontramos diferencia menor
        if min_difference is None or time_difference < min_difference:
            min_difference = time_difference
            best_schedule = schedule

    return best_schedule


def _build_record_response(employee: Empleado, record: RegistroAsistencia, record_type: str) -> tuple[RegistroAsistencia, dict]:
    '''
    Info:
        Construye la respuesta del registro de asistencia con datos serializados del empleado.

    Params:
        employee (Empleado): Objeto del empleado que realizó el registro.
        record (RegistroAsistencia): Registro de asistencia creado.
        record_type (str): Tipo de registro - "Entrada" o "Salida".

    Return:
        tuple: Tupla con (registro, empleado_info) donde:
            - registro: Objeto RegistroAsistencia original
            - empleado_info: Diccionario con datos resumidos del empleado para la respuesta
    '''

    # Info: Serializar registro y construir nombre completo del empleado
    payload = RegistroAsistenciaSerializer(record).data

    # Info: Construir nombre completo filtrando campos vacíos
    full_name = " ".join(filter(None, [
        employee.primer_nombre,
        employee.segundo_nombre,
        employee.primer_apellido,
        employee.segundo_apellido
    ])).upper()

    # Info: Crear diccionario con información resumida del empleado
    employee_info = {
        "nombre_completo": full_name,
        "cargo": employee.cargo.upper(),
        "fecha_registro": payload["fecha"],
        "hora_registro": payload["hora"],
        "descripcion_registro": record_type
    }

    return record, employee_info
