from django.urls import path
from control import views

urlpatterns = [
    # Renderizar páginas
    path('app-lobby/', views.AppLobby, name='AppLobby'), # Página inicial
    path('registro-asistencia/', views.RegistroAsistencia, name='RegistroAsistencia'), # Página para el registro de asistencia
    path('dashboard/', views.Dashboard, name='Dashboard'), # Página inicial al iniciar sesión

    # Funciones AJAX
    path('app-lobby/login/validar-usuario/', views.IniciarSesion, name='IniciarSesion'), # Validar credenciales para el inicio de sesión
    path('registro-asistencia/guardar-sede/', views.GuardarSede, name='GuardarSede'), # Guardar sede seleccionada
    path('registro-asistencia/guardar-registro/', views.GuardarRegistro, name='guardarRegistro'),

    # Cerrar sesión
    path('cerrar-sesion/', views.CerrarSesion, name='CerrarSesion'),
]
