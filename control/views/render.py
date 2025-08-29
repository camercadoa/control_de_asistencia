from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def appLobbyRender(request):
    # * Página Principal del Aplicativo
    return render(
        request,
        'lobby.html'
    )


def appQrReaderRender(request):
    # * Página del lector QR
    return render(
        request,
        'qr_reader.html'
    )


@login_required
def appDashboardRender(request):
    # * Dashboard
    return render(
        request,
        'dashboard.html'
    )


def appDashboardEmployeesRender(request):
    # * Dashboard -> Empleados
    return render(
        request,
        'block_content/employees.html'
    )


def appDashboardAssistanceRecordRender(request):
    # * Dashboard -> Registros de Asistencia
    return render(
        request,
        'block_content/assistance_records.html'
    )
