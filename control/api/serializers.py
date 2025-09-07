from rest_framework import serializers
from django.utils.timezone import localtime
from control.models import (
    Sede, Empleado, RegistroAsistencia, CorreoInstitucional, TipoDocumento, AreaTrabajo, Notificacion, TipoNovedad, NovedadAsistencia
)


class SedeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sede
        fields = '__all__'


class EmpleadoSerializer(serializers.ModelSerializer):
    documento = serializers.SerializerMethodField()
    nombre_completo = serializers.SerializerMethodField()
    correo_institucional = serializers.SerializerMethodField()

    class Meta:
        model = Empleado
        fields = ["id", "nombre_completo", "cargo", "activo", "documento", "correo_institucional"]

    def get_documento(self, obj):
        numero = f"{obj.numero_documento:,}".replace(",", ".")
        return f"{obj.fk_tipo_documento.tipo_documento} - {numero}"

    def get_nombre_completo(self, obj):
        return f"{obj.primer_nombre} {obj.segundo_nombre or ''} {obj.primer_apellido} {obj.segundo_apellido or ''}".strip()

    def get_correo_institucional(self, obj):
        correo = CorreoInstitucional.objects.filter(fk_empleado=obj).first()
        return correo.correo_institucional if correo else None


class RegistroAsistenciaSerializer(serializers.ModelSerializer):
    fecha = serializers.SerializerMethodField()
    hora = serializers.SerializerMethodField()
    nombre_empleado = serializers.SerializerMethodField()
    documento = serializers.SerializerMethodField()
    lugar_registro = serializers.SerializerMethodField()
    fk_empleado = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = RegistroAsistencia
        fields = [
            "id", "nombre_empleado", "documento", "fecha",
            "hora", "descripcion_registro", "lugar_registro", "fk_empleado"
        ]

    def get_fecha(self, obj):
        return localtime(obj.fecha_hora_registro).strftime("%d/%m/%Y")

    def get_hora(self, obj):
        return localtime(obj.fecha_hora_registro).strftime("%I:%M:%S %p")

    def get_nombre_empleado(self, obj):
        return f"{obj.fk_empleado.primer_nombre} {obj.fk_empleado.primer_apellido} {obj.fk_empleado.segundo_apellido or ''}".strip()

    def get_documento(self, obj):
        numero = f"{obj.fk_empleado.numero_documento:,}".replace(",", ".")
        return f"{obj.fk_empleado.fk_tipo_documento.tipo_documento} - {numero}"


    def get_lugar_registro(self, obj):
        sede = f'{obj.lugar_registro.ubicacion} - {obj.lugar_registro.ciudad}'
        return sede if obj.lugar_registro else None


class CorreoInstitucionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = CorreoInstitucional
        fields = '__all__'


class TipoDocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoDocumento
        fields = '__all__'


class AreaTrabajoSerializer(serializers.ModelSerializer):
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
        miembros_data = validated_data.pop('miembros', None)
        instance = super().update(instance, validated_data)
        if miembros_data is not None:
            instance.miembros.set(miembros_data)  # ⚡ Actualiza ManyToMany
        return instance



class NotificacionSerializer(serializers.ModelSerializer):
    fecha_creacion = serializers.SerializerMethodField()

    class Meta:
        model = Notificacion
        fields = '__all__'

    def get_fecha_creacion(self, obj):
        return localtime(obj.fecha_creacion).strftime("%d/%m/%Y %I:%M:%S %p")


class TipoNovedadSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoNovedad
        fields = '__all__'


class NovedadAsistenciaSerializer(serializers.ModelSerializer):
    fecha_inicio = serializers.SerializerMethodField()
    fecha_fin = serializers.SerializerMethodField()

    class Meta:
        model = NovedadAsistencia
        fields = '__all__'

    def get_fecha_inicio(self, obj):
        return obj.fecha_inicio.strftime("%d/%m/%Y")

    def get_fecha_fin(self, obj):
        return obj.fecha_fin.strftime("%d/%m/%Y")
