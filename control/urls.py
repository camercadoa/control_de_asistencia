from django.urls import path
from control import views

urlpatterns = [

    # Renderizar páginas
    path('app_lobby/', views.app_lobby, name='app_lobby'), # Página inicial

    # Funciones AJAX
    path('app_lobby/guardar_sede/', views.guardar_sede, name='guardar_sede'), # Guardar sede seleccionada
]
