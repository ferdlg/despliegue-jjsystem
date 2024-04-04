from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

from .controllers.envios import enviosCRUD
from .controllers.estadosenvios import estadosenviosCRUD
from .controllers.tecnicos import tecnicosCRUD
from .controllers.ventas import ventasCRUD

router = DefaultRouter()
router.register(r'envios', enviosCRUD)
router.register(r'estadoenvios', estadosenviosCRUD)
router.register(r'tecnicos', tecnicosCRUD)
router.register(r'ventas', ventasCRUD)

urlpatterns=[
    path('', views.homeEnvios, name='homeEnvios'),
    path('create/', views.createEnvioView, name='createEnvio'),
    path('editarEnvio/<idEnvio>', views.editarEnvio, name='editarEnvio'),
    path('eliminarEnvio/<idEnvio>', views.eliminarEnvio, name='eliminarEnvio'),
    path('tecnicos/', views.homeEnviosTecnico, name='homeTecnicosEnvios'),
    path('api/', include(router.urls)),

    path('clientes/', views.enviosCliente, name='vista_cliente'),
    path('historialEnvios/', views.historialEnviosCliente, name='historial_envios_cliente'),
    path('generar_pdf/<str:templateName>/', views.generar_pdf, name='generar_pdf_envios'),


]
