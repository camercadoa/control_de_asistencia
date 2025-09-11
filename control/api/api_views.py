from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from control.models import (
    Sede, Empleado, RegistroAsistencia, CorreoInstitucional, TipoDocumento, AreaTrabajo, TipoNovedad, NovedadAsistencia, Horario
)
from .serializers import *

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

class SedeRegistroCountView(APIView):
    def get(self, request, pk):
        try:
            sede = Sede.objects.get(pk=pk)
        except Sede.DoesNotExist:
            return Response({"error": "Sede no encontrada"}, status=status.HTTP_404_NOT_FOUND)

        count = RegistroAsistencia.objects.filter(lugar_registro=sede).count()
        return Response({"sede": sede.id, "conteo": count})


# ---------------------
# Empleados API
# ---------------------

class EmpleadoListCreateView(ListAPIView):
    # Info: Lista todos los empleados o permite crear uno nuevo
    queryset = Empleado.objects.all().order_by('primer_nombre')
    serializer_class = EmpleadoSerializer


# ---------------------
# Registros de Asistencia API
# ---------------------

class RegistroAsistenciaListCreateView(ListCreateAPIView):
    queryset = RegistroAsistencia.objects.all().order_by('-fecha_hora_registro')
    serializer_class = RegistroAsistenciaSerializer


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


class TipoNovedadRegistroCountView(APIView):
    def get(self, request, pk):
        try:
            tipo_novedad = TipoNovedad.objects.get(pk=pk)
        except TipoNovedad.DoesNotExist:
            return Response({"error": "Tipo de novedad no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        count = NovedadAsistencia.objects.filter(fk_tipo_novedad=tipo_novedad).count()
        return Response({"conteo": count})


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
