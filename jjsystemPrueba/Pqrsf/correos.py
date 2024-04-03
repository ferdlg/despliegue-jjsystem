from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from Account.models import Clientes, Pqrsf, Respuestas, Administrador
from django.conf import settings
from django.contrib import messages

def correo_respuesta_cliente(request, idpqrsf):
    pqrsf = Pqrsf.objects.get(idpqrsf = idpqrsf)
    cliente = Clientes.objects.get(idcliente = pqrsf.idcliente)
    email = cliente.numerodocumento.email

    asunto = (f'Respuesta a tu {pqrsf.idtipopqrsf.nombretipopqrsf}')
    correo_origen = settings.EMAIL_HOST_USER

    #llamar a la funcion que convierte en pdf la respuesta a la PQRSF 
    html_message = render_to_string('correo_respuesta_cliente.html', {'pqrsf': pqrsf})
    send_mail(asunto, '', correo_origen, [email], html_message=html_message)
    return None

def correo_confirmacion_pqrsf_cliente_admin(request, idpqrsf):
    pqrsf = Pqrsf.objects.get(idpqrsf = idpqrsf)
    cliente = Clientes.objects.get(idcliente = pqrsf.idcliente)
    admin = Administrador.objects.get(idadministrador = 3)

    email_cliente = cliente.numerodocumento.email
    email_admin = admin.numerodocumento.email

    asunto_cliente = (f'Confirmacion: Se ha enviado con exito tu {pqrsf.idtipopqrsf.nombretipopqrsf}')
    asunto_admin = (f'Se ha registrado un(a) nuevo(a) {pqrsf.idtipopqrsf.nombretipopqrsf}')

    html_message_cliente = render_to_string('correo_confirmacion_pqrsf_cliente_admin.html', {'cliente': cliente, 'pqrsf': pqrsf, 'destinatario': 'Cliente'})
    html_message_admin = render_to_string('correo_confirmacion_pqrsf_cliente_admin.html', {'cliente': cliente, 'pqrsf': pqrsf, 'destinatario': 'Administrador'})

    correo_origen = settings.EMAIL_HOST_USER

    #Llamar a la funcio que convierte en pdf la pqrsf
    send_mail(asunto_cliente, '', correo_origen, [email_cliente], html_message=html_message_cliente)
    send_mail(asunto_admin, '', correo_origen, [email_admin], html_message=html_message_admin)

    return None



