from django.shortcuts import redirect, render
from rest_framework import viewsets
from Account.models import Clientes
from .serializers import ClientesSerializers
from django.contrib.auth.hashers import make_password, check_password


class clientesCRUD(viewsets.ModelViewSet):
    queryset = Clientes.objects.all()
    serializer_class = ClientesSerializers
    #Actualizad datos --> rol cliente
    def actualizar_mis_datos(self, request):
        numerodocumento = request.user.numerodocumento
        cliente = Clientes.objects.get(numerodocumento = numerodocumento)
        usuario = request.user

        if request.method == 'POST':
            nombre = request.POST.get('nombre')
            apellido = request.POST.get('apellido')
            email = request.POST.get('email')
            numerodocumento = request.POST.get('numerodocumento')
            numerocontacto = request.POST.get('numerocontacto')

            usuario.nombre = nombre
            usuario.apellido = apellido
            usuario.email = email
            usuario.numerodocumento = numerodocumento
            usuario.numerocontacto = numerocontacto
            usuario.save()

            return redirect('ver_perfil')
        return render(request, 'cliente/ver_perfil.html', {'usuario':usuario, 'cliente':cliente})
    
    def validar_password(self, request):
        usuario = request.user
        password = make_password(request.POST.get('password'))
        if check_password(password, usuario.password):
            password_correct = True
        else:
            password_correct = False
        return render(request, 'cliente/cambiar_password.html', {'password_correct': password_correct})
    
    def cambiar_password(self, request):
        usuario = request.user
        new_password = request.POST.get('new_password')

        usuario.password = make_password(new_password)
        usuario.save()

        return redirect('actualizar_mis_datos')