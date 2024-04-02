from django.utils import timezone
from rest_framework import viewsets
from Account.models import *
from .serializers import PqrsfSerializer
from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch


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
    
    def crear_pqrsf(self, request):
        try:
            if request.method == 'POST':
                numerodocumento = request.user.numerodocumento
                cliente = Clientes.objects.get(numerodocumento=numerodocumento)
                fechapqrsf = timezone.now().date()
                informacionpqrsf = request.POST.get('informacionpqrsf')
                tipo = request.POST.get('idtipopqrsf')

                estadopqrsf = Estadospqrsf.objects.get(nombreestadopqrsf='Solicitada')
                tipopqrsf = Tipospqrsf.objects.get(idtipopqrsf=tipo)

                pqrsf = Pqrsf.objects.create(
                    idcliente=cliente,
                    fechapqrsf=fechapqrsf,
                    informacionpqrsf=informacionpqrsf,
                    idestadopqrsf=estadopqrsf,
                    idtipopqrsf=tipopqrsf
                )
                messages.success(request, 'Cotización registrada correctamente')
        except Clientes.DoesNotExist:
            messages.error(request, 'Cliente no encontrado')
        except Estadospqrsf.DoesNotExist:
            messages.error(request, 'Estado de PQRSF no encontrado')
        except Tipospqrsf.DoesNotExist:
            messages.error(request, 'Tipo de PQRSF no encontrado')
        
        return redirect('ir_a_pqrsf') 
    
def convertir_pqrsf_pdf(request, idpqrsf):
    pqrsf = Pqrsf.objects.get(idpqrsf=idpqrsf)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{pqrsf.idtipopqrsf.nombretipopqrsf}_{idpqrsf}.pdf"'

    # Configurar márgenes y espacio entre tablas
    margenes = (50, 50, 50, 50)  # (izquierda, derecha, arriba, abajo)
    espacio_entre_tablas = 0.5 * inch  # Espacio de 0.5 pulgadas
    pdf = SimpleDocTemplate(response, pagesize=letter, leftMargin=margenes[0], rightMargin=margenes[1], topMargin=margenes[2], bottomMargin=margenes[3])
    elementos = []

    datos_encabezado_solicitud = [
        ['Ubicación:', 'Bogotá D.C'],
        ['Fecha: ', pqrsf.fechapqrsf],
        ['Nombres del peticionario:', pqrsf.idcliente.numerodocumento.nombre],
        ['Apellidos del peticionario:', pqrsf.idcliente.numerodocumento.apellido],
        ['Número de documento:', pqrsf.idcliente.numerodocumento],
        ['Correo electrónico:', pqrsf.idcliente.numerodocumento.email],
    ]

    datos_cuerpo_solicitud = [
        ['Tipo:', pqrsf.idtipopqrsf.nombretipopqrsf],
        ['Descripción:', pqrsf.informacionpqrsf]
    ]

    # Estilo para ajuste de texto automático
    tabla_estilo = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
    ])

    tabla_encabezado = Table(datos_encabezado_solicitud, colWidths=[150, 200])
    tabla_encabezado.setStyle(tabla_estilo)

    tabla_cuerpo = Table(datos_cuerpo_solicitud, colWidths=[150, 400])
    tabla_cuerpo.setStyle(tabla_estilo)

    # Insertar espacio entre las tablas
    elementos.append(tabla_encabezado)
    elementos.append(Spacer(1, espacio_entre_tablas))  # Spacer horizontal de 1 unidad x espacio_entre_tablas
    elementos.append(tabla_cuerpo)

    pdf.build(elementos)

    return response