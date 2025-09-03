from django.db import models
from .empleados import Empleado

class TipoNovedad(models.Model):
    tipo = models.CharField(max_length=50)  # Permiso, Licencia, Incapacidad
    descripcion = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "tipos_novedades"
        verbose_name = "Tipo de Novedad"
        verbose_name_plural = "Tipos de Novedades"

    def __str__(self):
        return self.nombre


class NovedadAsistencia(models.Model):
    fk_empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    fk_tipo_novedad = models.ForeignKey(TipoNovedad, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    observacion = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "novedades_asistencia"
        verbose_name = "Novedad de Asistencia"
        verbose_name_plural = "Novedades de Asistencia"

    def __str__(self):
        return f"{self.fk_empleado} - {self.fk_tipo_novedad.nombre} ({self.fecha_inicio} a {self.fecha_fin})"
