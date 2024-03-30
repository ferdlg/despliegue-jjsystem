from urllib import response
from rest_framework import viewsets
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from Account.models import Cotizaciones, Clientes, Estadoscotizaciones, Productos, Servicios, CotizacionesProductos, CotizacionesServicios
from .serializers import CotizacionesSerializer
from django.contrib import messages
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from io import BytesIO
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.lib.styles import getSampleStyleSheet
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

class CotizacionesCRUD(viewsets.ModelViewSet):
    queryset = Cotizaciones.objects.all()
    serializer_class = CotizacionesSerializer

    def listar_cotizaciones(self, request):
        id_cotizacion = request.GET.get('id_cotizacion')  # Obtener el ID de la cotización desde la URL
        
        # Filtrar por ID de cotización si está presente en la solicitud
        if id_cotizacion:
            cotizaciones_list = self.queryset.filter(idcotizacion=id_cotizacion)
        else:
            cotizaciones_list = self.queryset.all()
        
        paginator = Paginator(cotizaciones_list, 5)
        page_number = request.GET.get('page', 1)
        try:
            cotizaciones = paginator.page(page_number)
        except PageNotAnInteger:
            cotizaciones = paginator.page(1)
        except EmptyPage:
            cotizaciones = paginator.page(paginator.num_pages)
        
        estados = Estadoscotizaciones.objects.all()
        clientes = Clientes.objects.all()
        return render(request, 'cotizaciones.html', {'cotizaciones': cotizaciones, 'estados':estados, 'clientes':clientes})

    def crear_cotizaciones(self, request):
        if request.method == 'POST':
            totalcotizacion = request.POST.get('totalCotizacion')
            descripcioncotizacion = request.POST.get('descripcionCotizacion')
            idcliente = request.POST.get('cliente')
            idestadocotizacion = request.POST.get('estado')

            cliente = Clientes.objects.get(idcliente=idcliente)
            estado = Estadoscotizaciones.objects.get(idestadocotizacion=idestadocotizacion)

            cotizacion = Cotizaciones.objects.create(
                totalcotizacion=totalcotizacion,
                descripcioncotizacion=descripcioncotizacion,
                idcliente=cliente,
                idestadocotizacion=estado
            )
            return redirect( 'asignar_productos_servicios', idcotizacion = cotizacion.idcotizacion)
        productos = Productos.objects.all()
        servicios = Servicios.objects.all()

        return render(request, 'cotizaciones.html', {'productos':productos, 'servicios':servicios})

    def asignar_productos_servicios(self, request, idcotizacion):
        try:
            cotizacion = Cotizaciones.objects.get(idcotizacion=idcotizacion)
        except ObjectDoesNotExist:
            messages.error(request, 'No se encontró la cotización asociada.')
            return redirect('ver_cotizaciones')

        if request.method == 'POST':
            productos_seleccionados = request.POST.getlist('producto[]')
            servicios_seleccionados = request.POST.getlist('servicio[]')

            for idproducto in productos_seleccionados:
                cantidad = request.POST.get('cantidad_' + idproducto)
                if cantidad: 
                    try:
                        producto = Productos.objects.get(idproducto=idproducto)
                        producto_cotizacion = CotizacionesProductos.objects.create(
                            idcotizacion=cotizacion,
                            idproducto=producto,
                            cantidad=cantidad
                        )
                    except ObjectDoesNotExist:
                        messages.warning(request, f'No se encontró el producto asociado con el ID {idproducto}.')
                else:
                    messages.warning(request, f'No se ha ingresado una cantidad para el producto con ID {idproducto}.')

            for idservicio in servicios_seleccionados:
                try:
                    servicio = Servicios.objects.get(idservicio=idservicio)
                    servicio_cotizacion = CotizacionesServicios.objects.create(
                        idcotizacion=cotizacion,
                        idservicio=servicio
                    )
                except ObjectDoesNotExist:
                    messages.warning(request, f'No se encontró el servicio asociado con el ID {idservicio}.')

            messages.success(request, 'Cotización creada exitosamente')
            return redirect('ver_cotizaciones')

        else:
            productos = Productos.objects.all()
            servicios = Servicios.objects.all()
            return render(request, 'asignarProductosServicios.html', {'productos': productos, 'servicios': servicios, 'idcotizacion': idcotizacion})
        
    
    
    def editar_cotizacion(request, idcotizacion):
        try:
            cotizacion = Cotizaciones.objects.get(idcotizacion=idcotizacion)

            if request.method == 'POST':
                totalcotizacion = request.POST.get('totalCotizacion')
                descripcioncotizacion = request.POST.get('descripcionCotizacion')
                idcliente = request.POST.get('cliente')
                idestadocotizacion = request.POST.get('estado')

                cliente = Clientes.objects.get(idcliente=idcliente)
                estado = Estadoscotizaciones.objects.get(idestadocotizacion=idestadocotizacion)

                cotizacion.totalcotizacion = totalcotizacion
                cotizacion.descripcioncotizacion = descripcioncotizacion
                cotizacion.idcliente = cliente
                cotizacion.idestadocotizacion = estado
                cotizacion.save()

                messages.success(request, 'Cotización editada correctamente')
                return redirect('ver_cotizaciones')

            clientes = Clientes.objects.all()
            estados = Estadoscotizaciones.objects.all()

            return render(request, 'EditarCotizacion.html', {'cotizacion': cotizacion, 'clientes': clientes, 'estados': estados})
        except ObjectDoesNotExist:
            messages.error(request, 'La cotización especificada no existe.')
        except Exception as e:
                messages.error(request, f'Ocurrió un error al intentar editar la cita: {str(e)}')
        return redirect('ver_cotizaciones')
        
    def eliminar_cotizacion(self, request, idcotizacion):
        try:
            cotizacion = Cotizaciones.objects.get(idcotizacion=idcotizacion)
        except ObjectDoesNotExist:
            messages.error(request, 'No se pudo encontrar la cotización.')
            return redirect('ver_cotizaciones')

        if request.method == 'POST':
            try:
                CotizacionesProductos.objects.filter(idcotizacion=cotizacion).delete()
                CotizacionesServicios.objects.filter(idcotizacion=cotizacion).delete()
                cotizacion.delete()
                messages.success(request, 'Cotización eliminada correctamente')
            except Exception as e:
                messages.error(request, f'Ocurrió un error al eliminar la cotización: {str(e)}')
        else:
            return render(request, 'ConfirmarEliminarCotizacion.html', {'cotizacion': cotizacion})

        return redirect('ver_cotizaciones')

