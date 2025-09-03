from django.db import models
from .empleados import Empleado

class AreaTrabajo(models.Model):
    area = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    miembros = models.ManyToManyField(Empleado, related_name="grupos")

    class Meta:
        db_table = "grupos_trabajo"
        verbose_name = "Grupo de Trabajo"
        verbose_name_plural = "Grupos de Trabajo"

    def __str__(self):
        return self.area
