from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

from .controllers.estadospqrsf import estadospqrsfCRUD
from .controllers.tipospqrsf import tipospqrsfCRUD
from .controllers.pqrsf import pqrsfCRUD, convertir_pqrsf_pdf
from .controllers.respuesta import respuestaCRUD

router = DefaultRouter()
router.register(r'Estadospqrsf', estadospqrsfCRUD)
router.register(r'Tipospqrsf', tipospqrsfCRUD)
router.register(r'Pqrsf', pqrsfCRUD)
router.register(r'respuesta', respuestaCRUD)


urlpatterns=[
    path('',include(router.urls)),
    path('editarPqrsf/<int:idPqrsf>', views.editarPqrsf, name='editarPqrsf'),
    path('indexPqrsf/', views.indexPqrsf, name='indexPqrsf'),
    path('indexPqrsf/pqrsf', views.home_pqrsf, name='homePqrsf'),
    path('indexPqrsf/pqrsf/pdf/<int:idpqrsf>', convertir_pqrsf_pdf,  name='convertir_pqrsf_pdf'),

#cliente
    path('pqrsf/ver_pqrsf', pqrsfCRUD.as_view({'get': 'ir_a_pqrsf'}),  name='ir_a_pqrsf'),
    path('crear_pqrsf/',pqrsfCRUD.as_view({'post': 'crear_pqrsf', 'get':'crear_pqrsf'}) , name='crear_pqrsf'),
    path('eliminarPqrsf/<idPqrsf>', views.eliminarPqrsf, name='eliminarPqrsf'),

    path('respuesta/<id_pqrsf>', respuestaCRUD.as_view({'post':'crear_respuesta', 'get':'crear_respuesta'}), name='crear_respuesta')
]