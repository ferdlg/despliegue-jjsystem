from rest_framework import viewsets
from Account.models import RolesHasPermisos
from .serializers import Rol_has_permisosSerializers


class rol_has_permisosCRUD(viewsets.ModelViewSet):
    queryset = RolesHasPermisos.objects.all()
    serializer_class = Rol_has_permisosSerializers