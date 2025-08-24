from django.db import models


class TipoDocumento(models.Model):
    id = models.AutoField(primary_key=True)
    tipo_documento = models.CharField(max_length=255)
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'tipo_documentos'
        verbose_name = 'Tipo de Documento'
        verbose_name_plural = 'Tipos de Documentos'

    def __str__(self):
        return f"{self.tipo_documento} - {self.descripcion}"


class Empleado(models.Model):
    # Campos obligatorios
    id = models.AutoField(primary_key=True)
    cargo = models.CharField(max_length=255)
    primer_nombre = models.CharField(max_length=255)
    primer_apellido = models.CharField(max_length=255)
    fk_tipo_documento = models.ForeignKey(
        TipoDocumento, on_delete=models.CASCADE)
    numero_documento = models.BigIntegerField(unique=True)
    correo_personal = models.EmailField()

# Campos opcionales
    segundo_nombre = models.CharField(
        max_length=255, null=True, blank=True)
    segundo_apellido = models.CharField(
        max_length=255, null=True, blank=True)
    # True = Activo - False = Inactivo
    activo = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'empleados'
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'

    def __str__(self):
        return f"{self.primer_nombre} {self.primer_apellido} - {self.fk_tipo_documento.tipo_documento} {self.numero_documento}"


class CorreoInstitucional(models.Model):
    fk_empleado = models.ForeignKey(
        Empleado, on_delete=models.CASCADE)
    correo_institucional = models.EmailField(verbose_name='Correo Institucional')

    class Meta:
        verbose_name = "Correo Institucional"
        verbose_name_plural = "Correo Institucionales"

    def __str__(self):
        return f"{self.fk_empleado.primer_nombre} {self.fk_empleado.primer_apellido} - {self.correo_institucional}"

