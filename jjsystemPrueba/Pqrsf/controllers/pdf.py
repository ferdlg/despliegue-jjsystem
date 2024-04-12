from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import redirect
from django.template.loader import render_to_string
from reportlab.lib.pagesizes import letter, inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from Account.models import Administrador, Pqrsf, Respuestas
import os
from django.contrib import messages
from Account.views import role_required
from django.contrib.auth.decorators import login_required

@login_required
@role_required(1)
def convertir_pqrsf_pdf(request, idpqrsf):
    pqrsf = Pqrsf.objects.get(idpqrsf=idpqrsf)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{pqrsf.idtipopqrsf.nombretipopqrsf}_{pqrsf.idpqrsf}_{pqrsf.fechapqrsf}.pdf"'

    margenes = (50, 50, 50, 50)  
    espacio_entre_tablas = 0.2 * inch 

    pdf = SimpleDocTemplate(response, pagesize=letter, leftMargin=margenes[0], rightMargin=margenes[1], topMargin=margenes[2], bottomMargin=margenes[3])
    elementos = []

    titulo = 'FORMATO DE PQRSF JJSYSTEM PROJECT'
    estilo_titulo = ParagraphStyle(
        name='Titulo',
        fontSize=16,
        leading=20,
        fontName='Helvetica-Bold'
    )

    logo_path = os.path.join(settings.STATICFILES_DIRS[3], 'images', 'logo.png')

    titulo_paragraph = Paragraph(titulo, estilo_titulo)
    logo_img = Image(logo_path, width=110, height=30)

    datos_encabezado_solicitud = [
        ['Bogotá D.C'],
        ['Fecha: ', pqrsf.fechapqrsf],
        ['Peticionario:', f'{pqrsf.idcliente.numerodocumento.nombre} {pqrsf.idcliente.numerodocumento.apellido}'],
        ['No. Documento:', pqrsf.idcliente.numerodocumento.numerodocumento],
        ['Correo electrónico:', pqrsf.idcliente.numerodocumento.email],
        ['Tipo de pqrsf:', pqrsf.idtipopqrsf.nombretipopqrsf],
    ]

    datos_cuerpo_solicitud = [
        ['Estimados JJSystem, '],
        [Paragraph(pqrsf.informacionpqrsf)]
    ]

    datos_pie_pagina = [
        ['© 2024 JJSystem Project. Todos los derechos reservados. El tiempo de respuesta de su solicitud puede variar dependiendo del tipo de PQRSF presentada. Nos esforzamos por atender todas las solicitudes de manera oportuna. Gracias por elegirnos.']
    ]
    estilo_pie_pagina = ParagraphStyle(
        name='EstiloPiePagina',
        fontSize=10,
        textColor='gray',
        alignment=1
    )

    # Estilo para ajuste de texto automático
    tabla_estilo = TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ])

    tabla_logo_titulo = Table([[logo_img, titulo_paragraph]], colWidths=[110, 385], rowHeights=[30])
    tabla_encabezado = Table(datos_encabezado_solicitud, colWidths=[100, 400])
    tabla_cuerpo = Table(datos_cuerpo_solicitud, colWidths=[500])

    tabla_logo_titulo.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.white),  
        ('BOX', (0, 1), (-1, -1), 1, colors.black)
    ]))

    tabla_encabezado.setStyle(tabla_estilo)
    tabla_cuerpo.setStyle(tabla_estilo)

    elementos.append(tabla_logo_titulo)
    elementos.append(Spacer(3, espacio_entre_tablas))  
    elementos.append(tabla_encabezado)
    elementos.append(Spacer(3, espacio_entre_tablas))  
    elementos.append(tabla_cuerpo)

    # Definir función para el pie de página
    def pie_pagina(canvas, doc):
        parrafo_pie_pagina = Paragraph(datos_pie_pagina[0][0], estilo_pie_pagina)
        parrafo_pie_pagina.wrapOn(canvas, doc.width, inch)
        parrafo_pie_pagina.drawOn(canvas, inch, inch)

    # Construir el PDF con la función de pie de página
    pdf.build(elementos, onFirstPage=pie_pagina, onLaterPages=pie_pagina)

    return response

