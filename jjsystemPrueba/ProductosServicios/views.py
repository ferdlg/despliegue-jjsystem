from django.shortcuts import render, redirect
from Account.models import Productos, Servicios
from Account.models import Categoriasproductos 


# Create your views here.
def landing(request):
    return render(request, 'landing/Index.html')

# mostrar template de servicios
def servicios(request):
    return render(request, 'landing/Servicios.html')

#filtrar productos en la landing
def productos(request):
    categorias = Categoriasproductos.objects.all()
    selected_category = request.GET.get('categoria')
    productos = Productos.objects.all()

    if selected_category == "-1":
        productos
    elif selected_category:
        productos = Productos.objects.filter(idcategoriaproducto=selected_category)

    if not productos:
        if selected_category:
            message = "No hay productos disponibles en esta categoría"
        else:
            message = "No hay productos disponibles"
        return render(request, 'landing/Productos.html', {"message": message, "categorias": categorias})

    return render(request, 'landing/Productos.html', {"productos": productos, "categorias": categorias})

# Filtrar producto por id
def producto(request, id):
    producto = Productos.objects.get(idproducto = id)
    return render(request, 'landing/VisualizaciónProducto.html',{'producto':producto})

def home(request):
    return render(request, "crudAdmin/IndexProductosServicios.html")


def buscar_productos_servicios(request):
    if request.method == 'GET':
        palabra_clave = request.GET.get('palabra_clave')

        productos = Productos.objects.filter(nombreproducto__icontains=palabra_clave)
        servicios = Servicios.objects.filter(nombreservicio__icontains=palabra_clave)

        return render(request, 'landing/resultados_busqueda.html', {'productos': productos, 'servicios': servicios})
    else:
        return render(request, 'landing/index.html')
