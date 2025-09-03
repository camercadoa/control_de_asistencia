from django.db import models
from .empleados import Empleado

class Notificacion(models.Model):
    fk_empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, null=True, blank=True)
    mensaje = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    leido = models.BooleanField(default=False)
    observacion = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "notificaciones"
        verbose_name = "Notificación"
        verbose_name_plural = "Notificaciones"

    def __str__(self):
        return f"{self.mensaje[:30]}..."
