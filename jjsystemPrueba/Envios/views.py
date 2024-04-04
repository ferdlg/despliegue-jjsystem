from pyexpat.errors import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from Account.models import *
from Account.views import role_required
from django.http import HttpResponse, HttpResponseRedirect
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from io import BytesIO
from django.template.loader import get_template
from django.core.exceptions import ObjectDoesNotExist
from django.template import Context
from Account.models import *
from django.db import connection
import smtplib
import os
# from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jjsystemPrueba import settings
from .envio_correo import enviar_correo_estado_envio
# Create your views here.

def homeEnvios(request):
    search_query = request.GET.get('search', '')
    estado_filter = request.GET.get('estado', '')  # Obtener el valor del filtro por estado

    envios = Envios.objects.all()

    # Filtrar los envíos por dirección si hay un término de búsqueda
    if search_query:
        envios = envios.filter(direccionenvio__icontains=search_query)
    
    # Filtrar los envíos por estado si se ha seleccionado un estado en el filtro
    if estado_filter:
        envios = envios.filter(idestadoenvio=estado_filter)

    paginator = Paginator(envios, 5)  # Dividir los resultados en páginas, 5 por página
    page_number = request.GET.get('page')  # Obtener el número de página de la URL
    try:
        envios = paginator.page(page_number)
    except PageNotAnInteger:
        # Si el número de página no es un número entero, mostrar la primera página
        envios = paginator.page(1)
    except EmptyPage:
        # Si el número de página está fuera de rango (por encima de la última página), mostrar la última página de resultados
        envios = paginator.page(paginator.num_pages)
    
    # Obtener todos los detalles de envío
    detallesEnvio = DetalleEnviosVentas.objects.all()

    # Obtener todos los estados de envío para el menú desplegable de filtro
    estados = Estadosenvios.objects.all()

    return render(request, "crudAdmin/Index.html", {"envios": envios, "search_query": search_query, "detallesEnvio": detallesEnvio, "estados": estados})



#@login_required
#@role_required(1)
def createEnvioView(request):
    if request.method == 'POST':
        direccion = request.POST.get('direccion')
        idtecnico = request.POST.get('idtecnico')
        idestadoenvio = request.POST.get('estado')

        try:
            idtecnico = int(idtecnico)
            tecnico = Tecnicos.objects.get(idtecnico=idtecnico)
            estado = Estadosenvios.objects.get(idestadoenvio=idestadoenvio)

            # Crear el envío
            envio = Envios.objects.create(
                direccionenvio=direccion,
                idtecnico=tecnico,
                idestadoenvio=estado
            )

            # Redireccionar después de crear el envío
            return redirect('homeEnvios')

        except Tecnicos.DoesNotExist:
            messages.error(request, 'Error: No se encontró el Técnico.')
            return redirect('homeEnvios')
        except Estadosenvios.DoesNotExist:
            messages.error(request, 'Error: No se encontró el Estado de Envío.')
            return redirect('homeEnvios')

    estados = Estadosenvios.objects.all()
    tecnicos = Tecnicos.objects.all()  # Obtener todos los técnicos
    return render(request, "crudAdmin/Create.html", {"estados": estados, "tecnicos": tecnicos})

#@login_required
#@role_required(1)

def editarEnvio(request, idEnvio):
    idenvio = None  # Asignar un valor por defecto

    try:
        envio = Envios.objects.get(idenvio=idEnvio)
        estados = Estadosenvios.objects.all()
        tecnicos = Tecnicos.objects.all()
    except ObjectDoesNotExist:
        messages.error(request, 'No se pudo encontrar el envío solicitado.')
        return redirect('homeEnvios')

    if request.method == 'POST':
        try:
            # Obtener los datos de la petición
            direccion = request.POST.get('direccion')
            idtecnico = int(request.POST.get('idtecnico'))
            idestadoenvio = int(request.POST.get('estado'))

            # Obtener las instancias de Tecnicos y Estadosenvios
            tecnico = Tecnicos.objects.get(idtecnico=idtecnico)
            estado_envio = Estadosenvios.objects.get(idestadoenvio=idestadoenvio)

            # Actualizar los campos del objeto envio
            envio.direccionenvio = direccion
            envio.idtecnico = tecnico
            envio.idestadoenvio = estado_envio
            envio.save()

            # Obtener el correo electrónico del cliente asociado al envío
            try:
                envio_usuario = EnviosUsuarios.objects.get(idEnvio=idEnvio)
                email_cliente = envio_usuario.emailCliente
            except EnviosUsuarios.DoesNotExist:
                messages.error(request, 'No se pudo encontrar el cliente asociado al envío.')
                return redirect('homeEnvios')

            # Envío de correo electrónico al cliente con el estado actualizado
            detalles_envio = DetalleEnviosVentas.objects.get(idenvio=idEnvio)  # <-- Usar idenvio
            idenvio = detalles_envio.idenvio

            # Agregar impresión para verificar los parámetros
            print("Parámetros de la función enviar_correo_estado_envio:", email_cliente,idenvio)

            # Llamar a la función enviar_correo_estado_envio
            enviar_correo_estado_envio(request, email_cliente,idenvio)

            print("Correo electrónico enviado correctamente a:", email_cliente)

            return redirect('homeEnvios')
        except Exception as e:
            # Agregar impresión para verificar errores
            print("Error al enviar el correo electrónico:", str(e))
            return redirect('homeEnvios')

    return render(request, "crudAdmin/Editar.html", {"envio": envio, "estados": estados, "tecnicos": tecnicos})

