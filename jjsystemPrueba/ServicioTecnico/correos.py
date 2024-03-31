from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from Account.models import Clientes, Tecnicos, Citas
from django.conf import settings
from django.contrib import messages

def correo_bienvenida_tecnico(request,idtecnico):
    tecnico = Tecnicos.objects.get(idtecnico)
    return

def correo_cotizacion_registrada():
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