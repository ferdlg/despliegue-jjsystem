from django.shortcuts import render, redirect
from rest_framework import viewsets
from Account.models import CotizacionesProductos
from .serializers import CotizacionesProductosSerializers
from django.core.paginator import Paginator , EmptyPage , PageNotAnInteger


class CotizacionesServiciosCRUD():
    queryset = CotizacionesProductos.objects.all()
    serializer_class = CotizacionesProductosSerializers

