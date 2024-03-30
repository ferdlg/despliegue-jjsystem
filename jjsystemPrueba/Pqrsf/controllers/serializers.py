from rest_framework import serializers
from Account.models import *

class PqrsfSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Pqrsf
        fields = '__all__'

class EstadosPqrsfSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Estadospqrsf
        fields = '__all__'

class TiposPqrsfSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Tipospqrsf
        fields = '__all__'

class RespuestaPqrsfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Respuestas
        fields = '__all__'