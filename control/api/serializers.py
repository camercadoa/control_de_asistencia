from rest_framework import serializers
from django.utils.timezone import localtime
from control.models import (
    Sede, Empleado, RegistroAsistencia, CorreoInstitucional, TipoDocumento, AreaTrabajo, TipoNovedad, NovedadAsistencia, Horario
)

# ---------------------
# Sedes Serializer
# ---------------------

class SedeSerializer(serializers.ModelSerializer):
    # Info: Serializer para el modelo Sede
    class Meta:
        model = Sede
        fields = '__all__'


# ---------------------
# Empleados Serializer
# ---------------------

class EmpleadoSerializer(serializers.ModelSerializer):
    # Info: Serializer para el modelo Empleado
    documento = serializers.SerializerMethodField()
    nombre_completo = serializers.SerializerMethodField()
    correo_institucional = serializers.SerializerMethodField()

    class Meta:
        model = Empleado
        fields = ["id", "nombre_completo", "cargo", "activo", "documento", "correo_institucional"]

    def get_documento(self, obj):
        # Info: Devuelve el documento del empleado en formato "Tipo - Número"
        numero = f"{obj.numero_documento:,}".replace(",", ".")
        return f"{obj.fk_tipo_documento.tipo_documento} - {numero}"

    def get_nombre_completo(self, obj):
        # Info: Devuelve el nombre completo del empleado
        return f"{obj.primer_apellido} {obj.segundo_apellido or ''} {obj.primer_nombre} {obj.segundo_nombre or ''}".strip()

    def get_correo_institucional(self, obj):
        # Info: Devuelve el correo institucional del empleado si existe
        correo = CorreoInstitucional.objects.filter(fk_empleado=obj).first()
        return correo.correo_institucional if correo else None


# ---------------------
# Registro de Asistencia Serializer
# ---------------------

class RegistroAsistenciaSerializer(serializers.ModelSerializer):
    # Info: Serializer para el modelo RegistroAsistencia
    fecha = serializers.SerializerMethodField()
    hora = serializers.SerializerMethodField()
    nombre_empleado = serializers.SerializerMethodField()
    documento = serializers.SerializerMethodField()
    lugar_registro = serializers.SerializerMethodField()
    fk_empleado = serializers.PrimaryKeyRelatedField(read_only=True)
    fk_areas_trabajo = serializers.SerializerMethodField()
    fk_sede = serializers.PrimaryKeyRelatedField(source="lugar_registro", read_only=True)

    class Meta:
        model = RegistroAsistencia
        fields = ["id", "nombre_empleado", "documento", "fecha", "hora", "descripcion_registro", "lugar_registro", "fk_empleado", "fk_areas_trabajo","fk_sede", "minutos", "estado_registro"]

    def get_fecha(self, obj):
        return localtime(obj.fecha_hora_registro).strftime("%d/%m/%Y")

    def get_hora(self, obj):
        return localtime(obj.fecha_hora_registro).strftime("%I:%M:%S %p")

    def get_nombre_empleado(self, obj):
        return f"{obj.fk_empleado.primer_apellido} {obj.fk_empleado.segundo_apellido or ''} {obj.fk_empleado.primer_nombre}".strip()

    def get_documento(self, obj):
        numero = f"{obj.fk_empleado.numero_documento:,}".replace(",", ".")
        return f"{obj.fk_empleado.fk_tipo_documento.tipo_documento} - {numero}"

    def get_lugar_registro(self, obj):
        sede = f'{obj.lugar_registro.ubicacion} - {obj.lugar_registro.ciudad}'
        return sede if obj.lugar_registro else None

    def get_fk_areas_trabajo(self, obj):
        # Devuelve lista de IDs de áreas
        return list(obj.fk_empleado.grupos.values_list("id", flat=True))


# ---------------------
# Correo Institucional Serializer
# ---------------------

class CorreoInstitucionalSerializer(serializers.ModelSerializer):
    # Info: Serializer para el modelo CorreoInstitucional
    class Meta:
        model = CorreoInstitucional
        fields = '__all__'


# ---------------------
# Tipo Documento Serializer
# ---------------------

class TipoDocumentoSerializer(serializers.ModelSerializer):
    # Info: Serializer para el modelo TipoDocumento
    class Meta:
        model = TipoDocumento
        fields = '__all__'


# ---------------------
# Área de Trabajo Serializer
# ---------------------

class AreaTrabajoSerializer(serializers.ModelSerializer):
    # Info: Serializer para el modelo AreaTrabajo
    miembros = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Empleado.objects.all(),
        required=False
    )
    miembros_info = EmpleadoSerializer(source="miembros", many=True, read_only=True)

    class Meta:
        model = AreaTrabajo
        fields = ["id", "area", "descripcion", "miembros", "miembros_info"]

    def update(self, instance, validated_data):
        # Info: Actualiza los miembros del área de trabajo
        miembros_data = validated_data.pop('miembros', None)
        instance = super().update(instance, validated_data)
        if miembros_data is not None:
            instance.miembros.set(miembros_data)
        return instance


# ---------------------
# Tipo Novedad Serializer
# ---------------------

class TipoNovedadSerializer(serializers.ModelSerializer):
    # Info: Serializer para el modelo TipoNovedad
    class Meta:
        model = TipoNovedad
        fields = '__all__'


# ---------------------
# Novedad de Asistencia Serializer
# ---------------------

class NovedadAsistenciaSerializer(serializers.ModelSerializer):
    # Info: Serializer para el modelo NovedadAsistencia
    nombre_empleado = serializers.SerializerMethodField()
    tipo_novedad = serializers.SerializerMethodField()

    class Meta:
        model = NovedadAsistencia
        fields = ['id', 'fk_empleado', 'fk_tipo_novedad', 'nombre_empleado', 'tipo_novedad', 'fecha_inicio', 'fecha_fin', 'observacion']

    def get_nombre_empleado(self, obj):
        return f"{obj.fk_empleado.primer_apellido} {obj.fk_empleado.segundo_apellido or ''} {obj.fk_empleado.primer_nombre}".strip()

    def get_tipo_novedad(self, obj):
        return obj.fk_tipo_novedad.tipo


# ---------------------
# Horario Serializer
# ---------------------

class HorarioSerializer(serializers.ModelSerializer):
    # Info: Serializer para el modelo Horario
    hora_entrada = serializers.TimeField()
    hora_salida = serializers.TimeField()
    miembros = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Empleado.objects.all(),
        required=False
    )
    miembros_info = EmpleadoSerializer(source="miembros", many=True, read_only=True)

    class Meta:
        model = Horario
        fields = ["id", "hora_entrada", "hora_salida", "miembros", "miembros_info"]

    def update(self, instance, validated_data):
        # Info: Actualiza los miembros del horario
        miembros_data = validated_data.pop('miembros', None)
        instance = super().update(instance, validated_data)
        if miembros_data is not None:
            instance.miembros.set(miembros_data)
        return instance