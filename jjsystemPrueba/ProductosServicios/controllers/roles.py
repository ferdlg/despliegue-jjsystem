from rest_framework import viewsets
from Account.models import Roles
from .serializers import RolesSerializers


class rolesCRUD(viewsets.ModelViewSet):
    queryset = Roles.objects.all()
    serializer_class = RolesSerializers