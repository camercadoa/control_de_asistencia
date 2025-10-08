from django.db import models


class Sede(models.Model):
    id = models.AutoField(primary_key=True)
    ubicacion = models.CharField(max_length=255, null=True, blank=True)
    ciudad = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'sedes'
        verbose_name = 'Sede'
        verbose_name_plural = 'Sedes'
        managed = False

    def __str__(self):
        return f"{self.ubicacion}"
