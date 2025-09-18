from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from control.models import Sede
from .helpers import _redirect_if_authenticated, _redirect_if_sede


# ---------------------
# Lobby
# ---------------------

def appLobbyRender(request):
    # Info: Renderiza la página principal (Lobby) del aplicativo
    # Params:
    #   - request (HttpRequest) -> Objeto de solicitud HTTP

    # Warn: Si el usuario ya está autenticado, será redirigido
    is_authenticated = _redirect_if_authenticated(request)
    if is_authenticated:
        return is_authenticated

    # Warn: Si existe "sede_id" en sesión, será redirigido
    is_sede = _redirect_if_sede(request)
    if is_sede:
        return is_sede

    # Return: render() de 'lobby.html'
    return render(request, 'lobby.html')


# ---------------------
# QR Reader
# ---------------------

def appQrReaderRender(request):
    # Info: Renderiza la página del lector de QR
    # Params:
    #   - request (HttpRequest) -> Objeto de solicitud HTTP

    # Warn: Si el usuario ya está autenticado, será redirigido
    is_authenticated = _redirect_if_authenticated(request)
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

    # Return: render() de 'qr_reader.html' con información de la sede si existe
    return render(request, 'qr_reader.html', {'sede_info': sede_info})


# ---------------------
# Dashboard
# ---------------------

@login_required
def appDashboardHomeRender(request):
    # Info: Renderiza el bloque principal del Dashboard
    # Warn: Requiere que el usuario esté autenticado (login_required)
    # Params:
    #   - request (HttpRequest) -> Objeto de solicitud HTTP

    # Warn: Si existe "sede_id" en sesión, será redirigido
    is_sede = _redirect_if_sede(request)
    if is_sede:
        return is_sede

    # Return: render() de 'block_content/home.html'
    return render(request, 'block_content/home.html')


@login_required
def appDashboardActiveEmployeesRender(request):
    # Info: Renderiza el bloque de empleados activos dentro del Dashboard
    # Warn: Requiere que el usuario esté autenticado (login_required)
    # Params:
    #   - request (HttpRequest) -> Objeto de solicitud HTTP

    # Return: render() de 'block_content/active_employees.html'
    return render(request, 'block_content/active_employees.html')


@login_required
def appDashboardAssistanceRecordRender(request):
    # Info: Renderiza el bloque de registros de asistencia dentro del Dashboard
    # Warn: Requiere que el usuario esté autenticado (login_required)
    # Params:
    #   - request (HttpRequest) -> Objeto de solicitud HTTP

    # Return: render() de 'block_content/assistance_records.html'
    return render(request, 'block_content/assistance_records.html')


@login_required
def appDashboardNewsRender(request):
    # Info: Renderiza el bloque de novedades dentro del Dashboard
    # Warn: Requiere que el usuario esté autenticado (login_required)
    # Params:
    #   - request (HttpRequest) -> Objeto de solicitud HTTP

    # Return: render() de 'block_content/news.html'
    return render(request, 'block_content/news.html')


# ---------------------
# Dashboard Settings
# ---------------------

@login_required
def appDashboardLocationSettingsRender(request):
    # Info: Renderiza el bloque de configuración de sedes dentro del Dashboard
    # Warn: Requiere que el usuario esté autenticado (login_required)
    # Params:
    #   - request (HttpRequest) -> Objeto de solicitud HTTP

    # Return: render() de 'block_content/settings/locations.html'
    return render(request, 'block_content/settings/locations.html')


@login_required
def appDashboardWorkAreaSettingsRender(request):
    # Info: Renderiza el bloque de configuración de áreas de trabajo dentro del Dashboard
    # Warn: Requiere que el usuario esté autenticado (login_required)
    # Params:
    #   - request (HttpRequest) -> Objeto de solicitud HTTP

    # Return: render() de 'block_content/settings/work_areas.html'
    return render(request, 'block_content/settings/work_areas.html')


@login_required
def appDashboardSchedulesSettingsRender(request):
    # Info: Renderiza el bloque de configuración de horarios dentro del Dashboard
    # Warn: Requiere que el usuario esté autenticado (login_required)
    # Params:
    #   - request (HttpRequest) -> Objeto de solicitud HTTP

    # Return: render() de 'block_content/settings/schedules.html'
    return render(request, 'block_content/settings/schedules.html')


@login_required
def appDashboardTypeNewsSettingsRender(request):
    # Info: Renderiza el bloque de configuración de tipos de novedades dentro del Dashboard
    # Warn: Requiere que el usuario esté autenticado (login_required)
    # Params:
    #   - request (HttpRequest) -> Objeto de solicitud HTTP

    # Return: render() de 'block_content/settings/type_news.html'
    return render(request, 'block_content/settings/type_news.html')