#@login_required
#@role_required(1)
def eliminarEnvio(request, idEnvio):
    try:
        envio = Envios.objects.get(idenvio=idEnvio)
    except ObjectDoesNotExist:
        messages['error'] = 'El envío que intenta eliminar no existe.'
        return redirect('homeEnvios')

    try:
        envio.delete()
        messages['success'] = 'Envío eliminado con éxito'
    except Exception as e:
        messages['error'] = f'Ocurrió un error al eliminar el envío: {str(e)}'

    return redirect('homeEnvios')
#Views del tecnico

#@login_required
#@role_required(1)
def homeEnviosTecnico(request):
    # Obtener el número de documento del técnico autenticado
    numerodocumento = request.user.numerodocumento
    # Obtener todos los envíos asignados al técnico autenticado
    envios_tecnico = Envios.objects.filter(idtecnico__numerodocumento=numerodocumento)
    return render(request, 'tecnico/IndexTecnico.html', {'envios': envios_tecnico})


#Views cliente

def enviosCliente(request):
    # Obtener el número de documento del cliente autenticado
    numerodocumento = request.user.numerodocumento

    # Obtener todas las ventas del cliente autenticado que tienen un envío asociado
    ventas_con_envio = Ventas.objects.filter(idcotizacion__idcliente__numerodocumento=numerodocumento, idenvio__isnull=False)
    detallesEnvio = DetalleEnviosVentas.objects.all()
    # Obtener los ids de envío asociados a estas ventas
    ids_envios = ventas_con_envio.values_list('idenvio', flat=True)

    # Obtener los objetos de envío correspondientes a los ids de envío obtenidos
    envios = Envios.objects.filter(idenvio__in=ids_envios)

    return render(request, 'cliente/EnviosCliente.html', {'envios': envios, "detallesEnvio": detallesEnvio})

    
def historialEnviosCliente(request):
    # Obtener el número de documento del cliente autenticado
    numerodocumento = request.user.numerodocumento

    # Obtener todas las ventas del cliente autenticado que tienen un envío asociado
    ventas_con_envio = Ventas.objects.filter(idcotizacion__idcliente__numerodocumento=numerodocumento, idenvio__isnull=False)
    detallesEnvio = DetalleEnviosVentas.objects.all()
    # Obtener los ids de envío asociados a estas ventas
    ids_envios = ventas_con_envio.values_list('idenvio', flat=True)

    # Obtener los objetos de envío correspondientes a los ids de envío obtenidos
    envios = Envios.objects.filter(idenvio__in=ids_envios)

    # Filtrar solo los envíos con estado "Entregado"
    envios_entregados = envios.filter(idestadoenvio__nombreestadoenvio="Entregado")

    return render(request, 'cliente/HistorialEnviosCliente.html', {'envios': envios_entregados, "detallesEnvio": detallesEnvio})

#PDF

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

    logo_path = os.path.join(settings.STATICFILES_DIRS[3], 'images/logo.png')
    # Aplicar estilos a la tabla
    estilo_tabla = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                               ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                               ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                               ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                               ('GRID', (0, 0), (-1, -1), 1, colors.black)])

    tabla.setStyle(estilo_tabla)

    # Agregar la tabla al documento
    elementos = []
    elementos.append(tabla)
    doc.build(elementos)

    # Obtener el PDF generado
    pdf = buffer.getvalue()
    buffer.close()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="envios.pdf"'
    response.write(pdf)
    return response





