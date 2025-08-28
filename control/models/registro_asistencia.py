from django.db import models
from django.utils import timezone
from .empleados import Empleado
from .sedes import Sede


class RegistroAsistencia(models.Model):
    fk_empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    descripcion_registro = models.CharField(
        max_length=20, verbose_name="Descripcion")
    fecha_hora_registro = models.DateTimeField(
        default=timezone.now)  # ✅ Unificado
    lugar_registro = models.ForeignKey(Sede, on_delete=models.CASCADE)

    class Meta:
        db_table = 'registros_asistencia'
        verbose_name = 'Registro de Asistencia'
        verbose_name_plural = 'Registros de Asistencias'
