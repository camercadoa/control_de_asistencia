import json
import traceback
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from .utilities import success, error, warning, info

@csrf_exempt
def validateAuthentication(request):
    try:
        if request.method != "POST":
            return warning(
                user_message="Método no permitido",
                code=405,
                log_message=f"Método {request.method} en validateAuthentication"
            )

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError as e:
            return error(
                user_message="Los datos enviados no son válidos",
                code=400,
                log_message="JSON inválido en validateAuthentication",
                exc=e
            )

        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return warning(
                user_message="Debes ingresar usuario y contraseña",
                code=400,
                log_message="Credenciales incompletas"
            )

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return success(
                user_message="Inicio de sesión exitoso",
                log_message=f"Usuario {username} inició sesión"
            )
        else:
            return warning(
                user_message="Usuario o contraseña incorrecto",
                code=401,
                log_message=f"Intento fallido de login con usuario {username}"
            )

    except Exception as e:
        traceback.print_exc()
        return error(
            user_message="Ocurrió un error inesperado en el servidor",
            code=500,
            log_message="Excepción en validateAuthentication",
            exc=e
        )