def convertir_respuesta_pdf(request, idpqrsf):
    try:
        respuesta = Respuestas.objects.get(idpqrsf=idpqrsf)
    except Respuestas.DoesNotExist:
        messages.error(request, "Aún no se ha registradodo la respuesta para esta PQRSF.")
        return redirect('homePqrsf')
    pqrsf = Pqrsf.objects.get(idpqrsf = respuesta.idpqrsf.idpqrsf)
    admin = Administrador.objects.get(idadministrador=1)

    response = HttpResponse(content_type = 'application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{pqrsf.idtipopqrsf.nombretipopqrsf}_{pqrsf.idpqrsf}_respuesta_{respuesta.idrespuesta}.pdf"'

    margenes = (50, 50, 50, 50)  
    espacio_entre_tablas = 0.2 * inch 

    pdf = SimpleDocTemplate(response, pagesize=letter, leftMargin=margenes[0], rightMargin=margenes[1], topMargin=margenes[2], bottomMargin=margenes[3])
    elementos = []

    titulo = 'FORMATO DE RESPUESTA-PQRSF JJSYSTEM PROJECT'
    estilo_titulo = ParagraphStyle(
        name='Titulo',
        fontSize=16,
        leading=20,
        fontName='Helvetica-Bold'
    )
    logo_path = os.path.join(settings.STATICFILES_DIRS[3], 'images', 'logo.png')

    titulo_paragraph = Paragraph(titulo, estilo_titulo)
    logo_img = Image(logo_path, width=110, height=30)
    datos_encabezado_solicitud = [
        ['Bogotá D.C'],
        ['Fecha: ', respuesta.fecha],
        ['Peticionario:', f'{pqrsf.idcliente.numerodocumento.nombre} {pqrsf.idcliente.numerodocumento.apellido}'],
        ['No. Documento:', pqrsf.idcliente.numerodocumento.numerodocumento],
        ['Correo electrónico:', pqrsf.idcliente.numerodocumento.email],
        ['Tipo de pqrsf:', pqrsf.idtipopqrsf.nombretipopqrsf],
        ['Encargado PQRSF: ', f'{admin.numerodocumento.nombre} {admin.numerodocumento.apellido}'],
        ['Correo electronico:', admin.numerodocumento.email],
        ['No.Documento:', admin.numerodocumento.numerodocumento]
    ]
    datos_cuerpo_solicitud = [
        ['Estimado(a)' f' {pqrsf.idcliente.numerodocumento.nombre} {pqrsf.idcliente.numerodocumento.apellido},'],
        [Paragraph(respuesta.informacionrespuesta)]
    ]
    datos_pie_pagina = [
        ['© 2024 JJSystem Project. Todos los derechos reservados. Gracias por elegirnos.']
    ]
    estilo_pie_pagina = ParagraphStyle(
        name='EstiloPiePagina',
        fontSize=10,
        textColor='gray',
        alignment=1
    )
        # Estilo para ajuste de texto automático
    tabla_estilo = TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ])

    tabla_logo_titulo = Table([[logo_img, titulo_paragraph]], colWidths=[110, 385], rowHeights=[30])
    tabla_encabezado = Table(datos_encabezado_solicitud, colWidths=[100, 400])
    tabla_cuerpo = Table(datos_cuerpo_solicitud, colWidths=[500])

    tabla_logo_titulo.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.white),  
        ('BOX', (0, 1), (-1, -1), 1, colors.black)
    ]))

    tabla_encabezado.setStyle(tabla_estilo)
    tabla_cuerpo.setStyle(tabla_estilo)

    elementos.append(tabla_logo_titulo)
    elementos.append(Spacer(3, espacio_entre_tablas))  
    elementos.append(tabla_encabezado)
    elementos.append(Spacer(3, espacio_entre_tablas))  
    elementos.append(tabla_cuerpo)

    # Definir función para el pie de página
    def pie_pagina(canvas, doc):
        parrafo_pie_pagina = Paragraph(datos_pie_pagina[0][0], estilo_pie_pagina)
        parrafo_pie_pagina.wrapOn(canvas, doc.width, inch)
        parrafo_pie_pagina.drawOn(canvas, inch, inch)

    # Construir el PDF con la función de pie de página
    pdf.build(elementos, onFirstPage=pie_pagina, onLaterPages=pie_pagina)

    return response