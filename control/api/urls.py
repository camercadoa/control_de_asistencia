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
]
