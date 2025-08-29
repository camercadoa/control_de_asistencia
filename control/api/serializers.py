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
    class Meta:
        model = Empleado
        fields = '__all__'

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