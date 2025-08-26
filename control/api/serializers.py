from rest_framework import serializers
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
    class Meta:
        model = RegistroAsistencia
        fields = '__all__'

class CorreoInstitucionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = CorreoInstitucional
        fields = '__all__'

class TipoDocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoDocumento
        fields = '__all__'