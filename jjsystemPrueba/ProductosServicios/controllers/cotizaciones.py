from django.shortcuts import get_object_or_404, redirect, render
from ServicioTecnico.controllers.cotizaciones import CotizacionesCRUD as BaseCotizacionesCRUD
from Account.models import *
from django.db import connection
from django.contrib import messages


class CotizacionesCRUD(BaseCotizacionesCRUD):
    # Métodos heredados de la clase base
    def ir_a_cotizaciones(self, request):
        numerodocumento = request.user.numerodocumento
        cotizaciones = Cotizaciones.objects.filter(idcliente__numerodocumento=numerodocumento)
        return render(request, 'cliente/crear_cotizacion.html', {'cotizaciones':cotizaciones})
    
    def crear_cotizacion(self,request):
        if request.method == 'POST':
            # Obtener los datos del formulario de creación de cotización
            numerodocumento = request.user.numerodocumento
            cliente = get_object_or_404(Clientes, numerodocumento=numerodocumento)
            idcliente = cliente.idcliente
            descripcion_cotizacion = request.POST.get('descripcioncotizacion', '')
            estado = Estadoscotizaciones.objects.get(idestadocotizacion =1)
            # Crear la nueva cotización
            nueva_cotizacion = Cotizaciones.objects.create(
                idcliente=cliente,
                totalcotizacion=0.0,  
                descripcioncotizacion=descripcion_cotizacion,
                idestadocotizacion = estado
            )

            # Redirigir a la vista para agregar productos a la cotización recién creada
            return redirect('asignar_productos_servicios_cliente', id_cotizacion=nueva_cotizacion.idcotizacion)
        # Renderizar el formulario de creación de cotización
        messages.error(request,'Error al crear la cotizacion')
        return render(request, 'cliente/crear_cotizacion.html')
    
    def asignar_productos_servicios_cliente(self,request, id_cotizacion):
        if request.method == 'POST':
            productos_seleccionados = request.POST.getlist('producto[]')
            servicios_seleccionados = request.POST.getlist('servicio[]')

            cotizacion = Cotizaciones.objects.get(idcotizacion=id_cotizacion)
            print(productos_seleccionados)
            for idproducto in productos_seleccionados:
                cantidades = request.POST.getlist('cantidad_' + idproducto)
                for cantidad in cantidades:
                    if cantidad.strip():  # Verificar si la cantidad no está vacía
                        try:
                            cantidad = int(cantidad)
                            if cantidad > 0:
                                producto = Productos.objects.get(idproducto=idproducto)
                                producto_cotizacion = CotizacionesProductos.objects.create(
                                    idcotizacion=cotizacion,
                                    idproducto=producto,
                                    cantidad=cantidad
                                )
                                messages.success(request, 'Se ha agregado el producto a la cotización')
                            else:
                                messages.error(request, 'La cantidad debe ser un número entero positivo')
                        except ValueError:
                            messages.error(request, 'La cantidad debe ser un número entero')
                    else:
                        messages.error(request, 'No se ha ingresado la cantidad')

            for idservicio in servicios_seleccionados:
                servicio = Servicios.objects.get(idservicio=idservicio)
                servicio_cotizacion = CotizacionesServicios.objects.create(
                    idcotizacion=cotizacion,
                    idservicio=servicio
                )

            productos = Productos.objects.all()
            servicios = Servicios.objects.all()

            messages.success(request, 'Se ha creado tu cotizacion correctamente')
            return redirect('ver_cotizacion_cliente', id_cotizacion=id_cotizacion )
            
        else:
            productos = Productos.objects.all()
            servicios = Servicios.objects.all()
            messages.error(request, 'No se han agregado productos o servicios a la cotización')
            return render(request, 'cliente/agregar_productos_servicios.html', {'productos': productos, 'servicios': servicios, 'idcotizacion': id_cotizacion})

def obtener_detalles_cotizacion(id_cotizacion):
    with connection.cursor() as cursor:
        cursor.callproc('ObtenerDetallesCotizacion', [id_cotizacion])
        resultados = cursor.fetchall()
    return resultados

def vista_detalle_cotizacion(request, id_cotizacion):
    detalles_cotizacion = obtener_detalles_cotizacion(id_cotizacion)
    return render(request, 'cliente/ver_cotizacion.html', {'detalles_cotizacion': detalles_cotizacion})