from django.shortcuts import redirect, render
from rest_framework import viewsets
from Account.models import Categoriasproductos, Categoriasservicios, Servicios
from .serializers import ServiciosSerializer
from django.core.paginator import Paginator , EmptyPage , PageNotAnInteger
from django.contrib import messages
from Account.views import role_required
from django.contrib.auth.decorators import login_required

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

@login_required
@role_required(1)
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

@login_required
@role_required(1)
#crud en el front
def createServiciosView(request):
    try:
        if request.method == 'POST':
            nombreservicio = request.POST.get('nombre')
            descripcionservicio = request.POST.get('descripcion')
            idcategoriaservicio = request.POST.get('categoria')
    
            # Obtener la instancia de categorias
            categoria = Categoriasservicios.objects.get(idcategoriaservicio=idcategoriaservicio)

            # Crear la instancia de producto
            servicio = Servicios.objects.create(
                    nombreservicio=nombreservicio,
                    descripcionservicio=descripcionservicio,
                    idcategoriaservicio=categoria
                )
            messages.success(request, 'Servicio creado correctamente')

            return redirect('homeServicios')
        categorias = Categoriasservicios.objects.all()
        return render(request, "crudAdmin/CreateServicio.html", {"categorias": categorias})
    
    except Categoriasservicios.DoesNotExist:
        messages.error(request, 'La categoría seleccionada no existe')
        return redirect('homeServicios')
    except Exception as e:
        messages.error(request, f'Error al crear el servicio: {str(e)}')
        return redirect('homeServicios')

@login_required
@role_required(1)
def editarServicio(request, idServicio):
    try:
        servicio = Servicios.objects.get(idservicio=idServicio)
        categorias = Categoriasservicios.objects.all()

        if request.method == 'POST':
            # Obtener los datos de la petición
            nombreservicio = request.POST.get('nombre')
            descripcionservicio = request.POST.get('descripcion')
            idcategoriaservicio = request.POST.get('categoria')

            # Obtener la instancia de categorias
            categoria = Categoriasservicios.objects.get(idcategoriaservicio=idcategoriaservicio)

            # Actualizar los campos del objeto envio
            servicio.nombreproducto = nombreservicio
            servicio.descripcionproducto = descripcionservicio
            servicio.idcategoriaproducto = categoria
            servicio.save()

            messages.success(request, 'Servicio modificado correctamente')
            return redirect('homeServicios')

        return render(request, "crudAdmin/EditarServicio.html", {"servicio": servicio, "categorias": categorias})
    
    except Servicios.DoesNotExist:
        messages.error(request, 'El servicio seleccionado no existe')
        return redirect('homeServicios')
    except Categoriasservicios.DoesNotExist:
        messages.error(request, 'La categoría seleccionada no existe')
        return redirect('homeServicios')
    except Exception as e:
        messages.error(request, f'Error al editar el servicio: {str(e)}')
        return redirect('homeServicios')

@login_required
@role_required(1)
def eliminarServicio(request, idServicio):
    try:
        servicio = Servicios.objects.get(idservicio=idServicio)
        servicio.delete()
        messages.success(request, 'Servicio eliminado correctamente')
    except:
        messages.error(request, 'El servicio que intenta eliminar  esta asociado a citas u otras actividades.')
    return redirect('homeServicios')
