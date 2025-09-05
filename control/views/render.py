from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from control.models import (
    Sede
)
from .helpers import redirect_if_authenticated, redirect_if_sede

# ---------------------
# Lobby
# ---------------------


def appLobbyRender(request):
    # Info: Renderiza la página principal (Lobby) del aplicativo
    # Return: redirect() si aplica o render() de 'lobby.html'

    # Warn: Si el usuario ya está autenticado, será redirigido
    is_authenticated = redirect_if_authenticated(request)
    if is_authenticated:
        return is_authenticated

    # Warn: Si existe "sede_id" en sesión, será redirigido
    is_sede = redirect_if_sede(request)
    if is_sede:
        return is_sede

    return render(
        request,
        'lobby.html'
    )


# ---------------------
# QR Reader
# ---------------------


def appQrReaderRender(request):
    # Info: Renderiza la página del lector de QR
    # Return: render() de 'qr_reader.html' con información de la sede si existe

    # Warn: Si el usuario ya está autenticado, será redirigido
    is_authenticated = redirect_if_authenticated(request)
    if is_authenticated:
        return is_authenticated

    sede_id = request.session.get("sede_id")
    sede_info = None

    # Info: Se envía la sede si existe en el request.session
    if sede_id:
        try:
            sede = Sede.objects.get(id=sede_id)
            sede_info = {
                "id": sede.id,
                "location": f"{sede.ubicacion} - {sede.ciudad}"
            }
        # Warn: Si "sede_id" en sesión no corresponde a una sede válida, se elimina de la sesión
        except Sede.DoesNotExist:
            request.session.pop("sede_id", None)

    return render(
        request,
        'qr_reader.html',
        {'sede_info': sede_info}
    )


# ---------------------
# Dashboard
# ---------------------

@login_required
def appDashboardHomeRender(request):
    # Info: Renderiza el bloque principal del Dashboard
    # Return: render() de 'block_content/home.html'
    # Warn: Requiere que el usuario esté autenticado (login_required)

    # Warn: Si existe "sede_id" en sesión, será redirigido
    is_sede = redirect_if_sede(request)
    if is_sede:
        return is_sede

    return render(
        request,
        'block_content/home.html'
    )


@login_required
def appDashboardActiveEmployeesRender(request):
    # Info: Renderiza el bloque de empleados activos dentro del Dashboard
    # Return: render() de 'block_content/active_employees.html'
    # Warn: Requiere que el usuario esté autenticado (login_required)

    return render(
        request,
        'block_content/active_employees.html'
    )


@login_required
def appDashboardInactiveEmployeesRender(request):
    # Info: Renderiza el bloque de empleados inactivos dentro del Dashboard
    # Return: render() de 'block_content/inactive_employees.html'
    # Warn: Requiere que el usuario esté autenticado (login_required)

    return render(
        request,
        'block_content/inactive_employees.html'
    )


@login_required
def appDashboardAssistanceRecordRender(request):
    # Info: Renderiza el bloque de registros de asistencia dentro del Dashboard
    # Return: render() de 'block_content/assistance_records.html'
    # Warn: Requiere que el usuario esté autenticado (login_required)

    return render(
        request,
        'block_content/assistance_records.html'
    )


# ---------------------
# Dashboard Settings
# ---------------------

@login_required
def appDashboardLocationSettingsRender(request):
    # Info: Renderiza el bloque de configuración de sedes dentro del Dashboard
    # Return: render() de 'block_content/location_settings.html'
    # Warn: Requiere que el usuario esté autenticado (login_required)

    return render(
        request,
        'block_content/location_settings.html'
    )


@login_required
def appDashboardWorkAreaSettingsRender(request):
    # Info: Renderiza el bloque de configuración de áreas de trabajo dentro del Dashboard
    # Return: render() de 'block_content/work_area_settings.html'
    # Warn: Requiere que el usuario esté autenticado (login_required)

    return render(
        request,
        'block_content/work_area_settings.html'
    )
