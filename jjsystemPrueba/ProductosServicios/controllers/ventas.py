from django.shortcuts import redirect, render
from rest_framework import viewsets
from Account.models import *
from .serializers import VentasSerializer
from django.core.paginator import Paginator , EmptyPage , PageNotAnInteger
from django.http import HttpResponseRedirect


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
            mensaje = 'Aún no tienes compras.'
            return render(request, 'mensaje.html', {'mensaje': mensaje})

# Ventas en dashboard admin
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


def createVenta(request):
    if request.method == 'POST':
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

        return redirect('homeVentas')

    envios = Envios.objects.all()
    cotizaciones = Cotizaciones.objects.all()
    return render(request, "crudAdmin/createVenta.html", {"envios": envios, "cotizaciones": cotizaciones})


def editVenta(request, idVenta):
    venta = Ventas.objects.get(idventa=idVenta)
    if request.method == 'POST':
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

        return redirect('homeVentas')

    envios = Envios.objects.all()
    cotizaciones = Cotizaciones.objects.all()
    return render(request, "crudAdmin/EditVenta.html", {"venta": venta, "envios": envios, "cotizaciones": cotizaciones})

def deleteVenta(request, idVenta):
    venta = Ventas.objects.get(idventa=idVenta)
    if request.method == 'POST':
        # Eliminar los detalles de venta asociados
        venta.detallesventas_set.all().delete()
        # Eliminar la venta
        venta.delete()
        return HttpResponseRedirect('/productos_servicios/ventas')  # Redirigir al home de ventas después de eliminar la venta
    else:
        # Si la solicitud no es POST, redirigir al home de ventas
        return HttpResponseRedirect('/productos_servicios/ventas')

