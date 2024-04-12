from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .controllers.cotizaciones import CotizacionesCRUD

from .controllers.citas import citasCRUD
from .controllers.pdf import generar_pdf
from .controllers.cronogramatecnicos import cronogramatecnicosCRUD
from .controllers.estadocotizaciones import estadocotizacionesCRUD
from .controllers.tecnicos import tecnicosCRUD, tecnico_home, mi_agenda, mis_actividades, mis_citas
from .controllers.clientes import ClientesCRUD
from .correos import correo_respuesta_cotizacion, correo_fechas_disponibles_cita

#urls back 

router = DefaultRouter()
router.register(r'citas',citasCRUD)
router.register(r'cotizaciones', CotizacionesCRUD)
router.register(r'cronograma_tecnicos', cronogramatecnicosCRUD)
router.register(r'estado_cotizaciones',estadocotizacionesCRUD)
router.register(r'tecnicos', tecnicosCRUD)
router.register(r'clientes', ClientesCRUD)


# urls front 
from .views import index, inicio, indexTecnicos, mi_perfil, validar_contrasena, cambiar_contrasena

urlpatterns=[
    path('',include(router.urls)),
    path('inicio/', inicio, name = 'inicio'),
    path('index/', index , name='index'),
    path('index/mi_perfil/', mi_perfil, name='mi_perfil'),
    path('mi_perfil/validar_password/', validar_contrasena, name='index_validar_password'),
    path('mi_perfil/validar_password/cambiar_password/', cambiar_contrasena, name='index_cambiar_password'),
    path('index/tecnicos/', indexTecnicos, name='indexTecnicos'),
    path('index/tecnicos/ver_tecnicos', tecnicosCRUD.as_view({'post':'listar_tecnicos','get':'listar_tecnicos'}), name='verTecnicos'),
    path('index/tecnicos/editar_datos/<idtecnico>',tecnicosCRUD.as_view({'post':'editar_datos_tecnico', 'get':'editar_datos_tecnico'}), name='editar_datos_tecnico'),
    path('eliminar-tecnico/<int:idtecnico>/', tecnicosCRUD.as_view({'post': 'eliminar_tecnico','get': 'eliminar_tecnico'}), name='eliminar_tecnico'),
    path('registrar_tecnico/', tecnicosCRUD.as_view({'post': 'registrar_tecnico'}), name='registrar_tecnico'),
    path('index/ver_clientes/',ClientesCRUD.as_view({'get':'listar_clientes'}), name='ver_clientes'),
    path('index/ver_clientes/actualizar_datos/<idcliente>',ClientesCRUD.as_view({'get':'actualizar_datos', 'post':'actualizar_datos'}), name='actualizar_datos_clientes'),


    path('cita_analisis/', citasCRUD.as_view({'get':'cita_analisis'}), name='cita_analisis'),
    path('cita_instalacion/', citasCRUD.as_view({'get':'cita_instalacion'}), name='cita_instalacion'),
    path('cita_mantenimiento/', citasCRUD.as_view({'get':'cita_mantenimiento'}), name='cita_mantenimiento'),
    path('crear_citas/', citasCRUD.as_view({'post':'crear_citas'}), name='crear_citas'),
    path('editar_citas/<int:idcita>/', citasCRUD.as_view({'post': 'editar_citas'}), name='editar_citas'),
    path('eliminar_citas/<int:idcita>/',citasCRUD.as_view({'post':'eliminar_citas'}),name='eliminar_citas'),

    path('ver_cotizaciones/', CotizacionesCRUD.as_view({'get':'listar_cotizaciones'}), name='ver_cotizaciones'),
    path('ver_cotizaciones/enviar_respuesta/<int:idcotizacion>/', correo_respuesta_cotizacion, name='enviar_respuesta'),
    path('ver_cotizaciones/enviar_fechas_disponibles/<int:idcotizacion>/', correo_fechas_disponibles_cita, name='fechas_disponibles'),
    path('editar_cotizaciones/<int:idcotizacion>/', CotizacionesCRUD.as_view({'get': 'editar_cotizacion', 'post': 'editar_cotizacion'}), name='editar_cotizaciones'),
    #path('editar_productos_servicios/<int:idcotizacion>/', CotizacionesCRUD.as_view({'get': 'editar_productos_servicios', 'post': 'editar_productos_servicios'}), name='editar_productos_servicios'),
    path('generar_pdf/<int:idcotizacion>/', generar_pdf, name='generar_pdf'),
    path('crear_cotizaciones/', CotizacionesCRUD.as_view({'post':'crear_cotizaciones'}), name='crear_cotizaciones'),
    path('crear_cotizaciones/productos_servicios/<int:idcotizacion>/', CotizacionesCRUD.as_view({'post':'asignar_productos_servicios', 'get':'asignar_productos_servicios'}), name='asignar_productos_servicios'),

    path('index/tecnicos/ver_tecnicos/registrar_tecnico/', tecnicosCRUD.as_view({'post':'registrar_tecnico'}), name='registrar_tecnico'),
    path('index/tecnicos/ver_tecnicos/editar_especialidad/<idtecnico>', tecnicosCRUD.as_view({'post':'editar_especialidad'}), name='editar_especialidad'),
    path('index/tecnicos/ver_tecnicos/ver_agenda/<idtecnico>', cronogramatecnicosCRUD.as_view({'post':'admin_ver_agenda_tecnico', 'get':'admin_ver_agenda_tecnico'}), name='admin_ver_agenda_tecnico'),
    path('crear_cotizaciones/productos_servicios/<int:idcotizacion>/', CotizacionesCRUD.as_view({'post':'asignar_productos_servicios', 'get':'asignar_productos_servicios'}), name='asignar_productos_servicios'),
    path('eliminar_cotizacion/<int:idcotizacion>/', CotizacionesCRUD.as_view({'post': 'eliminar_cotizacion'}), name='eliminar_cotizacion'),

    #Tecnicos
    path('home_tecnico/', tecnico_home, name='tecnico_home'),
    path('home_tecnico/mi_agenda/', cronogramatecnicosCRUD.as_view({'get': 'citas_eventos_tecnicos'}), name='mi_agenda'),
    path('home_tecnico/mis_actividades/', mis_actividades, name='mis_actividades'),

    #agendas
    path('home_tecnico/mis_citas/',cronogramatecnicosCRUD.as_view({'get': 'citas_tecnico'}), name='mis_citas'),
    path('home_tecnico/mis_citas/cambiar_estado/<int:idcita>',citasCRUD.as_view({'post': 'cambiar_estado_cita'}), name='cambiar_estado_cita')


]
