
from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.contrib.staticfiles.urls import static 
from ProductosServicios.views import landing, servicios, productos


urlpatterns = [
    path('', landing, name = 'landing'),
    path('admin/', admin.site.urls),
    path('account/', include('Account.urls')),
    path('productos_servicios/', include('ProductosServicios.urls')),
    path('servicio_tecnico/', include('ServicioTecnico.urls')),
    path('envios/', include('Envios.urls')),
    path('pqrsf/', include('Pqrsf.urls')),
    path('servicios/', servicios, name ='servicios'),
    path('productos/', productos, name='productos')
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

