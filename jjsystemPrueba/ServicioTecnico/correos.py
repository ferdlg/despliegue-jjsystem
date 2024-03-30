from django.core.mail import send_mail
from django.shortcuts import render
from django.template.loader import render_to_string
from Account.models import Clientes, Tecnicos
from django.conf import settings
from django.contrib import messages

def correo_bienvenida_tecnico():
    return

def correo_cotizacion_registrada():
    return

def correo_cotizacion_aceptada():
    return

def correo_fechas_disponibles_citas():
    return

def correo_cita_agendada(request, idcliente, idtecnico):
    cliente = Clientes.objects.get(idcliente=idcliente)
    tecnico = Tecnicos.objects.get(idtecnico=idtecnico)

    asunto_cliente = 'Se ha agendado tu cita'
    asunto_tecnico = 'Nueva asignación de cita'

    html_message = render_to_string('correo_template.html', {'cliente': cliente, 'tecnico': tecnico})

    email_cliente = cliente.email
    email_tecnico = tecnico.email

    correo_origen = settings.EMAIL_HOST_USER

    send_mail(asunto_cliente, '', correo_origen, [email_cliente], html_message=html_message)
    send_mail(asunto_tecnico, '', correo_origen, [email_tecnico], html_message=html_message)
