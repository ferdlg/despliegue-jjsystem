from rest_framework import viewsets
from Account.models import Cronogramatecnicos
from .serializers import CronogramatecnicosSerializer


class cronogramatecnicosCRUD(viewsets.ModelViewSet):
    queryset = Cronogramatecnicos.objects.all()
    serializer_class = CronogramatecnicosSerializer

    #ver cronograma por tecnico
    #asignarle actividades al cronograma 