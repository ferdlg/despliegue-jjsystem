from rest_framework import viewsets
from Account.models import *
from .serializers import PqrsfSerializer
from django.shortcuts import redirect, render
from django.contrib import messages


class pqrsfCRUD(viewsets.ModelViewSet):
    queryset = Pqrsf.objects.all()
    serializer_class = PqrsfSerializer

    def ir_a_pqrsf(self, request):
        numerodocumento = request.user.numerodocumento
        cliente = Clientes.objects.get(numerodocumento = numerodocumento)
        estados = Estadospqrsf.objects.all()
        tipos = Tipospqrsf.objects.all()

        pqrsfs = Pqrsf.objects.filter(idcliente = cliente.idcliente)

        return render(request, 'cliente/ver_pqrsf.html', {'estados':estados,'tipos':tipos, 'pqrsfs':pqrsfs})
    
    def crear_pqrsf( self, request):
        if request.method == 'POST':
            numerodocumento = request.user.numerodocumento
            cliente = Clientes.objects.get(numerodocumento = numerodocumento)
            fechapqrsf = request.POST.get('fechapqrsf')
            informacionpqrsf = request.POST.get('informacionpqrsf')
            tipo = request.POST.get('idtipopqrsf')

            # Obtener la instancia de EstadosPqrsf
            estadopqrsf = Estadospqrsf.objects.get(nombreestadopqrsf = 'Solicitada')
            # Obtener la instancia de TiposPqrsf
            tipopqrsf = Tipospqrsf.objects.get(idtipopqrsf=tipo)

            # Crear la instancia de Pqrsf
            pqrsf = Pqrsf.objects.create(
                idcliente = cliente,
                fechapqrsf=fechapqrsf,
                informacionpqrsf=informacionpqrsf,
                idestadopqrsf=estadopqrsf,
                idtipopqrsf=tipopqrsf
            )
            messages.success(request,'Cotización registrada correctamente')
        return redirect('ir_a_pqrsf')  