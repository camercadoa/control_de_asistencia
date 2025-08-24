from django.urls import path
from control import views

urlpatterns = [

    # Renderizar páginas
    path('app-lobby/', views.appLobby, name='AppLobby'), # Página inicial
    path('registro-asistencia/', views.registroAsistencia, name='RegistroAsistencia'), # Página para el registro de asistencia
    path('dashboard/', views.dashboard, name='Dashboard'), # Página inicial al iniciar sesión

    # Funciones AJAX
    path('app-lobby/login/validar-usuario/', views.iniciarSesion, name='IniciarSesion'), # Validar credenciales para el inicio de sesión
    path('registro-asistencia/guardar-sede/', views.guardarSede, name='GuardarSede'), # Guardar sede seleccionada

    # Cerrar sesión
    path('cerrar-sesion/', views.cerrarSesion, name='CerrarSesion'),
]
