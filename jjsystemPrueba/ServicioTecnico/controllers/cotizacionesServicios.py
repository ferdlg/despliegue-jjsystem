from django.shortcuts import render, redirect
from rest_framework import viewsets
from Account.models import CotizacionesServicios
from .serializers import CotizacionesServiciosSerializers
from django.core.paginator import Paginator , EmptyPage , PageNotAnInteger

class CotizacionesServiciosCRUD():
    queryset = CotizacionesServicios.objects.all()
    serializer_class = CotizacionesServiciosSerializers
