from django.contrib.auth.decorators import login_required
from django.shortcuts import render

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
@login_required
def appDashboardRender(request):
    return render(
        request,
        'dashboard.html'
    )