import qrcode
from io import BytesIO
from email.mime.image import MIMEImage
from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveAPIView
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


class EmpleadoDetailView(RetrieveAPIView):
    # Info: Obtiene un empleado específico
    queryset = Empleado.objects.all()
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


class QRGeneratorView(APIView):
    def get(self, request, empleado_id):
        try:
            empleado = Empleado.objects.get(id=empleado_id)
            # Extraer solo el número del documento
            numero_documento = empleado.numero_documento

            # Crear QR
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(str(numero_documento))
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)

            # Devolver imagen
            return HttpResponse(buffer.getvalue(), content_type='image/png')

        except Empleado.DoesNotExist:
            return Response({"error": "Empleado no encontrado"}, status=404)


from email.mime.image import MIMEImage

class QREmailView(APIView):
    def post(self, request, empleado_id):
        try:
            empleado = Empleado.objects.get(id=empleado_id)
            correo = CorreoInstitucional.objects.get(fk_empleado=empleado)

            # Crear QR
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(str(empleado.numero_documento))
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)

            # Email
            asunto = "Código QR para Control de Asistencia - Unicorsalud"

            cuerpo_texto = f"""
Estimado/a {empleado.primer_nombre.title()} {empleado.primer_apellido.title()},

Le saludamos cordialmente desde el Sistema de Control de Asistencia de Unicorsalud.

Adjunto a este correo encontrará su código QR personal para el registro de entrada y salida en nuestras instalaciones. Este código es único e intransferible.

INSTRUCCIONES DE USO:
• Presente el código QR en los lectores ubicados en las entradas principales
• Mantenga el código visible y en buen estado
• En caso de pérdida o daño, contacte al departamento de Talento Humano

IMPORTANTE: Este es un correo automático generado por nuestro sistema. Por favor, no responda a este mensaje.

Si tiene alguna consulta o inconveniente, puede contactarnos a través de los canales oficiales de comunicación.

Atentamente,

Sistema de Control de Asistencia
Unicorsalud

---
Este mensaje y sus adjuntos son confidenciales y están dirigidos exclusivamente al destinatario indicado.
            """

            # HTML
            cuerpo_html = render_to_string(
                "utilities/mail_qr.html",
                {"empleado": empleado}
            )

            # Crear email con alternativa HTML
            email = EmailMultiAlternatives(
                subject=asunto,
                body=cuerpo_texto,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[correo.correo_institucional],
            )
            email.attach_alternative(cuerpo_html, "text/html")

            # Adjuntar QR como imagen inline (para cid:qr_code)
            qr_img = MIMEImage(buffer.getvalue())
            qr_img.add_header("Content-ID", "<qr_code>")
            qr_img.add_header("Content-Disposition", "inline", filename=f"QR_Asistencia_{empleado.numero_documento}.png")
            email.attach(qr_img)

            # Enviar correo
            email.send()

            return Response({
                "message": f"Código QR enviado exitosamente a {correo.correo_institucional}",
                "empleado": f"{empleado.primer_nombre} {empleado.primer_apellido}",
                "documento": empleado.numero_documento
            }, status=200)

        except Empleado.DoesNotExist:
            return Response({
                "error": "Empleado no encontrado",
                "codigo": "EMPLEADO_NOT_FOUND"
            }, status=404)
        except CorreoInstitucional.DoesNotExist:
            return Response({
                "error": "El empleado no tiene correo institucional registrado",
                "codigo": "EMAIL_NOT_FOUND"
            }, status=404)
        except Exception as e:
            return Response({
                "error": f"Error interno del servidor: {str(e)}",
                "codigo": "INTERNAL_ERROR"
            }, status=500)