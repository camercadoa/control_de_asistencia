from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from control.models import Sede
from .helpers import _redirect_if_authenticated, _redirect_if_sede


# ---------------------
# Lobby
# ---------------------

def appLobbyRender(request: HttpRequest) -> HttpResponse:
    '''
    Info:
        Renderiza el lobby de la aplicación después de validar autenticación y tipo de sede.

    Params:
        request (HttpRequest): Objeto de solicitud HTTP para obtener información de la URL.

    Return:
        HttpResponse: Renderizado de la página lobby o redirección según las validaciones.
    '''

    # Info: Verifica si el usuario está autenticado y redirige si es necesario
    if is_authenticated := _redirect_if_authenticated(request):
        return is_authenticated

    # Info: Verifica si es una sede y redirige si es necesario
    if is_sede := _redirect_if_sede(request):
        return is_sede

    return render(request, 'lobby.html')


# ---------------------
# QR Reader
# ---------------------


def appQrReaderRender(request: HttpRequest) -> HttpResponse:
    '''
    Info:
        Renderiza el lector de QR después de validar autenticación y recuperar información de sede.
        Proporciona datos de la sede actual si existe en la sesión.

    Params:
        request (HttpRequest): Objeto de solicitud HTTP para obtener información de la URL.

    Return:
        HttpResponse: Renderizado de la página QR reader con información de sede o redirección.
    '''

    # Info: Verifica si el usuario está autenticado y redirige si es necesario
    if is_authenticated := _redirect_if_authenticated(request):
        return is_authenticated

    # Info: Obtiene el ID de sede de la sesión y recupera información
    sede_id = request.session.get("sede_id")
    sede_info = None

    # Info: Si existe sede_id, busca y construye información de la sede
    if sede_id:
        try:
            sede = Sede.objects.get(id=sede_id)
            sede_info = {
                "id": sede.id,
                "location": f"{sede.ubicacion} - {sede.ciudad}"
            }
        except Sede.DoesNotExist:
            # Warn: Si la sede no existe, elimina el ID de la sesión
            request.session.pop("sede_id", None)

    return render(request, 'qr_reader.html', {'sede_info': sede_info})


# ---------------------
# Dashboard
# ---------------------


@login_required
def appDashboardHomeRender(request: HttpRequest) -> HttpResponse:
    '''
    Info:
        Renderiza la página principal del Dashboard para usuarios autenticados y proporciona tipos de novedades para la interfaz.

    Params:
        request (HttpRequest): Objeto de solicitud HTTP para obtener información de la URL.

    Return:
        HttpResponse: Renderizado de la página home del dashboard con tipos de novedades.
    '''

    # Info: Verifica si es una sede y redirige si es necesario
    if is_sede := _redirect_if_sede(request):
        return is_sede

    # Info: Define diccionario de tipos de novedades para la interfaz
    tipos = {
        'entradas': 'Entradas',
        'salidas': 'Salidas',
        'sedes': 'Sedes'
    }

    return render(request, 'block_content/home.html', {'tipos': tipos})


@login_required
def appDashboardActiveEmployeesRender(request: HttpRequest) -> HttpResponse:
    '''
    Info:
        Renderiza la interfaz para visualizar empleados actualmente activos en el sistema.

    Params:
        request (HttpRequest): Objeto de solicitud HTTP para obtener información de la URL.

    Return:
        HttpResponse: Renderizado de la página de empleados activos del dashboard.
    '''

    return render(request, 'block_content/active_employees.html')


@login_required
def appDashboardAssistanceRecordRender(request: HttpRequest) -> HttpResponse:
    '''
    Info:
        Renderiza la interfaz para visualizar los registros de asistencia del personal.

    Params:
        request (HttpRequest): Objeto de solicitud HTTP para obtener información de la URL.

    Return:
        HttpResponse: Renderizado de la página de registros de asistencia del dashboard.
    '''

    return render(request, 'block_content/assistance_records.html')


@login_required
def appDashboardNewsRender(request: HttpRequest) -> HttpResponse:
    '''
    Info:
        Renderiza la interfaz para visualizar y gestionar las novedades del sistema.

    Params:
        request (HttpRequest): Objeto de solicitud HTTP para obtener información de la URL.

    Return:
        HttpResponse: Renderizado de la página de novedades del dashboard.
    '''

    return render(request, 'block_content/news.html')


# ---------------------
# Dashboard Settings
# ---------------------


@login_required
def appDashboardLocationSettingsRender(request: HttpRequest) -> HttpResponse:
    '''
    Info:
        Renderiza la interfaz para gestionar y configurar las sedes del sistema.

    Params:
        request (HttpRequest): Objeto de solicitud HTTP para obtener información de la URL.

    Return:
        HttpResponse: Renderizado de la página de configuración de ubicaciones del dashboard.
    '''

    return render(request, 'block_content/settings/locations.html')


@login_required
def appDashboardWorkAreaSettingsRender(request: HttpRequest) -> HttpResponse:
    '''
    Info:
        Renderiza la interfaz para gestionar y configurar las áreas de trabajo del sistema.

    Params:
        request (HttpRequest): Objeto de solicitud HTTP para obtener información de la URL.

    Return:
        HttpResponse: Renderizado de la página de configuración de áreas de trabajo del dashboard.
    '''

    # Info: Renderiza la página de configuración de áreas de trabajo
    return render(request, 'block_content/settings/work_areas.html')


@login_required
def appDashboardSchedulesSettingsRender(request: HttpRequest) -> HttpResponse:
    '''
    Info:
        Renderiza la interfaz para gestionar y configurar los horarios del sistema.

    Params:
        request (HttpRequest): Objeto de solicitud HTTP para obtener información de la URL.

    Return:
        HttpResponse: Renderizado de la página de configuración de horarios del dashboard.
    '''

    return render(request, 'block_content/settings/schedules.html')


@login_required
def appDashboardTypeNewsSettingsRender(request: HttpRequest) -> HttpResponse:
    '''
    Info:
        Renderiza la interfaz para gestionar y configurar los tipos de novedades del sistema.

    Params:
        request (HttpRequest): Objeto de solicitud HTTP para obtener información de la URL.

    Return:
        HttpResponse: Renderizado de la página de configuración de tipos de novedades del dashboard.
    '''

    return render(request, 'block_content/settings/type_news.html')
