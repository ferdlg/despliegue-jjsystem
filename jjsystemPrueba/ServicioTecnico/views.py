from django.shortcuts import render, redirect
from rest_framework import viewsets
from Account.models import Citas , Tecnicos, Administrador
from Account.utilities import actualizar_datos_usuario, validar_password, cambiar_password
from .controllers.serializers import CitasSerializer
from .controllers.citas import citasCRUD

def index (request):
    return render(request, 'index.html')

def indexTecnicos(request):
    return render(request, 'tecnicos.html')

def inicio(request):
    return render(request, 'inicio.html')

#actualizar datos para admin y tecnico
def mi_perfil(request):
    user = request.user
    if user.idrol.idrol == 1 or user.idrol.idrol == 3:
        return actualizar_datos_usuario(request, 'mi_perfil')
    else:
        return redirect('mensaje')
    
def validar_contrasena(request):
    return validar_password(request)

def cambiar_contrasena(request):
    return cambiar_password(request)
