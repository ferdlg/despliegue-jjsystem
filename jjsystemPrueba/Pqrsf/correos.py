from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from Account.models import Clientes, Pqrsf, Respuestas, Administrador
from django.conf import settings
from .controllers.pdf import convertir_pqrsf_pdf

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
    pqrsf = Pqrsf.objects.get(idpqrsf=idpqrsf)
    cliente = Clientes.objects.get(idcliente=pqrsf.idcliente)
    admin = Administrador.objects.get(idadministrador=3)

    email_cliente = cliente.numerodocumento.email
    email_admin = admin.numerodocumento.email

    asunto_cliente = f'Confirmación: Se ha enviado con éxito tu {pqrsf.idtipopqrsf.nombretipopqrsf}'
    asunto_admin = f'Se ha registrado un(a) nuevo(a) {pqrsf.idtipopqrsf.nombretipopqrsf}'

    pdf_content = convertir_pqrsf_pdf(request, idpqrsf=idpqrsf)
    pdf_filename = f'{pqrsf.idtipopqrsf.nombretipopqrsf}_{idpqrsf}.pdf'

    correo_cliente = EmailMultiAlternatives(asunto_cliente, '', settings.EMAIL_HOST_USER, [email_cliente])
    correo_admin = EmailMultiAlternatives(asunto_admin, '', settings.EMAIL_HOST_USER, [email_admin])

    correo_cliente.attach(pdf_filename, pdf_content, 'application/pdf')
    correo_admin.attach(pdf_filename, pdf_content, 'application/pdf')

    html_message_cliente = render_to_string('correo_confirmacion_pqrsf_cliente_admin.html', {'cliente': cliente, 'pqrsf': pqrsf, 'destinatario': 'Cliente'})
    html_message_admin = render_to_string('correo_confirmacion_pqrsf_cliente_admin.html', {'cliente': cliente, 'pqrsf': pqrsf, 'destinatario': 'Administrador'})

    correo_cliente.attach_alternative(html_message_cliente, 'text/html')
    correo_admin.attach_alternative(html_message_admin, 'text/html')

    send_mail(correo_cliente)
    send_mail(correo_admin)
    return None



