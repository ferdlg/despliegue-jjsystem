from rest_framework import serializers
from Account.models import *

class EnviosSerializers(serializers.ModelSerializer):
    class Meta:
        model = Envios
        fields = '__all__'

class TecnicosSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tecnicos
        fields = '__all__'

class EstadosEnviosSerializers(serializers.ModelSerializer):
    class Meta:
        model = Estadosenvios
        fields = '__all__'

class VentasSerializers(serializers.ModelSerializer):
    class Meta:
        model = Ventas
        fields = '__all__'