from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

from .controllers.categoriasproductos import categoriaproductosCRUD , home_categoriaProductos , createCategoriaProductoView , editarCategoriaProductoView, eliminarCategoriaProductoView
from .controllers.categoriasservicios import categoriaserviciosCRUD , home_categoriaServicios, createCategoriaServicioView, editarCategoriaServicioView, eliminarCategoriaServicioView
from .controllers.clientes import clientesCRUD
from .controllers.permisos import permisosCRUD
from .controllers.productos import productosCRUD , home_productos , createProductoView, editarProducto, eliminarProducto
from .controllers.ventas import ventasCRUD, home_ventas,createVenta, editVenta, deleteVenta
from .controllers.proveedoresproductos import proveedoresCRUD, home_proveedorProductos, createProveedorProductoView, editarProveedorProductoView, eliminarProveedorProductoView
from .controllers.rol_has_permisos import rol_has_permisosCRUD
from .controllers.roles import rolesCRUD
from .controllers.servicios import serviciosCRUD, servicios, servicios_landing, home_servicios, createServiciosView, editarServicio, eliminarServicio
from .controllers.cotizaciones import CotizacionesCRUD, obtener_detalles_cotizacion, vista_detalle_cotizacion
from .correos import correo_confirmacion_compra

router = DefaultRouter()
router.register(r'categoriasproductos', categoriaproductosCRUD)
router.register(r'categoriasservicios', categoriaserviciosCRUD)
router.register(r'clientes', clientesCRUD)
router.register(r'permisos', permisosCRUD)
router.register(r'productos', productosCRUD)
router.register(r'proveedoresproductos', proveedoresCRUD)
router.register(r'rol_has_permisos', rol_has_permisosCRUD)
router.register(r'roles', rolesCRUD)
router.register(r'servicios', serviciosCRUD)
router.register(r'ventas', ventasCRUD)


urlpatterns=[
    path('', views.home, name='home'),
    path('productos',home_productos, name='homeProductos'),
    path('ventas', home_ventas, name='homeVentas' ),
    path('ventas/createVenta', createVenta, name='createVenta' ),
    path('editVenta/<int:idVenta>/', editVenta, name='editarVenta' ),
    path('deleteVenta/<int:idVenta>/', deleteVenta, name='deleteVenta' ),
    path('serviciosLanding/<int:categoria>/',servicios_landing, name='serviciosLanding'),
    path('buscar/', views.buscar_productos_servicios, name='buscar'),
    path('verProducto/<id>/', views.producto, name='verProducto'),
    path('api/', include(router.urls)),

    path('proveedores/',home_proveedorProductos, name='proveedorProductos'),
    path('crearProveedor/',createProveedorProductoView, name='crearProveedor'),
    path('editarProveedor/<int:idproveedorproducto>',editarProveedorProductoView, name='editarProveedor'),
    path('elimiarProveedor/<int:idproveedorproducto>',eliminarProveedorProductoView, name='eliminarProveedor'),

    path('createProducto/',createProductoView, name='createProducto'),
    path('editarProducto/<idproducto>',editarProducto, name='editarProducto'),
    path('eliminarProducto/<idproducto>',eliminarProducto, name='eliminarProducto'),

    path('categoriaProducto/', home_categoriaProductos, name='categoriaProductos'),
    path('crearCategoriaProducto/', createCategoriaProductoView, name = 'createCategoriaProducto'),
    path('editarCategoriaProducto/<idcategoriaproducto>', editarCategoriaProductoView, name='editarCategoriaProducto'),
    path('eliminarCategoriaProducto/<idcategoriaproducto>', eliminarCategoriaProductoView, name = 'eliminarCategoriaProducto'),

    path('servicios/', home_servicios, name='homeServicios'),
    path('createServicio/', createServiciosView, name='createServicio'),
    path('editarServicio/<idservicio>', editarServicio, name='editarServicio'),
    path('eliminarServicio/<idservicio>', eliminarServicio, name='eliminarServicio'),

    path('categoriaServicio/', home_categoriaServicios, name = 'categoriaServicios'),
    path('createCategoriaServicio/', createCategoriaServicioView, name="createCategoriaServicio"),
    path('editarCategoriaServicio/<idcategoriaservicio>', editarCategoriaServicioView, name='editarCategoriaServicio'),
    path('eliminarCategoriaServicio/<idcategoriaservicio>', eliminarCategoriaServicioView, name = 'eliminarCategoriaServicio'),

    path('cotizaciones/', CotizacionesCRUD.as_view({'get': 'ir_a_cotizaciones'}), name='ir_a_cotizaciones'),
    path('cotizaciones/crear_cotizacion/', CotizacionesCRUD.as_view({'post': 'crear_cotizacion', 'get': 'crear_cotizacion'}), name='crear_cotizacion'),
    path('cotizaciones/asignar_productos_servicios/<id_cotizacion>/', CotizacionesCRUD.as_view({'post': 'asignar_productos_servicios_cliente', 'get': 'asignar_productos_servicios_cliente'}), name='asignar_productos_servicios_cliente'),
    path('cotizaciones/ver_cotizacion_cliente/<id_cotizacion>/',vista_detalle_cotizacion, name='ver_cotizacion_cliente'),

    path('mis_compras/historial/',ventasCRUD.as_view({'get':'historial_compras'}), name='historial_compras'),
    path('mi_perfil/', clientesCRUD.as_view({'get':'actualizar_mis_datos','post':'actualizar_mis_datos'}), name='actualizar_mis_datos'),
    path('mi_perfil/cliente/ver_perfil/', clientesCRUD.as_view({'get':'actualizar_mis_datos','post':'actualizar_mis_datos'}), name='cliente/ver_perfil'),
    path('mi_perfil/validar_password/',clientesCRUD.as_view({'post':'validar_contrasena'}), name = 'validar_password'),
    path('mi_perfil/validar_password/cambiar_password', clientesCRUD.as_view({'post':'cambiar_contrasena'}), name='cambiar_password'),
    path('confirmacion_compra/<int:idcotizacion>', correo_confirmacion_compra, name='confirmacion_compra')
]