from rest_framework import viewsets
from Account.models import *
from .serializers import EstadosEnviosSerializers

class estadosenviosCRUD (viewsets.ModelViewSet):
    queryset = Estadosenvios.objects.all()
    serializer_class = EstadosEnviosSerializers