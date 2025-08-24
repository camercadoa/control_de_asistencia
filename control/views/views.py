from django.shortcuts import render
from control.models import (
    Sede
)

# * Vista para renderizar la página principal del aplicativo
def appLobby(request):
    return render(
        request,
        'lobby.html'
    )


# * Vista para renderizar la página principal del aplicativo
def registroAsistencia(request):
    sedes = Sede.objects.exclude(id=5).order_by('id')
    return render(
        request,
        'registro_asistencia.html',
        {
            'sedes': sedes
        }
    )


def dashboard(request):
    return render(
        request,
        'dashboard.html'
    )