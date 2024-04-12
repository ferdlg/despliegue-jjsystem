from django.shortcuts import redirect, render
from rest_framework import viewsets
from Account.models import *
from .serializers import VentasSerializer
from django.core.paginator import Paginator , EmptyPage , PageNotAnInteger
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from Account.views import role_required
from django.contrib.auth.decorators import login_required

class ventasCRUD(viewsets.ModelViewSet):
    queryset = Ventas.objects.all()
    serializer_class = VentasSerializer

    #cliente Historial de compras 
    def historial_compras(self,request):
        numerodocumento = request.user.numerodocumento        
        compras_queryset = Ventas.objects.filter(idcotizacion__idcliente__numerodocumento=numerodocumento)
        paginator = Paginator(compras_queryset, 10)
        page_number = request.GET.get('page')

        try:
            compras = paginator.page(page_number)
        except PageNotAnInteger:
            compras = paginator.page(1)
        except EmptyPage:
            compras = paginator.page(paginator.num_pages)

        if compras:
            return render(request, 'cliente/compras.html', {"compras": compras})
        else:
            messages.warning(request, 'Aun no tienes compras para mostrar')
            return render(request, 'cliente/compras.html')
# Ventas en dashboard admin
@login_required
@role_required(1)
def home_ventas(request):
    idventa = request.GET.get('idventa')
    
    if idventa:
        # Filtrar las ventas por ID de venta 
        ventas_list = Ventas.objects.filter(idventa=idventa)
    else:

        ventas_list = Ventas.objects.all()

    paginator = Paginator(ventas_list, 5)
    page_number = request.GET.get('page')
    try:
        ventas = paginator.page(page_number)
    except PageNotAnInteger:
        ventas = paginator.page(1)
    except EmptyPage:
        ventas = paginator.page(paginator.num_pages)
    
    return render(request, "crudAdmin/IndexVentas.html", {"ventas":ventas})

@login_required
@role_required(1)
def createVenta(request):
    if request.method == 'POST':
        try:
            fechaventa = request.POST.get('fecha')
            idenvio_id = request.POST.get('envio')
            idcotizacion_id = request.POST.get('cotizacion')

            idenvio = Envios.objects.get(pk=idenvio_id)
            idcotizacion = Cotizaciones.objects.get(pk=idcotizacion_id)

            # Crear la instancia de venta
            venta = Ventas.objects.create(
                fechaventa=fechaventa,
                idenvio=idenvio,
                idcotizacion=idcotizacion
            )

            # Obtener los detalles de venta del formulario
            detalles = request.POST.getlist('detalle')
            subtotales = request.POST.getlist('subtotal')
            totales = request.POST.getlist('total')

            # Crear instancias de Detallesventas y asignarlas a la venta
            for detalle, subtotal, total in zip(detalles, subtotales, totales):
                Detallesventas.objects.create(
                    detallesventa=detalle,
                    subtotalventa=subtotal,
                    totalventa=total,
                    idventa=venta
                )
            messages.success(request, 'Venta registrada exitosamente')
            return redirect('homeVentas')
        except ObjectDoesNotExist:
            messages.error(request, 'No se encontró el envío o la cotización.')
            return redirect('createVenta')  # Redirigir de vuelta al formulario de creación de venta
    else:
        envios = Envios.objects.all()
        cotizaciones = Cotizaciones.objects.all()
        return render(request, "crudAdmin/createVenta.html", {"envios": envios, "cotizaciones": cotizaciones})
@login_required
@role_required(1)
def editVenta(request, idVenta):
    try:
        venta = Ventas.objects.get(idventa=idVenta)
    except Ventas.DoesNotExist:
        messages.error(request, 'La venta especificada no existe.')
        return redirect('homeVentas')

    if request.method == 'POST':
        try:
            # Obtener los datos del formulario
            idenvio_id = request.POST.get('envio')
            idcotizacion_id = request.POST.get('cotizacion')
            detalle = request.POST.get('detalle')
            subtotal = request.POST.get('subtotal')
            total = request.POST.get('total')

            idenvio = Envios.objects.get(pk=idenvio_id)
            idcotizacion = Cotizaciones.objects.get(pk=idcotizacion_id)

            # Actualizar los campos de la venta
            venta.idenvio = idenvio
            venta.idcotizacion = idcotizacion
            venta.save()

            # Actualizar los detalles de venta
            detalle_venta = venta.detallesventas_set.first() 
            detalle_venta.detallesventa = detalle
            detalle_venta.subtotalventa = subtotal
            detalle_venta.totalventa = total
            detalle_venta.save()
            
            messages.success(request, 'Venta actualizada exitosamente')
            return redirect('homeVentas')
        except ObjectDoesNotExist:
            messages.error(request, 'No se encontró el envío o la cotización.')
            return redirect('editVenta', idVenta=idVenta)  # Redirigir de vuelta a la página de edición de venta
    else:
        envios = Envios.objects.all()
        cotizaciones = Cotizaciones.objects.all()
        return render(request, "crudAdmin/EditVenta.html", {"venta": venta, "envios": envios, "cotizaciones": cotizaciones})
@login_required
@role_required(1)    
def deleteVenta(request, idVenta):
    venta = Ventas.objects.get(idventa=idVenta)
    if request.method == 'POST':
        venta.detallesventas_set.all().delete()
        messages.success('Detalle de venta eliminado')
        venta.delete()
        messages.success('Venta eliminada correctamente')
    else:
        messages.error('Ocurrio un error al intentar eliminar la venta')
    return redirect('homeVentas') 

