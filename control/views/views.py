from django.shortcuts import render
from control.models import (
    Sede
)

# * Vista para renderizar la página principal del aplicativo
def app_lobby(request):
    sedes = Sede.objects.exclude(id=5).order_by('id')
    return render(
        request,
        'lobby.html',
        {
            'sedes': sedes
        }
    )
