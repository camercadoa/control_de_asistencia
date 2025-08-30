from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from control.models import (
    Sede
)
from .helpers import redirect_if_authenticated_or_sede


# Info: Renderiza la página principal (Lobby) del aplicativo
# Warn: Si el usuario ya está autenticado o tiene "sede_id" en sesión, será redirigido
# Return: redirect() si aplica o render() de 'lobby.html'
def appLobbyRender(request):
    # Info: Validación de redirecciones centralizada
    redirection = redirect_if_authenticated_or_sede(request)
    if redirection:
        return redirection
    return render(
        request,
        'lobby.html'
    )


# Info: Renderiza la página del lector de QR
# Warn: Si "sede_id" en sesión no corresponde a una sede válida, se elimina de la sesión
# Return: render() de 'qr_reader.html' con información de la sede si existe
def appQrReaderRender(request):

    sede_id = request.session.get("sede_id")
    sede_info = None

    # Info: Se envía la sede si existe en el request.session
    if sede_id:
        try:
            sede = Sede.objects.get(id=sede_id)
            sede_info = {
                "id": sede.id,
                "text": f"{sede.ubicacion} - {sede.ciudad}"
            }
        except Sede.DoesNotExist:
            request.session.pop("sede_id", None)
    return render(
        request,
        'qr_reader.html',
        {'sede_info': sede_info}
    )


# Info: Renderiza el Dashboard principal
# Warn: Requiere que el usuario esté autenticado (login_required)
# Return: render() de 'dashboard.html'
@login_required
def appDashboardRender(request):
    # Info: Validación de redirecciones centralizada
    redirection = redirect_if_authenticated_or_sede(request)
    if redirection:
        return redirection

    return render(
        request,
        'dashboard.html'
    )


# Info: Renderiza el bloque de empleados dentro del Dashboard
# Return: render() de 'block_content/employees.html'
def appDashboardEmployeesRender(request):
    return render(
        request,
        'block_content/employees.html'
    )


# Info: Renderiza el bloque de registros de asistencia dentro del Dashboard
# Return: render() de 'block_content/assistance_records.html'
def appDashboardAssistanceRecordRender(request):
    return render(
        request,
        'block_content/assistance_records.html'
    )
