from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta
from .empleados import Empleado
from .sedes import Sede

class RegistroAsistencia(models.Model):
    fk_empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    descripcion_registro = models.CharField(
        max_length=20,
        verbose_name="Descripción",
        help_text="Entrada o Salida"
    )
    fecha_hora_registro = models.DateTimeField(default=timezone.now)
    lugar_registro = models.ForeignKey(Sede, on_delete=models.CASCADE)
    registro_atraso = models.IntegerField(null=True, blank=True)
    registro_salida_anticipada = models.IntegerField(null=True, blank=True)
    estado_registro = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'registros_asistencia'
        verbose_name = 'Registro de Asistencia'
        verbose_name_plural = 'Registros de Asistencias'

    def __str__(self):
        return f"{self.fk_empleado} - {self.descripcion_registro} - {self.fecha_hora_registro}"
