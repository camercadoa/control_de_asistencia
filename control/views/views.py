from django.shortcuts import render
from control.models import (
    Sede
)

# * Vista para cargar la página principal del aplicativo
def app_lobby(request):
    sedes = Sede.objects.exclude(id=5)
    return render(
        request,
        'lobby.html',
        {
            'sedes': sedes
        }
    )
