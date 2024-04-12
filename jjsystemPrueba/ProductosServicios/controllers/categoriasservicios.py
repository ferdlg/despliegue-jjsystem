from django.shortcuts import redirect, render
from rest_framework import viewsets
from Account.models import Categoriasservicios
from .serializers import CategoriasServiciosSerializers
from django.core.paginator import Paginator , EmptyPage , PageNotAnInteger
from django.contrib import messages
from Account.views import role_required
from django.contrib.auth.decorators import login_required

class categoriaserviciosCRUD(viewsets.ModelViewSet):
    queryset = Categoriasservicios.objects.all()
    serializer_class = CategoriasServiciosSerializers



@login_required
@role_required(1)
#crud categorias servicios 
def home_categoriaServicios(request):
    # Obtener todas las categorías de servicios
    categoria_list = Categoriasservicios.objects.all()

    # Configurar la paginación
    paginator = Paginator(categoria_list, 10)  # Mostrar 10 categorías por página
    page_number = request.GET.get('page')      # Obtener el número de página solicitado
    try:
        categorias = paginator.page(page_number)
    except PageNotAnInteger:
        categorias = paginator.page(1)
    except EmptyPage:
        categorias = paginator.page(paginator.num_pages)

    return render(request, "crudAdmin/categoriasServicios.html", {"categorias": categorias})

@login_required
@role_required(1)
def createCategoriaServicioView(request):
    if request.method == 'POST':
        nombrecategoria = request.POST.get('nombrecategoria')
        # Crear la instancia de categoría de servicio
        categoria = Categoriasservicios.objects.create(
                nombrecategoria = nombrecategoria
            )
        messages.success(request, 'Categoria creada correctamente')
        return redirect('categoriaServicios')

    return render(request, "crudAdmin/categoriasServicios.html")

@login_required
@role_required(1)
def editarCategoriaServicioView(request, idcategoriaservicio):
    categoria = Categoriasservicios.objects.get(idcategoriaservicio=idcategoriaservicio)
    if request.method == 'POST':
        # Obtener los datos de la petición
        nombrecategoria = request.POST.get('nombrecategoria')
        # Actualizar los campos del objeto categoría de servicio
        categoria.nombrecategoria = nombrecategoria
        categoria.save()
        messages.success(request, 'Categoria modificada correctamente')
        return redirect('categoriaServicios')

    return render(request, "crudAdmin/categoriasServicios.html", {"categoria": categoria})

@login_required
@role_required(1)
def eliminarCategoriaServicioView(request, idcategoriaservicio):
    categoria = Categoriasservicios.objects.get(idcategoriaservicio=idcategoriaservicio)
    categoria.delete()

    messages.success(request, 'Categoria eliminada correctamente')
    return redirect('categoriaServicios')