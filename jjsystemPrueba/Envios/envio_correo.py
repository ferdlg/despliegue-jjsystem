from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from Account.models import *
from django.conf import settings
from django.contrib import messages

def enviar_correo_estado_envio(request, email_cliente, idenvio):
    detalles_envio = DetalleEnviosVentas.objects.get(idenvio = idenvio)
    envio = Envios.objects.get(idenvio = idenvio)

    html_message_cliente = render_to_string('estado_envio.html', {'detalles_envio': detalles_envio, 'envio':envio})
    asunto = 'Actualización del estado de envío'

    send_mail(asunto, '', settings.EMAIL_HOST_USER, [email_cliente], html_message=html_message_cliente)

    return None