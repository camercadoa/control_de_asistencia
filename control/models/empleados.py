# Modulos
from django.db import models

class Empleados(models.Model):
    cargo = models.CharField(max_length=255)
    primer_nombre = models.CharField(max_length=255)
    segundo_nombre = models.CharField(max_length=255, blank=True, null=True)
    primer_apellido = models.CharField(max_length=255)
    segundo_apellido = models.CharField(max_length=255, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    lugar_nacimiento = models.CharField(max_length=255, blank=True, null=True)
    numero_documento = models.BigIntegerField(unique=True)
    fecha_expedicion_documento = models.DateField(blank=True, null=True)
    lugar_expedicion_documento = models.CharField(max_length=255, blank=True, null=True)
    sexo = models.CharField(max_length=50, blank=True, null=True)
    telefono_fijo = models.CharField(max_length=15, blank=True, null=True)
    celular = models.CharField(max_length=15, blank=True, null=True)
    correo_personal = models.CharField(max_length=254)
    estado_civil = models.CharField(max_length=255, blank=True, null=True)
    direccion_residencia = models.CharField(max_length=255, blank=True, null=True)
    ciudad_residencia = models.CharField(max_length=255, blank=True, null=True)
    barrio_residencia = models.CharField(max_length=255, blank=True, null=True)
    activo = models.BooleanField()
    fecha_creacion = models.DateTimeField()
    fecha_modificacion = models.DateTimeField()
    fk_creado_por = models.ForeignKey('AuthUser', models.DO_NOTHING, blank=True, null=True)
    fk_modificado_por = models.ForeignKey('AuthUser', models.DO_NOTHING, related_name='empleados_fk_modificado_por_set', blank=True, null=True)
    fk_rol = models.ForeignKey('Roles', models.DO_NOTHING)
    fk_tipo_documento = models.ForeignKey('TipoDocumentos', models.DO_NOTHING)
    url_hoja_de_vida = models.CharField(max_length=200, blank=True, null=True)
    fk_eps = models.ForeignKey('Eps', models.DO_NOTHING, blank=True, null=True)
    fk_ultimo_nivel_estudio = models.ForeignKey('NivelesAcademicos', models.DO_NOTHING, blank=True, null=True)
    fk_afp = models.ForeignKey('Afp', models.DO_NOTHING, blank=True, null=True)
    fk_arl = models.ForeignKey('Arl', models.DO_NOTHING, blank=True, null=True)
    fk_caja_compensacion = models.ForeignKey('CajasCompensacion', models.DO_NOTHING, blank=True, null=True)
    fk_departamento_residencia = models.ForeignKey('Departamentos', models.DO_NOTHING, blank=True, null=True)
    fk_sede_donde_labora = models.ForeignKey('Sedes', models.DO_NOTHING, blank=True, null=True)
    fk_estado_revision = models.ForeignKey('EstadoRevision', models.DO_NOTHING, blank=True, null=True)
    fk_pais_nacimiento = models.ForeignKey('Paises', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'empleados'