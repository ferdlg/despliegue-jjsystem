import os
from django.conf import settings
from Account.models import Cotizaciones
from reportlab.lib.pagesizes import letter, inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib import colors
from io import BytesIO
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle
from Account.views import role_required
from django.contrib.auth.decorators import login_required
from ProductosServicios.controllers.utils import obtener_detalles_cotizacion

@login_required
@role_required(1)
def generar_pdf(request, idcotizacion):
    # Obtener la cotización y los detalles de la cotización
    cotizacion = get_object_or_404(Cotizaciones, idcotizacion=idcotizacion)
    detalles_cotizacion = obtener_detalles_cotizacion(idcotizacion)

    # Crear listas para almacenar productos y servicios
    productos = []
    servicios = []
    total_productos = 0.0
    total_servicios = 0.0

    for resultado in detalles_cotizacion:
        id_producto = resultado[4]
        nombre_producto = resultado[5]
        descripcion_producto = resultado[6]
        precio_producto = resultado[7]
        cantidad_producto = resultado[8]
        
        id_servicio = resultado[9]
        nombre_servicio = resultado[10]
        descripcion_servicio = resultado[11]
        precio_servicio = resultado[12]
        
        # Agregar productos si existe un ID de producto
        if id_producto:
            total_producto = precio_producto * cantidad_producto
            producto = {
                'nombre': nombre_producto,
                'descripcion': descripcion_producto,
                'precio': precio_producto,
                'cantidad': cantidad_producto,
                'total': total_producto
            }
            productos.append(producto)
            total_productos += total_producto
        
        # Agregar servicios si existe un ID de servicio
        if id_servicio:
            servicio = {
                'nombre': nombre_servicio,
                'descripcion': descripcion_servicio,
                'precio': precio_servicio
            }
            servicios.append(servicio)
            total_servicios += precio_servicio
    # Calcular el total de la cotización
    total_cotizacion = total_productos + total_servicios

    # Crear el PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    espacio_entre_tablas = 0.2 * inch 
    elementos = []

    # Crear el título y el logo
    titulo = 'FORMATO DE COTIZACIONES JJSYSTEM PROJECT'
    estilo_titulo = ParagraphStyle(
        name='Titulo',
        fontSize=16,
        leading=20,
        fontName='Helvetica-Bold'
    )
    logo_path = os.path.join(settings.STATICFILES_DIRS[3], 'images', 'logo.png')
    titulo_paragraph = Paragraph(titulo, estilo_titulo)
    logo_img = Image(logo_path, width=110, height=30)

    # Detalles de la cotización
    detalles_cotizacion_encabezado = [
        ['Numero de cotización:'],
        [cotizacion.idcotizacion],
        ['Fecha:', cotizacion.fechacotizacion],
        ['Cliente:', f'{cotizacion.idcliente.numerodocumento.nombre} {cotizacion.idcliente.numerodocumento.apellido}']
    ]

    # Crear tabla de encabezado
    tabla_encabezado = Table(detalles_cotizacion_encabezado, colWidths=[100, 390])

    # Estilo para la tabla
    tabla_estilo = TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ])

    # Aplicar estilo a la tabla de encabezado
    tabla_encabezado.setStyle(tabla_estilo)

    # Crear tabla de productos
    tabla_productos = Table([[Paragraph('Productos', styles['Heading2'])]] + [('Producto','Cantidad', 'Precio Unitario', 'Total')] + [[producto['nombre'], producto['cantidad'], producto['precio'], producto['total']] for producto in productos])

    # Crear tabla de servicios
    tabla_servicios = Table([[Paragraph('Servicios', styles['Heading2'])]] + [[servicio['nombre'], servicio['precio']] for servicio in servicios])
    tabla_total_cotizacion = Table([['Total Cotización:', total_cotizacion]])


    tabla_logo_titulo = Table([[logo_img, titulo_paragraph]], colWidths=[110, 390], rowHeights=[30])
    tabla_logo_titulo.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.white),  
        ('BOX', (0, 1), (-1, -1), 1, colors.black)
    ]))

    # Agregar elementos al documento
    elementos.append(tabla_logo_titulo)
    elementos.append(Spacer(3, espacio_entre_tablas))  
    elementos.append(tabla_encabezado)
    elementos.append(Spacer(3, espacio_entre_tablas))  
    elementos.append(tabla_productos)
    elementos.append(Spacer(3, espacio_entre_tablas))
    elementos.append(tabla_servicios)
    elementos.append(Spacer(3, espacio_entre_tablas))
    elementos.append(tabla_total_cotizacion)
    # Construir el documento
    doc.build(elementos)

    # Obtener el PDF generado
    pdf = buffer.getvalue()
    buffer.close()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="cotizacion_{idcotizacion}.pdf"'
    response.write(pdf)
    return response
