import json
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from control.models import (
    Empleado, Sede, RegistroAsistencia
)
from control.views import success, error, warning
from control.api import RegistroAsistenciaSerializer


# * Definir sede en donde se almacenarán los registros de asistencia
@csrf_exempt
def defineLocation(request):
    try:
        if request.method != 'POST':
            return warning(
                user_message="Acción no permitida. Por favor, intenta nuevamente",
                code=405,
                log_message=f"Método {request.method} no permitido en defineLocation"
            )

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError as e:
            return error(
                user_message="La información enviada no es válida. Verifica e inténtalo otra vez",
                code=400,
                log_message="JSON inválido en defineLocation",
                exc=e
            )

        sede_id = data.get('sede')
        if not sede_id:
            return warning(
                user_message="Debes seleccionar una sede antes de continuar",
                code=400,
                log_message="Parámetro 'sede' faltante en defineLocation"
            )

        request.session['sede_id'] = sede_id
        return success(
            user_message="La sede se ha definido correctamente",
            data={"sede_id": sede_id},
            log_message=f"Sede {sede_id} definida en la sesión."
        )

    except Exception as e:
        return error(
            user_message="Ocurrió un problema inesperado. Contacte a Soporte",
            code=500,
            log_message="Excepción en defineLocation",
            exc=e
        )


# * Guardar los registros de ingreso o salida de los usuarios
@csrf_exempt
def saveRecord(request):
    if request.method != 'POST':
        return warning(
            user_message="Acción no permitida. Intenta nuevamente",
            code=405,
            log_message=f"Método {request.method} no permitido en saveRecord"
        )

    try:
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError as e:
            return error(
                user_message="La información enviada no es válida",
                code=400,
                log_message="JSON inválido en saveRecord",
                exc=e
            )

        codigo = data.get('codigo')
        descripcion = "Prueba"
        sede_id = request.session.get('sede_id')

        if not sede_id:
            return warning(
                user_message="Debes seleccionar una sede antes de registrar asistencias",
                code=400,
                log_message="Intento de saveRecord sin sede en sesión"
            )

        if not codigo:
            return warning(
                user_message="Debes ingresar un código de empleado",
                code=400,
                log_message="Código de empleado faltante en saveRecord"
            )

        if not str(codigo).isdigit():
            return warning(
                user_message=f"El código ingresado no es válido, debe ser un valor numérico <br><br> <strong class='fs-5'>Código recibido:</strong> {codigo}",
                code=400,
                log_message=f"Código no numérico recibido en saveRecord: {codigo}"
            )

        try:
            empleado = Empleado.objects.get(numero_documento=codigo)
        except Empleado.DoesNotExist:
            return error(
                user_message=f"No se ha encontrado un empleado vinculado <br><br> <strong class='fs-5'>Código recibido:</strong> {codigo}",
                code=404,
                log_message=f"Empleado no encontrado con código {codigo}"
            )

        if not empleado.activo:
            return warning(
                user_message="El empleado está inactivo y no puede registrar asistencias",
                code=403,
                log_message=f"Intento de registro de asistencia para empleado inactivo {codigo}"
            )

        if not empleado.activo:
            return warning(
                user_message="El empleado está inactivo y no puede registrar asistencias",
                code=403,
                log_message=f"Intento de registro de asistencia para empleado inactivo {codigo}"
            )

        # ✅ Guardar el registro
        sede = Sede.objects.get(id=sede_id)
        # registro = RegistroAsistencia.objects.create(
        #     fk_empleado=empleado,
        #     descripcion_registro=descripcion,
        #     fecha_hora_registro=timezone.now(),  # Guardado en UTC
        #     lugar_registro=sede
        # )

        # ✅ Preparar el registro (sin guardar en BD todavía)
        registro = RegistroAsistencia(
            fk_empleado=empleado,
            descripcion_registro=descripcion,
            fecha_hora_registro=timezone.now(),  # UTC
            lugar_registro=sede
        )

        serializer = RegistroAsistenciaSerializer(registro)
        payload = serializer.data

        # 👀 Imprimir en logs técnicos (no visible al usuario final)
        print(
            f"[DEBUG] Registro preparado -> Empleado: {empleado.numero_documento}, "
            f"Nombre: {empleado.primer_nombre} {empleado.primer_apellido}, "
            f"Descripción: {descripcion}, "
            f"Fecha: {payload["fecha"]}, "
            f"Hora: {payload["hora"]}, "
        )

        empleado_info = {
            'nombre_completo': f"{empleado.primer_nombre.upper()} {empleado.primer_apellido.upper()}",
            'cargo': empleado.cargo.upper(),
            "fecha_registro": payload["fecha"],
            "hora_registro": payload["hora"],
        }

        return success(
            user_message="Registro guardado correctamente",
            data={"empleado": empleado_info},
            log_message=f"Registro de asistencia guardado para empleado {codigo} en sede {sede_id}"
        )

    except Exception as e:
        return error(
            user_message="Ocurrió un problema inesperado al guardar el registro",
            code=500,
            log_message="Excepción en saveRecord",
            exc=e
        )