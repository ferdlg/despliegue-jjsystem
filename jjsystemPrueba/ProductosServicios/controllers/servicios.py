from django.shortcuts import redirect, render
from rest_framework import viewsets
from Account.models import Categoriasproductos, Categoriasservicios, Servicios
from .serializers import ServiciosSerializer
from django.core.paginator import Paginator , EmptyPage , PageNotAnInteger


class serviciosCRUD(viewsets.ModelViewSet):
    queryset = Servicios.objects.all()
    serializer_class = ServiciosSerializer


# mostrar template de servicios
def servicios(request):
    return render(request, 'landing/Servicios.html')

# servicios filtrados en la landing 
def servicios_landing(request, categoria):
    servicios = Servicios.objects.filter(idcategoriaservicio=categoria)
    return render(request, 'landing/ServiciosCategorias.html', {'servicios': servicios})

# Servicios en dashboard admin
def home_servicios(request):
    # Obtener todos los productos
    servicios_list = Servicios.objects.all()

    # Configurar la paginación
    paginator = Paginator(servicios_list, 5)  # Mostrar 10 productos por página
    page_number = request.GET.get('page')      # Obtener el número de página solicitado
    try:
        servicios = paginator.page(page_number)
    except PageNotAnInteger:
        servicios = paginator.page(1)
    except EmptyPage:
        servicios = paginator.page(paginator.num_pages)

    return render(request, "crudAdmin/IndexServicios.html", {"servicios": servicios})


#crud en el front
def createServiciosView(request):
    if request.method == 'POST':
        nombreservicio = request.POST.get('nombre')
        descripcionservicio = request.POST.get('descripcion')
        idcategoriaservicio = request.POST.get('categoria')
            
        # Obtener la instancia de categorias
        categoria = Categoriasservicios.objects.get(idcategoriaservicio=idcategoriaservicio)

        # Crear la instancia de producto
        servicio = Servicios.objects.create(
                nombreservicio = nombreservicio,
                descripcionservicio = descripcionservicio,
                idcategoriaservicio = categoria
            )
        return redirect('homeServicios')

    categorias = Categoriasservicios.objects.all()
    return render(request, "crudAdmin/CreateServicio.html", {"categorias": categorias})

def editarServicio(request, idServicio):
    servicio = Servicios.objects.get(idservicio=idServicio)
    categorias = Categoriasservicios.objects.all()

    if request.method == 'POST':
        # Obtener los datos de la petición
        nombreservicio = request.POST.get('nombre')
        descripcionservicio = request.POST.get('descripcion')
        idcategoriaservicio = request.POST.get('categoria')

        # Obtener la instancia de categorias
        categoria = Categoriasproductos.objects.get(idcategoriservicio=idcategoriaservicio)

        # Actualizar los campos del objeto envio
        servicio.nombreproducto = nombreservicio
        servicio.descripcionproducto = descripcionservicio
        servicio.idcategoriaproducto = categoria
        servicio.save()

        return redirect('homeServicios')

    return render(request, "crudAdmin/EditarServicio.html", {"servicio": servicio, "categorias": categorias})

def eliminarServicio(request, idServicio):
    servicio = Servicios.objects.get(idservicio = idServicio)
    servicio.delete()

    return redirect('homeServicios')
