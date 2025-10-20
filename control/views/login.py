from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from .helpers import _success, _error, _warning, _parse_request_body
from django.views.decorators.http import require_POST


# ---------------------
# Autenticación
# ---------------------


@csrf_exempt
@require_POST
def validateAuthentication(request: HttpRequest) -> JsonResponse:
    '''
    Info:
        Procesa los datos de usuario y contraseña, verifica su validez y autentica al usuario.

    Params:
        request (HttpRequest): Objeto de solicitud HTTP para obtener información de la URL.

    Return:
        JsonResponse: Respuesta JSON con el resultado de la autenticación o error.
    '''

    # Info: Procesa y valida el cuerpo de la solicitud
    data, response = _parse_request_body(request, "validateAuthentication")
    if response:
        return response

    # Info: Valida las credenciales del usuario
    username, password, response = _validate_credentials(data)
    if response:
        return response

    return _authenticate_user(request, username, password)


# ---------------------
# Helpers
# ---------------------


def _validate_credentials(data: dict) -> tuple[str, str, JsonResponse | None]:
    '''
    Info:
        Valida que las credenciales de usuario estén presentes y completas.

    Params:
        data (dict): Diccionario con los datos de la solicitud que contiene las credenciales.

    Return:
        tuple: Tupla con (username, password, None) si son válidos, o (None, None, JsonResponse) si hay errores de validación.
    '''

    # Info: Extrae username y password del diccionario de datos
    username = data.get("username")
    password = data.get("password")

    # Warn: Valida que ambas credenciales estén presentes
    if not username or not password:
        return None, None, _warning(
            user_message="Debes ingresar usuario y contraseña",
            code=400,
            log_message="Credenciales incompletas"
        )

    return username, password, None


def _authenticate_user(request: HttpRequest, username: str, password: str) -> JsonResponse:
    '''
    Info:
        Autentica un usuario verificando credenciales y permisos de grupo.

    Params:
        request (HttpRequest): Objeto de solicitud HTTP para obtener información de la URL.
        username (str): Nombre de usuario para autenticar.
        password (str): Contraseña del usuario.

    Return:
        JsonResponse: Respuesta JSON indicando éxito o fallo en la autenticación.
        (Estructura: {"status", "message", "data"?})
    '''

    # Info: Autentica al usuario con las credenciales proporcionadas
    user = authenticate(request, username=username, password=password)

    # Warn: Verifica que el usuario exista y esté activo
    if user is None:
        return _warning(
            user_message="Usuario o contraseña incorrectos",
            code=401,
            log_message=f"Intento fallido de login con usuario {username}"
        )

    # Info: Define los grupos autorizados para el sistema
    groups = ["Secretaria Talento Humano", "Director Talento Humano", "Presidente", "Rector"]

    # Warn: Verifica si el usuario pertenece a al menos uno de los grupos requeridos
    if not any(user.groups.filter(name=grupo).exists() for grupo in groups):
        return _error(
            user_message="Usuario no autorizado",
            code=403,
            log_message=f"Usuario {username} intentó acceder sin pertenecer a los grupos requeridos"
        )

    # Info: Ejecuta el login del usuario en la sesión actual
    login(request, user)
    return _success(
        user_message="Inicio de sesión exitoso",
        log_message=f"Usuario {username} inició sesión"
    )
