from rest_framework import viewsets
from Account.models import Actividadescronogramatecnicos
from .serializers import ActividadescronogramatecnicosSerializer


class actividadesCrogTecCRUD(viewsets.ModelViewSet):
    queryset = Actividadescronogramatecnicos.objects.all()
    serializer_class = ActividadescronogramatecnicosSerializer