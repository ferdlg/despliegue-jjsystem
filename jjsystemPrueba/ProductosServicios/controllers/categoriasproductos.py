from django.shortcuts import redirect, render
from rest_framework import viewsets
from Account.models import Categoriasproductos
from .serializers import CategoriasProductosSerializers
from django.core.paginator import Paginator , EmptyPage , PageNotAnInteger


#definimos la clase 
class categoriaproductosCRUD(viewsets.ModelViewSet):
    # usamos queryset, que traera todos los objetos de la clase
    queryset = Categoriasproductos.objects.all()
    # usamos serializer class para poder ver los objetos que se traen 
    serializer_class = CategoriasProductosSerializers



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


def createCategoriaProductoView(request):
    if request.method == 'POST':
        nombrecategoria = request.POST.get('nombreCategoria')
        # Crear la instancia de producto
        categoria = Categoriasproductos.objects.create(
                nombrecategoria = nombrecategoria
            )
        return redirect('categoriaProductos')

    return render(request, "crudAdmin/categoriasProductos.html", {"categoria": categoria})

def editarCategoriaProductoView(request, idCategoriaProducto):
    categoria = Categoriasproductos.objects.get(idcategoriaproducto=idCategoriaProducto)
    if request.method == 'POST':
        # Obtener los datos de la petición
        nombrecategoria = request.POST.get('nombreCategoria')  # Corregido aquí
        # Actualizar los campos del objeto envio
        categoria.nombrecategoria = nombrecategoria
        categoria.save()

        return redirect('categoriaProductos')

    return render(request, "crudAdmin/categoriasProductos.html", {"categoria": categoria})

def eliminarCategoriaProductoView(request, idCategoriaProducto):
    categoria = Categoriasproductos.objects.get(idcategoriaproducto = idCategoriaProducto)
    categoria.delete()

    return redirect('categoriaProductos')