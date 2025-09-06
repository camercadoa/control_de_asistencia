from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from control.models import (
    Sede, Empleado, RegistroAsistencia, CorreoInstitucional, TipoDocumento, AreaTrabajo, Notificacion, TipoNovedad, NovedadAsistencia
)
from control.api import *

# Sedes API
class SedeListCreateView(ListCreateAPIView):
    queryset = Sede.objects.exclude(id=5).order_by('id')
    serializer_class = SedeSerializer

class SedeDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Sede.objects.exclude(id=5).order_by('id')
    serializer_class = SedeSerializer

# Empleados API
class EmpleadoListCreateView(ListCreateAPIView):
    queryset = Empleado.objects.all().order_by('primer_nombre')
    serializer_class = EmpleadoSerializer

class EmpleadoDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Empleado.objects.all().order_by('primer_nombre')
    serializer_class = EmpleadoSerializer

# Registros de Asistencia API
class RegistroAsistenciaListCreateView(ListCreateAPIView):
    queryset = RegistroAsistencia.objects.all()
    serializer_class = RegistroAsistenciaSerializer

class RegistroAsistenciaDetailView(RetrieveUpdateDestroyAPIView):
    queryset = RegistroAsistencia.objects.all()
    serializer_class = RegistroAsistenciaSerializer

# Correo Institucional API
class CorreoInstitucionalListCreateView(ListCreateAPIView):
    queryset = CorreoInstitucional.objects.all()
    serializer_class = CorreoInstitucionalSerializer

class CorreoInstitucionalDetailView(RetrieveUpdateDestroyAPIView):
    queryset = CorreoInstitucional.objects.all()
    serializer_class = CorreoInstitucionalSerializer

# Tipo Documento API
class TipoDocumentoListCreateView(ListCreateAPIView):
    queryset = TipoDocumento.objects.all()
    serializer_class = TipoDocumentoSerializer

class TipoDocumentoDetailView(RetrieveUpdateDestroyAPIView):
    queryset = TipoDocumento.objects.all()
    serializer_class = TipoDocumentoSerializer

# Area de Trabajo API
class AreaTrabajoListCreateView(ListCreateAPIView):
    queryset = AreaTrabajo.objects.all()
    serializer_class = AreaTrabajoSerializer

class AreaTrabajoDetailView(RetrieveUpdateDestroyAPIView):
    queryset = AreaTrabajo.objects.all()
    serializer_class = AreaTrabajoSerializer

# Notificaciones API
class NotificacionListCreateView(ListCreateAPIView):
    queryset = Notificacion.objects.all().order_by('-fecha_creacion')
    serializer_class = NotificacionSerializer

class NotificacionDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Notificacion.objects.all().order_by('-fecha_creacion')
    serializer_class = NotificacionSerializer

# Tipo Novedad API
class TipoNovedadListCreateView(ListCreateAPIView):
    queryset = TipoNovedad.objects.all()
    serializer_class = TipoNovedadSerializer

class TipoNovedadDetailView(RetrieveUpdateDestroyAPIView):
    queryset = TipoNovedad.objects.all()
    serializer_class = TipoNovedadSerializer

# Novedad Asistencia API
class NovedadAsistenciaListCreateView(ListCreateAPIView):
    queryset = NovedadAsistencia.objects.all()
    serializer_class = NovedadAsistenciaSerializer

class NovedadAsistenciaDetailView(RetrieveUpdateDestroyAPIView):
    queryset = NovedadAsistencia.objects.all()
    serializer_class = NovedadAsistenciaSerializer