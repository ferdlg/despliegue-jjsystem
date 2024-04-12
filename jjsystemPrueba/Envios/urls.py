from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

from .controllers.envios import enviosCRUD
from .controllers.estadosenvios import estadosenviosCRUD
from .controllers.tecnicos import tecnicosCRUD
from .controllers.ventas import ventasCRUD
from .controllers.pdf import generar_pdf, generar_pdf_envio

router = DefaultRouter()
router.register(r'envios', enviosCRUD)
router.register(r'estadoenvios', estadosenviosCRUD)
router.register(r'tecnicos', tecnicosCRUD)
router.register(r'ventas', ventasCRUD)

urlpatterns=[
    path('', views.homeEnvios, name='homeEnvios'),
    path('create/', views.createEnvioView, name='createEnvio'),
    path('editarEnvio/<idenvio>', views.editarEnvio, name='editarEnvio'),
    path('eliminarEnvio/<idenvio>', views.eliminarEnvio, name='eliminarEnvio'),
    path('tecnicos/', views.homeEnviosTecnico, name='homeTecnicosEnvios'),
    path('api/', include(router.urls)),

    path('clientes/', views.enviosCliente, name='vista_cliente'),
    path('historialEnvios/', views.historialEnviosCliente, name='historial_envios_cliente'),
    path('generar_pdf/<str:templateName>/', generar_pdf, name='generar_pdf_envios'),
    path('generar_pdf_envio/<int:idenvio>/', generar_pdf_envio, name='generar_pdf_envio'),


]
