from django.urls import path
from control import views

urlpatterns = [
    path('sedes/', views.SedeListCreateView.as_view(), name='ApiSedes'),
    path('sedes/<int:pk>/', views.SedeDetailView.as_view(), name='ApiSedeDetail'),
    path('empleados/', views.EmpleadoListCreateView.as_view(), name='ApiEmpleados'),
    path('empleados/<int:pk>/', views.EmpleadoDetailView.as_view(), name='ApiEmpleadoDetail'),
    path('registros-asistencias/', views.RegistroAsistenciaListCreateView.as_view(), name='ApiRegistrosAsistencias'),
    path('registros-asistencias/<int:pk>/', views.RegistroAsistenciaDetailView.as_view(), name='ApiRegistroAsistenciaDetail'),
    path('correos-institucionales/', views.CorreoInstitucionalListCreateView.as_view(), name='ApiCorreosInstitucionales'),
    path('correos-institucionales/<int:pk>/', views.CorreoInstitucionalDetailView.as_view(), name='ApiCorreoInstitucionalDetail'),
    path('tipos-documento/', views.TipoDocumentoListCreateView.as_view(), name='ApiTiposDocumento'),
    path('tipos-documento/<int:pk>/', views.TipoDocumentoDetailView.as_view(), name='ApiTipoDocumentoDetail'),
    path('areas-trabajo/', views.AreaTrabajoListCreateView.as_view(), name='ApiAreasTrabajo'),
    path('areas-trabajo/<int:pk>/', views.AreaTrabajoDetailView.as_view(), name='ApiAreaTrabajoDetail'),
    path('notificaciones/', views.NotificacionListCreateView.as_view(), name='ApiNotificaciones'),
    path('notificaciones/<int:pk>/', views.NotificacionDetailView.as_view(), name='ApiNotificacionDetail'),
    path('tipos-novedad/', views.TipoNovedadListCreateView.as_view(), name='ApiTiposNovedad'),
    path('tipos-novedad/<int:pk>/', views.TipoNovedadDetailView.as_view(), name='ApiTipoNovedadDetail'),
    path('novedades-asistencia/', views.NovedadAsistenciaListCreateView.as_view(), name='ApiNovedadesAsistencia'),
    path('novedades-asistencia/<int:pk>/', views.NovedadAsistenciaDetailView.as_view(), name='ApiNovedadAsistenciaDetail'),
]
