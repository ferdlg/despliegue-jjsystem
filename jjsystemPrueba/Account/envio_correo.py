from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from Account.models import *
from django.conf import settings
from django.contrib import messages

def enviar_correo_registro(email_cliente):
    # Renderizar el mensaje del correo electrónico
    html_message = render_to_string('correo_registro.html')

    # Asunto del correo electrónico
    asunto = 'Gracias por registrarte'

    try:
        # Enviar el correo electrónico y obtener el resultado
        resultado_envio = send_mail(asunto, '', settings.EMAIL_HOST_USER, [email_cliente], html_message=html_message)
        
        # Imprimir el resultado del envío del correo electrónico
        print("Resultado del envío del correo electrónico:", resultado_envio)
        
    except Exception as e:
        # Imprimir el error si ocurre algún problema al enviar el correo electrónico
        print("Error al enviar el correo electrónico:", e)
