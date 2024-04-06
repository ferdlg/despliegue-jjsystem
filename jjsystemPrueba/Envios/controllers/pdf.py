from django.conf import settings
from django.shortcuts import get_object_or_404
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageTemplate, Frame, Image, Table, TableStyle, HRFlowable
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from io import BytesIO
import os
from Account.models import DetalleEnviosVentas, Envios, Tecnicos

def generar_pdf(request, templateName):
    # Obtener los datos de los envíos
    envios = Envios.objects.all()

    # Crear un buffer de bytes para el PDF
    buffer = BytesIO()

    # Configurar el tamaño del documento
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    # Crear una tabla para los envíos
    tabla_datos = []
    tabla_datos.append(["ID", "Dirección", "ID Técnico", "Estado"])
    for envio in envios:
        tabla_datos.append([envio.idenvio, envio.direccionenvio, envio.idtecnico.idtecnico, envio.idestadoenvio.nombreestadoenvio])

    tabla = Table(tabla_datos)

    # Aplicar estilos a la tabla
    estilo_tabla = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#263465")),  # Cambiar el color del encabezado
                               ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                               ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                               ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                               ('GRID', (0, 0), (-1, -1), 1, colors.black)])

    tabla.setStyle(estilo_tabla)

    # Agregar el logotipo
    logo_path = os.path.join(settings.STATICFILES_DIRS[3], 'images/logo.png')
    logo_img = Image(logo_path, width=110, height=30)

    # Agregar espacio entre elementos
    elementos = []
    elementos.append(logo_img)
    elementos.append(Spacer(1, 12))
    elementos.append(Spacer(1, 12))
    elementos.append(tabla)

    # Construir el documento
    doc.build(elementos)

    # Obtener el PDF generado
    pdf = buffer.getvalue()
    buffer.close()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="envios.pdf"'
    response.write(pdf)
    return response

def generar_pdf_envio(request, idenvio):
    # Obtener el envío específico
    envio = Envios.objects.get(idenvio=idenvio)

    # Obtener los detalles de envío específicos para este envío
    detalles_envio = DetalleEnviosVentas.objects.filter(idenvio=idenvio)

    # Crear el PDF
    pdf_filename = f"comprobante_envio_{idenvio}.pdf"
    pdf = SimpleDocTemplate(pdf_filename, pagesize=letter, topMargin=50, bottomMargin=50)  

    # Crear elementos del PDF
    elementos = []

    # Agregar logo
    logo_path = os.path.join(settings.STATICFILES_DIRS[3], 'images', 'logo.png')
    logo = Image(logo_path, width=150, height=30)
    elementos.append(logo)

    # Agregar título
    titulo = "<b>Comprobante de Envío</b><br/><br/>"
    paragraph_titulo = Paragraph(titulo, getSampleStyleSheet()['Title'])
    elementos.append(paragraph_titulo)

    elementos.append(HRFlowable(width="100%", color=colors.black, thickness=1, spaceBefore=0, spaceAfter=20))

    # Agregar detalles del envío
    detalles_texto = f"<b>ID de Envío:</b> {envio.idenvio}<br/><b>Dirección de Envío:</b> {envio.direccionenvio}<br/><b>ID Técnico:</b> {envio.idtecnico_id}<br/><b>ID Estado de Envío:</b> {envio.idestadoenvio.nombreestadoenvio}<br/><br/>"
    paragraph_detalles = Paragraph(detalles_texto, getSampleStyleSheet()['Normal'])
    elementos.append(paragraph_detalles)

    # Agregar espacio antes de la tabla de detalles de venta
    elementos.append(Spacer(1, 20))  

    # Crear tabla para los detalles de venta (Parte 1)
    datos_tabla_detalles1 = [['ID Venta', 'Detalles de Venta']]
    for detalle in detalles_envio:
        datos_tabla_detalles1.append([detalle.idventa, Paragraph(detalle.detallesventa, getSampleStyleSheet()['Normal'])])

    tabla_detalles1 = Table(datos_tabla_detalles1, colWidths=[100, 200])
    tabla_detalles1.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#263465")),
                                         ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                         ('WORDWRAP', (1, 1), (-1, -1))]))  
    elementos.append(tabla_detalles1)

    # Agregar espacio entre las tablas
    elementos.append(Spacer(1, 20))  

    # Crear tabla para los detalles de venta (Parte 2)
    datos_tabla_detalles2 = [['Técnico Asignado', 'Número de Documento', 'Fecha de Venta']]
    for detalle in detalles_envio:
        datos_tabla_detalles2.append([detalle.nombretecnico, detalle.numerodocumento, detalle.fechaventa])

    tabla_detalles2 = Table(datos_tabla_detalles2, colWidths=[100, 150, 100])
    tabla_detalles2.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#263465")),
                                         ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke)]))
    elementos.append(tabla_detalles2)

    # Definir función para el pie de página
    def pie_pagina(canvas, doc):
        pie_de_pagina = "© 2024 JJSystem Project. Todos los derechos reservados."
        canvas.saveState()
        canvas.setFont("Helvetica", 9)
        canvas.drawString(inch, 0.75 * inch, pie_de_pagina)
        canvas.restoreState()

    # Construir el PDF con la función de pie de página
    pdf.build(elementos, onFirstPage=pie_pagina, onLaterPages=pie_pagina)

    # Devolver el PDF como respuesta
    with open(pdf_filename, 'rb') as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{pdf_filename}"'
        return response
