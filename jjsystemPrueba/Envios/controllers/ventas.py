from rest_framework import viewsets
from Account.models import *
from .serializers import VentasSerializers

class ventasCRUD (viewsets.ModelViewSet):
    queryset = Ventas.objects.all()
    serializer_class = VentasSerializers