def generar_pdf(request, idcotizacion):
    # Obtener la cotización específica
    cotizacion = get_object_or_404(Cotizaciones, idcotizacion=idcotizacion)

    # Crear un buffer de bytes para el PDF
    buffer = BytesIO()

    # Configurar el tamaño del documento
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    # Estilo del párrafo
    styles = getSampleStyleSheet()
    descripcion_style = styles["Normal"]

    # Crear una tabla para la cotización
    tabla_datos = [
        ["ID", "Fecha", "Descripción", "Total", "Cliente", "Num. Documento", "Estado"],
        [cotizacion.idcotizacion, cotizacion.fechacotizacion,
         Paragraph(cotizacion.descripcioncotizacion, descripcion_style),
         cotizacion.totalcotizacion, cotizacion.idcliente.numerodocumento.nombre + " " +
         cotizacion.idcliente.numerodocumento.apellido, cotizacion.idcliente.numerodocumento.numerodocumento,
         cotizacion.idestadocotizacion.nombreestadocotizacion]
    ]

    col_widths = [70, 80, 100, 70, 120, 100, 80]

    tabla = Table(tabla_datos, colWidths=col_widths)

    # Aplicar estilos a la tabla
    estilo_tabla = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Centrar verticalmente el texto en todas las celdas
    ])

    tabla.setStyle(estilo_tabla)

    # Agregar la tabla al documento
    elementos = [tabla]
    doc.build(elementos)

    # Obtener el PDF generado
    pdf = buffer.getvalue()
    buffer.close()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="cotizacion_{idcotizacion}.pdf"'
    response.write(pdf)
    return response

