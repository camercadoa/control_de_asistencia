from django.shortcuts import render
from control.models import (
    Sede
)

# * Vista para renderizar la página principal del aplicativo
def AppLobby(request):
    return render(
        request,
        'lobby.html'
    )


# * Vista para renderizar la página de Guardar Registro de Asistencia
def RegistroAsistencia(request):
    sedes = Sede.objects.exclude(id=5).order_by('id')
    return render(
        request,
        'registro_asistencia.html',
        {
            'sedes': sedes
        }
    )

# * Vista para renderizar el dashboard
def Dashboard(request):
    return render(
        request,
        'dashboard.html'
    )