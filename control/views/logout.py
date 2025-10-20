from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib.auth import logout


# ---------------------
# Logout
# ---------------------


def logoutSesion(request: HttpRequest) -> HttpResponseRedirect:
    '''
    Info:
        Cierra la sesión del usuario autenticado y elimina la sede de la sesión.

    Params:
        request (HttpRequest): Objeto de solicitud HTTP para obtener información de la URL.

    Return:
        HttpResponseRedirect: Redirección a la vista 'appLobbyRender' después de limpiar la sesión.
    '''

    # Info: Cerrar sesión solo si el usuario está autenticado
    if request.user.is_authenticated:
        logout(request)

    # Info: Eliminar sede_id de la sesión si existe
    request.session.pop('sede_id', None)

    return redirect('appLobbyRender')
