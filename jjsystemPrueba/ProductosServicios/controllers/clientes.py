from django.shortcuts import redirect, render
from rest_framework import viewsets
from Account.models import Clientes
from Account.utilities import actualizar_datos_usuario, validar_password , cambiar_password
from .serializers import ClientesSerializers
from django.contrib.auth.hashers import make_password, check_password


class clientesCRUD(viewsets.ModelViewSet):
    queryset = Clientes.objects.all()
    serializer_class = ClientesSerializers
    #Actualizad datos --> rol cliente
    def actualizar_mis_datos(self, request):
        user = request.user
        if user.idrol.idrol == 2:
            return actualizar_datos_usuario(request, 'cliente/ver_perfil')
        else:
            mensaje = 'Ocurrio un error al intentar actualizar tus datos'
            return render(request, 'mensaje.html',{'mensaje':mensaje})
    def validar_contrasena(self,request):
        return validar_password(request)

    def cambiar_contrasena(self,request):
        return cambiar_password(request)
