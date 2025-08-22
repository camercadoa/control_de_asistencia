from django.db import models
from .empleados import Empleado
from .sedes import Sede


class RegistroAsistencia(models.Model):
    fk_empleado = models.ForeignKey(
        Empleado, on_delete=models.CASCADE)
    description_registro = models.CharField(max_length=20, verbose_name="Descripcion")
    fecha_registro = models.DateField("Fecha Registro", auto_now=False, auto_now_add=True)
    hora_registro = models.TimeField("Hora Registro", auto_now=False, auto_now_add=True)
    lugar_registro = models.ForeignKey(
        Sede, on_delete=models.CASCADE)

    class Meta:
        db_table = 'registros_asistencia'
        verbose_name = 'Registro de Asistencia'
        verbose_name_plural = 'Registros de Asistencias'