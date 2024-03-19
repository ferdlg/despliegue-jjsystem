from django.shortcuts import redirect, render
from rest_framework import viewsets
from Account.models import *
from .serializers import ProductosSerializer
from django.core.paginator import Paginator , EmptyPage , PageNotAnInteger

'''
    Importamos la biblioteca viewsets 
    de Django Rest Framework la cual nos proporciona las
    operaciones de un crud 
'''

# Definimos la clase 
class productosCRUD(viewsets.ModelViewSet):
    # Usamos queryset, que traerá todos los objetos de la clase
    queryset = Productos.objects.all()
    # Usamos serializer class para poder ver los objetos que se traen 
    serializer_class = ProductosSerializer

# Productos en dashboard admin
def home_productos(request):
    # Obtener todos los productos
    productos_list = Productos.objects.all()

    # Configurar la paginación
    paginator = Paginator(productos_list, 5)  # Mostrar 10 productos por página
    page_number = request.GET.get('page')      # Obtener el número de página solicitado
    try:
        productos_list = paginator.page(page_number)
    except PageNotAnInteger:
        productos_list = paginator.page(1)
    except EmptyPage:
        productos_list = paginator.page(paginator.num_pages)

    return render(request, "crudAdmin/IndexProductos.html", {"productos": productos_list})

# CRUD de productos
import os
from django.conf import settings

def createProductoView(request):
    if request.method == 'POST':
        nombreproducto = request.POST.get('nombre')
        descripcionproducto = request.POST.get('descripcion')
        precioproducto = request.POST.get('precio')
        cantidad = request.POST.get('cantidad')
        idcategoriaproducto = request.POST.get('categoria')
        idproveedorproducto = request.POST.get('proveedor')
        imagen = request.FILES.get('imagen')

        categoria = Categoriasproductos.objects.get(idcategoriaproducto=idcategoriaproducto)
        proveedor = Proveedoresproductos.objects.get(idproveedorproducto=idproveedorproducto)

        if imagen:
            # Ruta de destino para guardar la imagen en la carpeta "productos" dentro de "static"
            ruta_imagen = os.path.join(settings.STATIC_ROOT, 'productos', imagen.name)
            with open(ruta_imagen, 'wb+') as destination:
                for chunk in imagen.chunks():
                    destination.write(chunk)

        producto = Productos.objects.create(
            nombreproducto=nombreproducto,
            descripcionproducto=descripcionproducto,
            precioproducto=precioproducto,
            cantidad=cantidad,
            idcategoriaproducto=categoria,
            idproveedorproducto=proveedor,
            imagen=ruta_imagen
        )

        return redirect('homeProductos')

    categorias = Categoriasproductos.objects.all()
    proveedores = Proveedoresproductos.objects.all()
    return render(request, "crudAdmin/CreateProducto.html", {"categorias": categorias, "proveedores": proveedores})

def editarProducto(request, idProducto):
    producto = Productos.objects.get(idproducto=idProducto)
    categorias = Categoriasproductos.objects.all()
    proveedores = Proveedoresproductos.objects.all()

    if request.method == 'POST':
        # Obtener los datos de la petición
        nombreproducto = request.POST.get('nombre')
        descripcionproducto = request.POST.get('descripcion')
        precioproducto = request.POST.get('precio')
        cantidad = request.POST.get('cantidad')
        idcategoriaproducto = request.POST.get('categoria')
        idproveedorproducto = request.POST.get('proveedor')
        foto = request.FILES.get('imagen')

        # Obtener la instancia de categorías
        categoria = Categoriasproductos.objects.get(idcategoriaproducto=idcategoriaproducto)

        # Obtener la instancia de proveedor
        proveedor = Proveedoresproductos.objects.get(idproveedorproducto=idproveedorproducto)

        # Actualizar los campos del objeto producto
        producto.nombreproducto = nombreproducto
        producto.descripcionproducto = descripcionproducto
        producto.precioproducto = precioproducto
        producto.cantidad = cantidad
        producto.idcategoriaproducto = categoria
        producto.idproveedorproducto = proveedor
        producto.imagen = foto
        producto.save()

        return redirect('homeProductos')

    return render(request, "crudAdmin/EditarProducto.html", {"producto": producto, "categorias": categorias, "proveedores": proveedores})

def eliminarProducto(request, idProducto):
    producto = Productos.objects.get(idproducto=idProducto)
    producto.delete()

    return redirect('homeProductos')
