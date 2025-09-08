from datetime import timedelta
import datetime
from django.utils import timezone
from django.views.decorators.http import require_POST
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
        registro, empleado_info_or_response = _save_asistencia(empleado, sede_id)

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
    # Info: Determina si el registro será Entrada o Salida, valida diferencia mínima de 30 min, y crea el registro
    # Params:
    #   - empleado (Empleado) -> Objeto del empleado
    #   - sede_id (int) -> ID de la sede donde se registrará

    # Info: Obtener fecha actual
    ahora = timezone.now()
    hoy_inicio = ahora.replace(hour=0, minute=0, second=0, microsecond=0)
    hoy_fin = ahora.replace(hour=23, minute=59, second=59, microsecond=999999)

    # Info: Buscar último registro del día
    ultimo_registro = RegistroAsistencia.objects.filter(
        fk_empleado=empleado,
        fecha_hora_registro__range=(hoy_inicio, hoy_fin)
    ).order_by('-fecha_hora_registro').first()

    # Info: Determinar tipo de registro
    if not ultimo_registro or ultimo_registro.descripcion_registro == "Salida":
        tipo_registro = "Entrada"
    else:
        tipo_registro = "Salida"

        # Info: Validar diferencia mínima de 30 min entre Entrada y Salida
        diferencia = ahora - ultimo_registro.fecha_hora_registro
        # if diferencia < timedelta(minutes=30):
        if diferencia < timedelta(minutes=1):
            # Info: No se permite guardar todavía
            return None, _info(
                user_message="Tiempo mínimo entre Entrada y Salida no cumplido",
                code=200,
                log_message=f"Intento de salida para empleado {empleado.numero_documento} antes del tiempo mínimo (diferencia: {diferencia})"
            )

    # Info: Guardar registro
    sede = Sede.objects.get(id=sede_id)
    registro = RegistroAsistencia.objects.create(
        fk_empleado=empleado,
        descripcion_registro=tipo_registro,
        fecha_hora_registro=ahora,
        lugar_registro=sede
    )

    # Info: Calcular puntualidad si es Entrada o Salida
    horarios = empleado.horarios.all()
    gabela = timedelta(minutes=10)
    if horarios.exists():
        registro_datetime = ahora

        # Info: Buscar el horario más cercano
        mejor_horario = None
        menor_diferencia = None

        # Info: Comparar con cada horario del empleado
        for horario in horarios:
            if tipo_registro == "Entrada":
                hora_programada = datetime.combine(registro_datetime.date(), horario.hora_entrada)
            else:
                hora_programada = datetime.combine(registro_datetime.date(), horario.hora_salida)

            delta = abs(registro_datetime - hora_programada)

            # Warn: Encontrar el horario con la menor diferencia
            if menor_diferencia is None or delta < menor_diferencia:
                menor_diferencia = delta
                mejor_horario = horario

        if mejor_horario:
            if tipo_registro == "Entrada":
                hora_entrada = datetime.combine(registro_datetime.date(), mejor_horario.hora_entrada)
                delta = registro_datetime - hora_entrada
                if delta > gabela:
                    registro.registro_atraso = int(delta.total_seconds() // 60)
                    registro.estado_registro = "Con retraso"
            else:
                hora_salida = datetime.combine(registro_datetime.date(), mejor_horario.hora_salida)
                delta = hora_salida - registro_datetime
                if delta > gabela:
                    registro.registro_salida_anticipada = int(delta.total_seconds() // 60)
                    registro.estado_registro = "Con anticipación"

            registro.save()

    # Info: Serializar registro guardado
    serializer = RegistroAsistenciaSerializer(registro)
    payload = serializer.data

    empleado_info = {
        "nombre_completo": f"{empleado.primer_nombre.upper()} "
                        f"{empleado.segundo_nombre.upper() or ''} "
                        f"{empleado.primer_apellido.upper()} "
                        f"{empleado.segundo_apellido.upper() or ''}",
        "cargo": empleado.cargo.upper(),
        "fecha_registro": payload["fecha"],
        "hora_registro": payload["hora"],
        "descripcion_registro": tipo_registro,
        "estado_registro": registro.estado_registro,
        "minutos_atraso": registro.registro_atraso,
        "minutos_anticipacion": registro.registro_salida_anticipada
    }

    return registro, empleado_info
