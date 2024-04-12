from rest_framework import viewsets
from Account.models import Detallesventas
from .serializers import DetalleVentasSerializer


class detalleVentaCRUD(viewsets.ModelViewSet):
    queryset = Detallesventas.objects.all()
    serializer_class = DetalleVentasSerializer