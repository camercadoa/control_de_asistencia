from rest_framework import serializers
from django.utils.timezone import localtime
from control.models import (
    Sede, Empleado, RegistroAsistencia, CorreoInstitucional, TipoDocumento
)

class SedeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sede
        fields = '__all__'

class EmpleadoSerializer(serializers.ModelSerializer):
    documento = serializers.SerializerMethodField()
    nombre_completo = serializers.SerializerMethodField()

    class Meta:
        model = Empleado
        fields = ["id", "nombre_completo", "cargo", "activo", "documento"]

    def get_documento(self, obj):
        numero = f"{obj.numero_documento:,}".replace(",", ".")
        return f"{obj.fk_tipo_documento.tipo_documento} - {numero}"

    def get_nombre_completo(self, obj):
        return f"{obj.primer_nombre} {obj.segundo_nombre or ''} {obj.primer_apellido} {obj.segundo_apellido or ''}".strip()

class RegistroAsistenciaSerializer(serializers.ModelSerializer):
    fecha = serializers.SerializerMethodField()
    hora = serializers.SerializerMethodField()

    class Meta:
        model = RegistroAsistencia
        fields = '__all__'

    def get_fecha(self, obj):
        return localtime(obj.fecha_hora_registro).strftime("%d/%m/%Y")

    def get_hora(self, obj):
        return localtime(obj.fecha_hora_registro).strftime("%I:%M:%S %p")

class CorreoInstitucionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = CorreoInstitucional
        fields = '__all__'

class TipoDocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoDocumento
        fields = '__all__'