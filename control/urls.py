from django.urls import path
from control import views

urlpatterns = [
    # Renderizar páginas
    path('lobby/', views.appLobbyRender, name='appLobbyRender'), # Página inicial
    path('assistance-record/', views.appAssistanceRecordRender, name='appAssistanceRecordRender'), # Página para el registro de asistencia
    path('dashboard/', views.appDashboardRender, name='appDashboardRender'), # Página inicial al iniciar sesión

    # Funciones AJAX
    path('lobby/login/authentication/', views.validateAuthentication, name='validateAuthentication'), # Validar credenciales para el inicio de sesión
    path('assistance-record/define-location/', views.defineLocation, name='defineLocation'), # Guardar sede seleccionada
    path('assistance-record/save/', views.saveRecord, name='saveRecord'),

    # Cerrar sesión
    path('dashboard/logout/', views.logoutSesion, name='logoutSesion'),
]
