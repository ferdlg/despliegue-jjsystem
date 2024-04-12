from django.shortcuts import redirect, render
from rest_framework import viewsets
from Account.models import Categoriasproductos
from .serializers import CategoriasProductosSerializers
from django.core.paginator import Paginator , EmptyPage , PageNotAnInteger
from django.contrib import messages
from Account.views import role_required
from django.contrib.auth.decorators import login_required
#definimos la clase 
class categoriaproductosCRUD(viewsets.ModelViewSet):
    # usamos queryset, que traera todos los objetos de la clase
    queryset = Categoriasproductos.objects.all()
    # usamos serializer class para poder ver los objetos que se traen 
    serializer_class = CategoriasProductosSerializers


@login_required
@role_required(1)
def home_categoriaProductos(request):
    # Obtener todos los productos
    categoria_list = Categoriasproductos.objects.all()

    # Configurar la paginación
    paginator = Paginator(categoria_list, 10)  # Mostrar 10 productos por página
    page_number = request.GET.get('page')      # Obtener el número de página solicitado
    try:
        categorias = paginator.page(page_number)
    except PageNotAnInteger:
        categorias = paginator.page(1)
    except EmptyPage:
        categorias = paginator.page(paginator.num_pages)

    return render(request, "crudAdmin/categoriasProductos.html", {"categorias": categorias})

@login_required
@role_required(1)
def createCategoriaProductoView(request):
    if request.method == 'POST':
        nombrecategoria = request.POST.get('nombrecategoria')
        # Crear la instancia de producto
        categoria = Categoriasproductos.objects.create(
                nombrecategoria = nombrecategoria
            )
        messages.success(request, 'Categoria creada correctamente')
        return redirect('categoriaProductos')

    return render(request, "crudAdmin/categoriasProductos.html", {"categoria": categoria})
@login_required
@role_required(1)
def editarCategoriaProductoView(request, idcategoriaproducto):
    categoria = Categoriasproductos.objects.get(idcategoriaproducto=idcategoriaproducto)
    if request.method == 'POST':
        # Obtener los datos de la petición
        nombrecategoria = request.POST.get('nombrecategoria')  # Corregido aquí
        # Actualizar los campos del objeto envio
        categoria.nombrecategoria = nombrecategoria
        categoria.save()

        messages.success(request, 'Categoria modificada correctamente')
        return redirect('categoriaProductos')

    return render(request, "crudAdmin/categoriasProductos.html", {"categoria": categoria})
@login_required
@role_required(1)
def eliminarCategoriaProductoView(request, idcategoriaproducto):
    categoria = Categoriasproductos.objects.get(idcategoriaproducto = idcategoriaproducto)
    categoria.delete()
    messages.success(request, 'Categoria eliminada correctamente')
    return redirect('categoriaProductos')