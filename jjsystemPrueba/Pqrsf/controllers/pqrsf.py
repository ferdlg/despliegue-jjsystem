from rest_framework import viewsets
from Account.models import *
from .serializers import PqrsfSerializer

class pqrsfCRUD(viewsets.ModelViewSet):
    queryset = Pqrsf.objects.all()
    serializer_class = PqrsfSerializer

    def crear_pqrsf(self, request):
        return