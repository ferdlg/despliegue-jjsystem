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
    cliente = Clientes.objects.get(idcliente = pqrsf.idcliente.idcliente)
    email = cliente.numerodocumento.email

    asunto = (f'Respuesta a tu {pqrsf.idtipopqrsf.nombretipopqrsf}')
    correo_origen = settings.EMAIL_HOST_USER

    html_message = render_to_string('correos/correo_respuesta_cliente.html', {'pqrsf': pqrsf, 'cliente':cliente})
    send_mail(asunto, '', correo_origen, [email], html_message=html_message)
    return None

def correo_confirmacion_pqrsf_cliente_admin(request, idpqrsf):
    pqrsf = Pqrsf.objects.get(idpqrsf=idpqrsf)
    cliente = Clientes.objects.get(idcliente=pqrsf.idcliente.idcliente)
    admin = Administrador.objects.get(idadministrador = 1)

    email_cliente = cliente.numerodocumento.email
    email_admin = admin.numerodocumento.email
    correo_origen = settings.EMAIL_HOST_USER

    asunto_cliente = f'Confirmación: Se ha enviado con éxito tu {pqrsf.idtipopqrsf.nombretipopqrsf}'
    asunto_admin = f'Se ha registrado un(a) nuevo(a) {pqrsf.idtipopqrsf.nombretipopqrsf}'

    html_message_cliente = render_to_string('correos/correo_confirmacion_pqrsf_cliente_admin.html',{'pqrsf':pqrsf, 'cliente':cliente, 'destinatario':'Cliente'})
    html_message_administrador = render_to_string('correos/correo_confirmacion_pqrsf_cliente_admin.html',{'pqrsf':pqrsf, 'administrador':admin, 'destinatario':'Administrador'})

    send_mail(asunto_cliente, '', correo_origen, [email_cliente], html_message=html_message_cliente)
    send_mail(asunto_admin, '', correo_origen, [email_admin], html_message=html_message_administrador)

    return None


