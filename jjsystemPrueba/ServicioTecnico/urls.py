from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .controllers.actividadesCrogTec import actividadesCrogTecCRUD
from .controllers.citas import citasCRUD
from .controllers.cotizaciones import CotizacionesCRUD, generar_pdf
from .controllers.cronogramatecnicos import cronogramatecnicosCRUD
from .controllers.detallesactividades import detallesactividadesCRUD
from .controllers.disponibilidadcronograma import disponibilidadcronogramaCRUD
from .controllers.estadocotizaciones import estadocotizacionesCRUD
from .controllers.tecnicos import tecnicosCRUD, tecnico_home, mi_agenda, mis_actividades, mis_citas
from .controllers.clientes import ClientesCRUD

#urls back 

router = DefaultRouter()
router.register(r'actividades_cronograma', actividadesCrogTecCRUD)
router.register(r'citas',citasCRUD)
router.register(r'cotizaciones', CotizacionesCRUD)
router.register(r'cronograma_tecnicos', cronogramatecnicosCRUD)
router.register(r'detalles_actividades',detallesactividadesCRUD)
router.register(r'disponibilidad_cronograma', disponibilidadcronogramaCRUD)
router.register(r'estado_cotizaciones',estadocotizacionesCRUD)
router.register(r'tecnicos', tecnicosCRUD)
router.register(r'clientes', ClientesCRUD)


# urls front 
from .views import index, inicio, indexTecnicos

urlpatterns=[
    path('',include(router.urls)),
    path('inicio/', inicio, name = 'inicio'),
    path('index/', index , name='index'),
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
    path('editar_citas/<idcita>/', citasCRUD.as_view({'put': 'editar_citas'}), name='editar_citas'),
    path('eliminar_citas/<int:idcita>/',citasCRUD.as_view({'delete':'eliminar_citas'}),name='eliminar_citas'),

    path('ver_cotizaciones/', CotizacionesCRUD.as_view({'get':'listar_cotizaciones'}), name='ver_cotizaciones'),
    path('editar_cotizaciones/<int:idcotizacion>/', CotizacionesCRUD.as_view({'get': 'editar_cotizacion', 'post': 'editar_cotizacion'}), name='editar_cotizaciones'),
    #path('editar_productos_servicios/<int:idcotizacion>/', CotizacionesCRUD.as_view({'get': 'editar_productos_servicios', 'post': 'editar_productos_servicios'}), name='editar_productos_servicios'),
    path('generar_pdf/<int:idcotizacion>/', generar_pdf, name='generar_pdf'),
    path('crear_cotizaciones/', CotizacionesCRUD.as_view({'post':'crear_cotizaciones'}), name='crear_cotizaciones'),
    path('crear_cotizaciones/productos_servicios/<int:idcotizacion>/', CotizacionesCRUD.as_view({'post':'asignar_productos_servicios', 'get':'asignar_productos_servicios'}), name='asignar_productos_servicios'),

    path('index/tecnicos/ver_tecnicos/registrar_tecnico/', tecnicosCRUD.as_view({'post':'registrar_tecnico'}), name='registrar_tecnico'),
    path('index/tecnicos/ver_tecnicos/editar_especialidad/<idtecnico>', tecnicosCRUD.as_view({'post':'editar_especialidad'}), name='editar_especialidad'),
    path('crear_cotizaciones/productos_servicios/<int:idcotizacion>/', CotizacionesCRUD.as_view({'post':'asignar_productos_servicios', 'get':'asignar_productos_servicios'}), name='asignar_productos_servicios'),
    path('eliminar_cotizacion/<int:idcotizacion>/', CotizacionesCRUD.as_view({'post': 'eliminar_cotizacion'}), name='eliminar_cotizacion'),

    #Tecnicos
    path('home_tecnico/', tecnico_home, name='tecnico_home'),
    path('home_tecnico/mi_agenda/', mi_agenda, name='mi_agenda'),
    path('home_tecnico/mis_citas/', mis_citas, name='mis_citas'),
    path('home_tecnico/mis_actividades/', mis_actividades, name='mis_actividades'),
    path('home_tecnico/mis_datos/', tecnicosCRUD.as_view({'post':'editar_datos_tecnico', 'get':'editar_datos_tecnico'}), name='editar_datos_tecnico')


]
