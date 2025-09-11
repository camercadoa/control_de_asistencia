from django.urls import path
from .api_views import *

urlpatterns = [
    path('sedes/', SedeListCreateView.as_view(), name='ApiSedes'),
    path('sedes/<int:pk>/', SedeDetailView.as_view(), name='ApiSedeDetail'),
    path('sedes/<int:pk>/conteo-registros/', SedeRegistroCountView.as_view(), name='ApiSedeRegistroCount'),
    path('empleados/', EmpleadoListCreateView.as_view(), name='ApiEmpleados'),
    path('empleados/<int:pk>/', EmpleadoDetailView.as_view(), name='ApiEmpleadoDetail'),
    path('registros-asistencias/', RegistroAsistenciaListCreateView.as_view(), name='ApiRegistrosAsistencias'),
    path('registros-asistencias/<int:pk>/', RegistroAsistenciaDetailView.as_view(), name='ApiRegistroAsistenciaDetail'),
    path('correos-institucionales/', CorreoInstitucionalListCreateView.as_view(), name='ApiCorreosInstitucionales'),
    path('correos-institucionales/<int:pk>/', CorreoInstitucionalDetailView.as_view(), name='ApiCorreoInstitucionalDetail'),
    path('tipos-documento/', TipoDocumentoListCreateView.as_view(), name='ApiTiposDocumento'),
    path('tipos-documento/<int:pk>/', TipoDocumentoDetailView.as_view(), name='ApiTipoDocumentoDetail'),
    path('areas-trabajo/', AreaTrabajoListCreateView.as_view(), name='ApiAreasTrabajo'),
    path('areas-trabajo/<int:pk>/', AreaTrabajoDetailView.as_view(), name='ApiAreaTrabajoDetail'),
    path('tipos-novedad/', TipoNovedadListCreateView.as_view(), name='ApiTiposNovedad'),
    path('tipos-novedad/<int:pk>/', TipoNovedadDetailView.as_view(), name='ApiTipoNovedadDetail'),
    path('tipos-novedad/<int:pk>/conteo-registros/', TipoNovedadRegistroCountView.as_view(), name='TipoNovedadRegistroCount'),
    path('novedades-asistencia/', NovedadAsistenciaListCreateView.as_view(), name='ApiNovedadesAsistencia'),
    path('novedades-asistencia/<int:pk>/', NovedadAsistenciaDetailView.as_view(), name='ApiNovedadAsistenciaDetail'),
    path('horarios/', HorarioListCreateView.as_view(), name='ApiHorarios'),
    path('horarios/<int:pk>/', HorarioDetailView.as_view(), name='ApiHorarioDetail'),
]
