from django.db import models
from .empleados import Empleado

class Horario(models.Model):
    hora_entrada = models.TimeField()
    hora_salida = models.TimeField()
    miembros = models.ManyToManyField(Empleado, related_name="horarios")

    class Meta:
        db_table = "horarios"
        verbose_name = "Horario"
        verbose_name_plural = "Horarios"

    def __str__(self):
        return f"Horario de {', '.join([m.nombre_completo for m in self.miembros.all()])}"
