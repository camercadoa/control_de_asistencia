from django.shortcuts import redirect
from django.contrib.auth import logout


# Info: Cierra la sesión del usuario y limpia la información de la sesión
# Warn: Si el usuario está autenticado, se cierra su sesión.
# Warn: Se elimina "sede_id" de la sesión en caso de existir.
# Return: redirect() hacia 'appLobbyRender'
def logoutSesion(request):
    # Info: Si el usuario está autenticado, cierra la sesión
    if request.user.is_authenticated:
        logout(request)

    # Info: Elimina "sede_id" si existe en la sesión
    request.session.pop('sede_id', None)

    # Info: Debug -> imprime las claves que aún permanecen en la sesión
    print(request.session.keys())

    # Info: Redirige al Lobby del aplicativo
    return redirect('appLobbyRender')
