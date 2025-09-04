import json
import traceback
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from .helpers import success, error, warning, info
from django.views.decorators.http import require_POST


# Info: Endpoint para validar autenticación de usuario
# Info: El decorador @require_POST asegura que solo se permita el método POST
@csrf_exempt
@require_POST
def validateAuthentication(request):
    try:
        # 1. Parsear body
        data, response = _parse_request_body(request)
        if response:
            return response

        # 2. Validar credenciales
        username, password, response = _validate_credentials(data)
        if response:
            return response

        # 3. Autenticar usuario
        return _authenticate_user(request, username, password)

    except Exception as e:
        # Warn: Captura cualquier excepción inesperada en el servidor
        traceback.print_exc()
        return error(
            user_message="Ocurrió un error inesperado en el servidor",
            code=500,
            log_message="Excepción en validateAuthentication",
            exc=e
        )


def _parse_request_body(request):
    try:
        # Info: Convierte el cuerpo de la solicitud en JSON
        return json.loads(request.body), None
    except json.JSONDecodeError as e:
        # Warn: Error al parsear el JSON enviado en la solicitud
        return None, error(
            user_message="Los datos enviados no son válidos",
            code=400,
            log_message="JSON inválido en validateAuthentication",
            exc=e
        )


# Params: data (dict) -> Diccionario que contiene los datos enviados en el request
def _validate_credentials(data):
    username = data.get("username")
    password = data.get("password")

    # Warn: Usuario o contraseña no proporcionados
    if not username or not password:
        return None, None, warning(
            user_message="Debes ingresar usuario y contraseña",
            code=400,
            log_message="Credenciales incompletas"
        )
    return username, password, None


# Params: username (str), password (str)
def _authenticate_user(request, username, password):
    # Info: Usa `authenticate` de Django para verificar credenciales
    user = authenticate(request, username=username, password=password)
    if user is not None:
        # Info: Validar grupos autorizados
        groups = ["Secretaria Talento Humano", "Director Talento Humano"]
        in_groups = any(
            user.groups.filter(name=grupo).exists() for grupo in groups
        )
        # Warn: Usuario no autorizado
        if not in_groups:
            return error(
                user_message="Usuario no autorizado",
                code=403,
                log_message=f"Usuario {username} intentó acceder sin pertenecer a los grupos requeridos"
            )

        login(request, user)
        return success(
            user_message="Inicio de sesión exitoso",
            log_message=f"Usuario {username} inició sesión"
        )

    # Warn: Usuario no existe
    return warning(
        user_message="Usuario o contraseña incorrectos",
        code=401,
        log_message=f"Intento fallido de login con usuario {username}"
    )
