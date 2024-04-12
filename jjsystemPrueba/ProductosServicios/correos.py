from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from Account.models import Clientes, Cotizaciones, Administrador
from django.conf import settings
from ServicioTecnico.controllers.pdf import generar_pdf

def correo_confirmacion_cotizacion(request, idcotizacion):
    cotizacion = Cotizaciones.objects.get(idcotizacion = idcotizacion)
    cliente = Clientes.objects.get(idcliente=cotizacion.idcliente.idcliente)
    admin = Administrador.objects.get(idadministrador = 1)

    email_cliente = cliente.numerodocumento.email
    email_admin = admin.numerodocumento.email
    correo_origen = settings.EMAIL_HOST_USER

    asunto_cliente = f'Confirmación: Se ha registrado con éxito tu cotización'
    asunto_admin = f'Notificación: Se ha registrado una nueva cotizacion'

    html_message_cliente = render_to_string('correos/confirmacion_cotizacion.html',{'cotizacion':cotizacion, 'cliente':cliente, 'destinatario':'Cliente'})
    html_message_administrador = render_to_string('correos/confirmacion_cotizacion.html',{'cotizacion':cotizacion, 'administrador':admin, 'destinatario':'Administrador'})

    send_mail(asunto_cliente, '', correo_origen, [email_cliente], html_message=html_message_cliente)
    send_mail(asunto_admin, '', correo_origen, [email_admin], html_message=html_message_administrador)
    return None

def correo_confirmacion_compra(request, idcotizacion):
    cotizacion = get_object_or_404(Cotizaciones, idcotizacion=idcotizacion)
    cliente = get_object_or_404(Clientes, idcliente=cotizacion.idcliente.idcliente)
    admin = Administrador.objects.get(idadministrador = 1)

    asunto_cliente = 'Confirmación de tu compra'
    asunto_admin = 'Nueva venta: confirmacion de compra'

    email_cliente = cliente.numerodocumento.email
    email_admin = admin.numerodocumento.email
    correo_origen = settings.EMAIL_HOST_USER

    html_message_cliente = render_to_string('correos/confirmacion_compra.html',{'cotizacion':cotizacion, 'cliente':cliente, 'destinatario':'Cliente'})
    html_message_administrador = render_to_string('correos/confirmacion_compra.html',{'cotizacion':cotizacion, 'administrador':admin, 'destinatario':'Administrador'})

    send_mail(asunto_cliente, '', correo_origen, [email_cliente], html_message=html_message_cliente)
    send_mail(asunto_admin, '', correo_origen, [email_admin], html_message=html_message_administrador)
    return redirect('')
