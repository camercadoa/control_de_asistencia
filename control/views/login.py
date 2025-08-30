import json
import traceback
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from .helpers import success, error, warning, info
from django.views.decorators.http import require_POST

# Info: El decorador @require_POST asegura que solo se permita el método POST en este endpoint.
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
        # Warn: Manejo de excepciones para asegurar que los errores sean capturados y respondidos adecuadamente.
        traceback.print_exc()
        return error(
            user_message="Ocurrió un error inesperado en el servidor",
            code=500,
            log_message="Excepción en validateAuthentication",
            exc=e
        )


def _parse_request_body(request):
    try:
        # Info: Se intenta convertir el cuerpo de la solicitud en JSON para procesarlo.
        return json.loads(request.body), None
    except json.JSONDecodeError as e:
        # Warn: Si ocurre un error al parsear el JSON, se retorna un error adecuado.
        return None, error(
            user_message="Los datos enviados no son válidos",
            code=400,
            log_message="JSON inválido en validateAuthentication",
            exc=e
        )


def _validate_credentials(data):
    # Params: data (dict) -> Diccionario que contiene los datos enviados en el request.
    username = data.get("username")
    password = data.get("password")

    # Warn: Si no se proporcionan las credenciales necesarias, se retorna una advertencia.
    if not username or not password:
        return None, None, warning(
            user_message="Debes ingresar usuario y contraseña",
            code=400,
            log_message="Credenciales incompletas"
        )
    return username, password, None


def _authenticate_user(request, username, password):
    # Info: Se usa el método authenticate de Django para verificar las credenciales.
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return success(
            user_message="Inicio de sesión exitoso",
            log_message=f"Usuario {username} inició sesión"
        )
    # Warn: Si las credenciales no son correctas, se retorna un mensaje de error.
    return warning(
        user_message="Usuario o contraseña incorrecto",
        code=401,
        log_message=f"Intento fallido de login con usuario {username}"
    )
