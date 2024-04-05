from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from Account.models import Clientes, Cotizaciones, Tecnicos, Citas
from django.conf import settings
from django.contrib import messages
from .controllers.pdf import generar_pdf

def correo_bienvenida_tecnico(request,idtecnico):
        tecnico = Tecnicos.objects.get(idtecnico=idtecnico)
        email = tecnico.numerodocumento.email
        password = tecnico.numerodocumento  

        asunto = 'Bienvenido a JJSystemProject'
        html_message_tecnico = render_to_string('correo_bienvenida_tecnico.html', {'tecnico': tecnico, 'password': password})
        correo_origen = settings.EMAIL_HOST_USER
        send_mail(asunto, '', correo_origen, [email], html_message=html_message_tecnico)
        return None


def correo_confirmacion_compra(request, idcliente,idcotizacion):
    cliente = Clientes.objects.get(idcliente=idcliente)
    cotizacion = Cotizaciones.objects.get(idcotizacion=idcotizacion)

    pdf = generar_pdf(request, idcotizacion)
    asunto = 'Se ha respondido tu cotizacion!'
    
    email_cliente = cliente.numerodocumento.email
    correo_origen = settings.EMAIL_HOST_USER
    html_message_cliente = render_to_string('correos/respuesta_cotizacion.html',{'cotizacion':cotizacion, 'cliente':cliente, 'destinatario':'Cliente'})
    send_mail(asunto, '', correo_origen, [email_cliente], html_message=html_message_cliente, fail_silently=False, attachments=[('cotizacion.pdf', pdf, 'application/pdf')])
    return None 

def correo_fechas_disponibles_cita(request, ):

    return

def correo_cotizacion_aceptada():
    return

def correo_fechas_disponibles_citas():
    return

def correo_cita_agendada(request, idcliente, idtecnico, idcita):
    cliente = Clientes.objects.get(idcliente=idcliente)
    tecnico = Tecnicos.objects.get(idtecnico=idtecnico)
    cita = Citas.objects.get(idcita = idcita)

    asunto_cliente = 'Se ha agendado tu cita'
    asunto_tecnico = 'Nueva asignación de cita'

    html_message_cliente = render_to_string('correo_asignacion_cita.html', {'cliente': cliente, 'tecnico': tecnico, 'cita': cita, 'destinatario': 'Cliente'})
    html_message_tecnico = render_to_string('correo_asignacion_cita.html', {'cliente': cliente, 'tecnico': tecnico, 'cita': cita, 'destinatario': 'Tecnico'})

    email_cliente = cliente.numerodocumento.email
    email_tecnico = tecnico.numerodocumento.email

    correo_origen = settings.EMAIL_HOST_USER

    send_mail(asunto_cliente, '', correo_origen, [email_cliente], html_message=html_message_cliente)
    send_mail(asunto_tecnico, '', correo_origen, [email_tecnico], html_message=html_message_tecnico)

    return None
