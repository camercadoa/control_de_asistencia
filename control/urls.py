from django.urls import path
from control import views

urlpatterns = [
    # Renderizar páginas
    path('lobby/', views.appLobbyRender, name='appLobbyRender'), # Página inicial
    path('qr-reader/', views.appQrReaderRender, name='appQrReaderRender'), # Página para uso del lector QR
    path('dashboard/home/', views.appDashboardHomeRender, name='appDashboardHomeRender'), # Dashboard principal
    path('dashboard/employees/active/', views.appDashboardActiveEmployeesRender, name='appDashboardActiveEmployeesRender'), # Gestión Empleados Activos
    path('dashboard/employees/inactive/', views.appDashboardInactiveEmployeesRender, name='appDashboardInactiveEmployeesRender'), # Gestión Empleados Inactivos
    path('dashboard/assistance-records/', views.appDashboardAssistanceRecordRender, name='appDashboardAssistanceRecordRender'), # Gestión Registros de Asistencias
    path('dashboard/news/', views.appDashboardNewsRender, name='appDashboardNewsRender'), # Gestión Novedades
    path('dashboard/settings/sedes/', views.appDashboardLocationSettingsRender, name='appDashboardLocationSettingsRender'), # CRUD de Sedes
    path('dashboard/settings/areas-trabajo/', views.appDashboardWorkAreaSettingsRender, name='appDashboardWorkAreaSettingsRender'), # CRUD de Áreas de Trabajo
    path('dashboard/settings/schedules/', views.appDashboardSchedulesSettingsRender, name='appDashboardSchedulesSettingsRender'), # CRUD de Horarios
    path('dashboard/settings/type-news/', views.appDashboardTypeNewsSettingsRender, name='appDashboardTypeNewsSettingsRender'), # CRUD de Tipos de Novedades

    # Funciones AJAX
    path('lobby/login/authentication/', views.validateAuthentication, name='validateAuthentication'), # Validar credenciales para el inicio de sesión
    path('qr-reader/define-location/', views.defineLocation, name='defineLocation'), # Guardar sede seleccionada
    path('qr-reader/save/', views.saveRecord, name='saveRecord'),

    # Cerrar sesión
    path('dashboard/logout/', views.logoutSesion, name='logoutSesion'),
]
