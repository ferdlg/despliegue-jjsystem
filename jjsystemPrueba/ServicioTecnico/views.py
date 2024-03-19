from django.shortcuts import render
from rest_framework import viewsets
from Account.models import Citas
from .controllers.serializers import CitasSerializer
from .controllers.citas import citasCRUD

def index (request):
    return render(request, 'index.html')

def indexTecnicos(request):
    return render(request, 'tecnicos.html')
