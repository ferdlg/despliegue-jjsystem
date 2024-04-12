from django.utils import timezone
from rest_framework import viewsets
from Account.models import *
from .serializers import PqrsfSerializer
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from ..correos import correo_confirmacion_pqrsf_cliente_admin
from Account.views import role_required
from django.contrib.auth.decorators import login_required

class pqrsfCRUD(viewsets.ModelViewSet):
    queryset = Pqrsf.objects.all()
    serializer_class = PqrsfSerializer

    def ir_a_pqrsf(self, request):
        numerodocumento = request.user.numerodocumento
        cliente = Clientes.objects.get(numerodocumento = numerodocumento)
        estados = Estadospqrsf.objects.all()
        tipos = Tipospqrsf.objects.all()

        pqrsfs = Pqrsf.objects.filter(idcliente = cliente.idcliente)

        return render(request, 'cliente/ver_pqrsf.html', {'estados':estados,'tipos':tipos, 'pqrsfs':pqrsfs, 'cliente':cliente})
    
    def crear_pqrsf(self, request):
        if request.method == 'POST':
            numerodocumento = request.user.numerodocumento
            cliente = get_object_or_404(Clientes, numerodocumento=numerodocumento)
            idcliente = cliente.idcliente if cliente else None
            fechapqrsf = timezone.now().date()
            informacionpqrsf = request.POST.get('informacionpqrsf')
            tipo = request.POST.get('idtipopqrsf')

            # Obtener los objetos de estado y tipo de PQRSF
            estadopqrsf = Estadospqrsf.objects.get(nombreestadopqrsf='Solicitada')
            tipopqrsf = Tipospqrsf.objects.get(idtipopqrsf=tipo)

            # Crear la instancia de PQRSF
            pqrsf = Pqrsf.objects.create(
                idcliente=cliente,
                fechapqrsf=fechapqrsf,
                informacionpqrsf=informacionpqrsf,
                idestadopqrsf=estadopqrsf,
                idtipopqrsf=tipopqrsf
            )
            messages.success(request, 'PQRSF registrada correctamente')
            correo_confirmacion_pqrsf_cliente_admin(request, idpqrsf=pqrsf.idpqrsf)
            return redirect('ir_a_pqrsf')
        return redirect('ir_a_pqrsf')
        
