from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from Account.models import *
from Account.views import role_required
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from io import BytesIO
from django.template.loader import get_template
from django.template import Context
from Account.models import *
from django.db import connection
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
            # Convertir idtecnico a entero
            idtecnico = int(idtecnico)
            
            # Obtener la instancia de Tecnicos
            idtecnico = Tecnicos.objects.get(idtecnico=idtecnico)

            # Obtener la instancia de Estadosenvios
            estado = Estadosenvios.objects.get(idestadoenvio=idestadoenvio)

            # Crear la instancia de Envios
            envio = Envios.objects.create(
                direccionenvio=direccion,
                idtecnico=idtecnico,
                idestadoenvio=estado
            )

            return redirect('homeEnvios')

        except Tecnicos.DoesNotExist:
            print("Error: No se encontró el Técnico.")
        except Estadosenvios.DoesNotExist:
            print("Error: No se encontró el Estado de Envío.")

    estados = Estadosenvios.objects.all()
    return render(request, "crudAdmin/Create.html", {"estados": estados})

#@login_required
#@role_required(1)
def editarEnvio(request, idEnvio):
    envio = Envios.objects.get(idenvio=idEnvio)
    estados = Estadosenvios.objects.all()

    if request.method == 'POST':
        # Obtener los datos de la petición
        direccion = request.POST.get('direccion')
        idtecnico = int(request.POST.get('idtecnico'))
        idestadoenvio = int(request.POST.get('estado'))

        # Obtener las instancias de Tecnicos y Estadosenvios
        idtecnico = Tecnicos.objects.get(idtecnico=idtecnico)
        idestadoenvio = Estadosenvios.objects.get(idestadoenvio=idestadoenvio)

        # Actualizar los campos del objeto envio
        envio.direccionenvio = direccion
        envio.idtecnico = idtecnico
        envio.idestadoenvio = idestadoenvio
        envio.save()

        return redirect('homeEnvios')

    return render(request, "crudAdmin/Editar.html", {"envio": envio, "estados": estados})

#@login_required
#@role_required(1)
def eliminarEnvio(request, idEnvio):
    envio = Envios.objects.get(idenvio = idEnvio)
    envio.delete()

    return redirect('homeEnvios')

def detallesView(request, idEnvio):
    detallesEnvio = DetalleEnviosVentas.objects.get(idenvio=idEnvio)
    return render(request, 'crudAdmin/Detalles.html', {'detallesEnvio': detallesEnvio})



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

    # Obtener los ids de envío asociados a estas ventas
    ids_envios = ventas_con_envio.values_list('idenvio', flat=True)

    # Obtener los objetos de envío correspondientes a los ids de envío obtenidos
    envios = Envios.objects.filter(idenvio__in=ids_envios)

    return render(request, 'cliente/EnviosCliente.html', {'envios': envios})

    
def historialEnviosCliente(request):
    # Obtener el número de documento del cliente autenticado
    numerodocumento = request.user.numerodocumento

    # Obtener todas las ventas del cliente autenticado que tienen un envío asociado
    ventas_con_envio = Ventas.objects.filter(idcotizacion__idcliente__numerodocumento=numerodocumento, idenvio__isnull=False)

    # Obtener los ids de envío asociados a estas ventas
    ids_envios = ventas_con_envio.values_list('idenvio', flat=True)

    # Obtener los objetos de envío correspondientes a los ids de envío obtenidos
    envios = Envios.objects.filter(idenvio__in=ids_envios)

    # Filtrar solo los envíos con estado "Entregado"
    envios_entregados = envios.filter(idestadoenvio__nombreestadoenvio="Entregado")

    return render(request, 'cliente/HistorialEnviosCliente.html', {'envios': envios_entregados})

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




