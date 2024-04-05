from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from Account.models import Administrador, Clientes, Cotizaciones, Tecnicos, Citas
from django.conf import settings
from django.contrib import messages

from ServicioTecnico.controllers.cronogramatecnicos import obtener_disponibilidad_tecnico
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

def correo_respuesta_cotizacion(request, idcotizacion):
    cotizacion = get_object_or_404(Cotizaciones, idcotizacion=idcotizacion)
    cliente = get_object_or_404(Clientes, idcliente=cotizacion.idcliente.idcliente)
    
    pdf = generar_pdf(request, idcotizacion)

    asunto = 'Respuesta a tu cotización'
    correo_origen = settings.EMAIL_HOST_USER
    email_cliente = cliente.numerodocumento.email
    html_message_cliente = render_to_string('correos/respuesta_cotizacion.html', {'cotizacion': cotizacion, 'cliente': cliente, 'destinatario': 'Cliente'})

    mensaje_correo = EmailMultiAlternatives(asunto, '', correo_origen, [email_cliente])
    mensaje_correo.attach_alternative(html_message_cliente, "text/html")
    mensaje_correo.attach('cotizacion.pdf', pdf.getvalue(), 'application/pdf')

    mensaje_correo.send(fail_silently=False)
    messages.success(request, 'Se ha enviado el correo de respuesta')
    return redirect('ver_cotizaciones')

def correo_fechas_disponibles_cita(request, idcotizacion):
    if request.method == 'POST':
        cotizacion = get_object_or_404(Cotizaciones, idcotizacion=idcotizacion)
        cliente = get_object_or_404(Clientes, idcliente=cotizacion.idcliente.idcliente)

        idtecnico = request.POST.get('idtecnico')
        tecnico = get_object_or_404(Tecnicos, idtecnico=idtecnico)
        fechas_disponibles = obtener_disponibilidad_tecnico(idtecnico)

        asunto_cliente = 'Agenda tu cita: Fechas Disponibles'
        correo_origen = settings.EMAIL_HOST_USER
        email_cliente = cliente.numerodocumento.email
        html_message_cliente = render_to_string('correos/fechas_disponibles.html', {'cotizacion': cotizacion, 'cliente': cliente, 'destinatario': 'Cliente', 'fechas_disponibles':fechas_disponibles})

        send_mail(asunto_cliente, '', correo_origen, [email_cliente], html_message=html_message_cliente)
        messages.success(request, 'Se ha enviado el correo con las fechas disponibles')
        return redirect('ver_cotizaciones')

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
