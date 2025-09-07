from django.shortcuts import redirect
from django.contrib.auth import logout


# ---------------------
# Logout
# ---------------------

def logoutSesion(request):
    # Info: Cierra la sesión del usuario y limpia la información de la sesión
    # Params:
    #   - request (HttpRequest) -> Objeto de solicitud HTTP

    # Warn: Si el usuario está autenticado, se cierra su sesión
    if request.user.is_authenticated:
        logout(request)

    # Warn: Se elimina "sede_id" de la sesión en caso de existir
    request.session.pop('sede_id', None)

    # Debug: Print de las claves en sesión (eliminar en producción)
    print(request.session.keys())

    # Return: redirect() hacia 'appLobbyRender'
    return redirect('appLobbyRender')