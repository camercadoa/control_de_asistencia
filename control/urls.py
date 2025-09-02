from django.urls import path
from control import views

urlpatterns = [
    # Renderizar páginas
    path('lobby/', views.appLobbyRender, name='appLobbyRender'), # Página inicial
    path('qr-reader/', views.appQrReaderRender, name='appQrReaderRender'), # Página para uso del lector QR
    path('dashboard/home/', views.appDashboardHomeRender, name='appDashboardHomeRender'), # Dashboard
    path('dashboard/employees/', views.appDashboardEmployeesRender, name='appDashboardEmployeesRender'), # Gestión Empleados
    path('dashboard/assistance-records/', views.appDashboardAssistanceRecordRender, name='appDashboardAssistanceRecordRender'), # Gestión Registros de Asistencias

    # Funciones AJAX
    path('lobby/login/authentication/', views.validateAuthentication, name='validateAuthentication'), # Validar credenciales para el inicio de sesión
    path('qr-reader/define-location/', views.defineLocation, name='defineLocation'), # Guardar sede seleccionada
    path('qr-reader/save/', views.saveRecord, name='saveRecord'),

    # Cerrar sesión
    path('dashboard/logout/', views.logoutSesion, name='logoutSesion'),
]
