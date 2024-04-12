from rest_framework import viewsets
from Account.models import Estadoscotizaciones
from .serializers import EstadoscotizacionesSerializer


class estadocotizacionesCRUD(viewsets.ModelViewSet):
    queryset = Estadoscotizaciones.objects.all()
    serializer_class = EstadoscotizacionesSerializer