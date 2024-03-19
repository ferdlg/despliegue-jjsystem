from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

from .controllers.estadospqrsf import estadospqrsfCRUD
from .controllers.tipospqrsf import tipospqrsfCRUD
from .controllers.pqrsf import pqrsfCRUD

router = DefaultRouter()
router.register(r'Estadospqrsf', estadospqrsfCRUD)
router.register(r'Tipospqrsf', tipospqrsfCRUD)
router.register(r'Pqrsf', pqrsfCRUD)

urlpatterns=[
    path('',include(router.urls)),
    path('editarPqrsf/<int:idPqrsf>', views.editarPqrsf, name='editarPqrsf'),
    path('indexPqrsf/', views.indexPqrsf, name='indexPqrsf'),
    path('indexPqrsf/pqrsf', views.home_pqrsf, name='homePqrsf'),
    path('createPqrsf/', views.createPqrsfView, name='createPqrsf'),
    path('eliminarPqrsf/<idPqrsf>', views.eliminarPqrsf, name='eliminarPqrsf'),

    # path('crear_pqrsf/',)
]