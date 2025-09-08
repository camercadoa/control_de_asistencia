from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from control.models import (
    Sede, Empleado, RegistroAsistencia, CorreoInstitucional, TipoDocumento, AreaTrabajo, Notificacion, TipoNovedad, NovedadAsistencia, Horario
)
from .serializers import *
from django.utils.timezone import now


# ---------------------
# Sedes API
# ---------------------

class SedeListCreateView(ListCreateAPIView):
    # Info: Lista todas las sedes (excepto id=5) o permite crear una nueva sede
    queryset = Sede.objects.exclude(id=5).order_by('id')
    serializer_class = SedeSerializer


class SedeDetailView(RetrieveUpdateDestroyAPIView):
    # Info: Obtiene, actualiza o elimina una sede específica (excepto id=5)
    queryset = Sede.objects.exclude(id=5).order_by('id')
    serializer_class = SedeSerializer


# ---------------------
# Empleados API
# ---------------------

class EmpleadoListCreateView(ListCreateAPIView):
    # Info: Lista todos los empleados o permite crear uno nuevo
    queryset = Empleado.objects.all().order_by('primer_nombre')
    serializer_class = EmpleadoSerializer


class EmpleadoDetailView(RetrieveUpdateDestroyAPIView):
    # Info: Obtiene, actualiza o elimina un empleado específico
    queryset = Empleado.objects.all().order_by('primer_nombre')
    serializer_class = EmpleadoSerializer


# ---------------------
# Registros de Asistencia API
# ---------------------

class RegistroAsistenciaListCreateView(ListCreateAPIView):
    queryset = RegistroAsistencia.objects.all().order_by('-fecha_hora_registro')
    serializer_class = RegistroAsistenciaSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        hoy = now().date()
        return queryset.filter(fecha_hora_registro__date=hoy).order_by('-fecha_hora_registro')


class RegistroAsistenciaDetailView(RetrieveUpdateDestroyAPIView):
    # Info: Obtiene, actualiza o elimina un registro de asistencia específico
    queryset = RegistroAsistencia.objects.all().order_by('-fecha_hora_registro')
    serializer_class = RegistroAsistenciaSerializer


# ---------------------
# Correo Institucional API
# ---------------------

class CorreoInstitucionalListCreateView(ListCreateAPIView):
    # Info: Lista todos los correos institucionales o permite crear uno nuevo
    queryset = CorreoInstitucional.objects.all()
    serializer_class = CorreoInstitucionalSerializer


class CorreoInstitucionalDetailView(RetrieveUpdateDestroyAPIView):
    # Info: Obtiene, actualiza o elimina un correo institucional específico
    queryset = CorreoInstitucional.objects.all()
    serializer_class = CorreoInstitucionalSerializer


# ---------------------
# Tipo Documento API
# ---------------------

class TipoDocumentoListCreateView(ListCreateAPIView):
    # Info: Lista todos los tipos de documento o permite crear uno nuevo
    queryset = TipoDocumento.objects.all()
    serializer_class = TipoDocumentoSerializer


class TipoDocumentoDetailView(RetrieveUpdateDestroyAPIView):
    # Info: Obtiene, actualiza o elimina un tipo de documento específico
    queryset = TipoDocumento.objects.all()
    serializer_class = TipoDocumentoSerializer


# ---------------------
# Área de Trabajo API
# ---------------------

class AreaTrabajoListCreateView(ListCreateAPIView):
    # Info: Lista todas las áreas de trabajo o permite crear una nueva
    queryset = AreaTrabajo.objects.all()
    serializer_class = AreaTrabajoSerializer


class AreaTrabajoDetailView(RetrieveUpdateDestroyAPIView):
    # Info: Obtiene, actualiza o elimina un área de trabajo específica
    queryset = AreaTrabajo.objects.all()
    serializer_class = AreaTrabajoSerializer


# ---------------------
# Notificaciones API
# ---------------------

class NotificacionListCreateView(ListCreateAPIView):
    # Info: Lista todas las notificaciones (ordenadas por fecha descendente) o permite crear una nueva
    queryset = Notificacion.objects.all().order_by('-fecha_creacion')
    serializer_class = NotificacionSerializer


class NotificacionDetailView(RetrieveUpdateDestroyAPIView):
    # Info: Obtiene, actualiza o elimina una notificación específica
    queryset = Notificacion.objects.all().order_by('-fecha_creacion')
    serializer_class = NotificacionSerializer


# ---------------------
# Tipo Novedad API
# ---------------------

class TipoNovedadListCreateView(ListCreateAPIView):
    # Info: Lista todos los tipos de novedad o permite crear uno nuevo
    queryset = TipoNovedad.objects.all()
    serializer_class = TipoNovedadSerializer


class TipoNovedadDetailView(RetrieveUpdateDestroyAPIView):
    # Info: Obtiene, actualiza o elimina un tipo de novedad específico
    queryset = TipoNovedad.objects.all()
    serializer_class = TipoNovedadSerializer


# ---------------------
# Novedad Asistencia API
# ---------------------

class NovedadAsistenciaListCreateView(ListCreateAPIView):
    # Info: Lista todas las novedades de asistencia o permite crear una nueva
    queryset = NovedadAsistencia.objects.all()
    serializer_class = NovedadAsistenciaSerializer


class NovedadAsistenciaDetailView(RetrieveUpdateDestroyAPIView):
    # Info: Obtiene, actualiza o elimina una novedad de asistencia específica
    queryset = NovedadAsistencia.objects.all()
    serializer_class = NovedadAsistenciaSerializer


# ---------------------
# Horario API
# ---------------------

class HorarioListCreateView(ListCreateAPIView):
    # Info: Lista todos los horarios o permite crear uno nuevo
    queryset = Horario.objects.all()
    serializer_class = HorarioSerializer


class HorarioDetailView(RetrieveUpdateDestroyAPIView):
    # Info: Obtiene, actualiza o elimina un horario específico
    queryset = Horario.objects.all()
    serializer_class = HorarioSerializer
