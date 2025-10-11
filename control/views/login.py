import traceback
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from .helpers import _success, _error, _warning, _info, _parse_request_body
from django.views.decorators.http import require_POST


# ---------------------
# Autenticación
# ---------------------

@csrf_exempt
@require_POST
def validateAuthentication(request):
    # Info: Endpoint para validar autenticación de usuario
    # Params:
    #   - request (HttpRequest) -> Objeto de solicitud HTTP

    try:
        # Info: Parsear body de la solicitud
        data, response = _parse_request_body(request, "validateAuthentication")
        if response:
            return response

        # Info: Validar credenciales
        username, password, response = _validate_credentials(data)
        if response:
            return response

        # Info: Autenticar usuario y devolver respuesta correspondiente
        # Return: Respuesta JSON de éxito, advertencia o error
        return _authenticate_user(request, username, password)

    except Exception as e:
        # Warn: Captura cualquier excepción inesperada en el servidor
        # Debug: Stacktrace de la excepción (eliminar en producción)
        traceback.print_exc()
        # Return: Respuesta JSON de error con código 500
        return _error(
            user_message="Ocurrió un error inesperado en el servidor",
            code=500,
            log_message="Excepción en validateAuthentication",
            exc=e
        )


# ---------------------
# Helpers
# ---------------------


def _validate_credentials(data):
    # Info: Valida que el diccionario contenga usuario y contraseña
    # Params:
    #   - data (dict) -> Diccionario que contiene los datos enviados en el request

    username = data.get("username")
    password = data.get("password")

    # Warn: Usuario o contraseña no proporcionados
    if not username or not password:
        # Return: Respuesta JSON de advertencia con código 400
        return None, None, _warning(
            user_message="Debes ingresar usuario y contraseña",
            code=400,
            log_message="Credenciales incompletas"
        )
    return username, password, None


def _authenticate_user(request, username, password):
    # Info: Usa `authenticate` de Django para verificar credenciales
    # Params:
    #   - request (HttpRequest) -> Objeto de solicitud HTTP
    #   - username (str) -> Nombre de usuario
    #   - password (str) -> Contraseña

    user = authenticate(request, username=username, password=password)
    if user is not None:
        # Info: Validar que el usuario pertenezca a grupos autorizados
        groups = ["Secretaria Talento Humano", "Director Talento Humano", "Presidente", "Rector"]
        in_groups = any(
            user.groups.filter(name=grupo).exists() for grupo in groups
        )

        # Warn: Usuario no autorizado
        if not in_groups:
            # Return: Respuesta JSON de error con código 403
            return _error(
                user_message="Usuario no autorizado",
                code=403,
                log_message=f"Usuario {username} intentó acceder sin pertenecer a los grupos requeridos"
            )

        # Info: Inicia sesión si el usuario está autorizado
        login(request, user)
        # Return: Respuesta JSON de éxito
        return _success(
            user_message="Inicio de sesión exitoso",
            log_message=f"Usuario {username} inició sesión"
        )

    # Warn: Usuario o contraseña incorrectos
    # Return: Respuesta JSON de advertencia con código 401
    return _warning(
        user_message="Usuario o contraseña incorrectos",
        code=401,
        log_message=f"Intento fallido de login con usuario {username}"
    )
