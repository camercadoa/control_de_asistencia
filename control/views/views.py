from django.shortcuts import render
from control.models import (
    Sede
)

# * Vista para renderizar la página principal del aplicativo
def appLobbyRender(request):
    return render(
        request,
        'lobby.html'
    )


# * Vista para renderizar la página de Guardar Registro de Asistencia
def appAssistanceRecordRender(request):
    return render(
        request,
        'registro_asistencia.html'
    )

# * Vista para renderizar el dashboard
def appDashboardRender(request):
    return render(
        request,
        'dashboard.html'
    )