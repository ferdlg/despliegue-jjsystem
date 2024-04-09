import os
from django.conf import settings
from django.shortcuts import redirect, render
from rest_framework import viewsets
from Account.models import *
from .serializers import ProductosSerializer
from django.core.paginator import Paginator , EmptyPage , PageNotAnInteger
from django.contrib import messages
from django.core.files.base import ContentFile
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile


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
    productos_list = Productos.objects.all().order_by('-idproducto')

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
    
def createProductoView(request):
    if request.method == 'POST':
        # Recuperar datos del formulario
        nombreproducto = request.POST.get('nombre')
        descripcionproducto = request.POST.get('descripcion')
        precioproducto = request.POST.get('precio')
        cantidad = request.POST.get('cantidad')
        idcategoriaproducto = request.POST.get('categoria')
        idproveedorproducto = request.POST.get('proveedor')

        imagen = request.FILES.get('imagen')  # Obtener el archivo de imagen

        try:
            categoria = Categoriasproductos.objects.get(idcategoriaproducto=idcategoriaproducto)
            proveedor = Proveedoresproductos.objects.get(idproveedorproducto=idproveedorproducto)

            if imagen:
                # Guardar la imagen en la carpeta de medios
                nombre_imagen = imagen.name
                path_imagen = os.path.join(settings.MEDIA_ROOT[2], 'static','images', 'productos', nombre_imagen)
                with open(path_imagen, 'wb+') as file:
                    for chunk in imagen.chunks():
                        file.write(chunk)

                # Crear el objeto Productos con la ruta de la imagen
                producto = Productos.objects.create(
                    nombreproducto=nombreproducto,
                    descripcionproducto=descripcionproducto,
                    precioproducto=precioproducto,
                    cantidad=cantidad,
                    idcategoriaproducto=categoria,
                    idproveedorproducto=proveedor,
                    imagen=os.path.join('productos', nombre_imagen)  # Guarda la ruta relativa de la imagen
                )

                messages.success(request, 'Producto creado correctamente')
                return redirect('homeProductos')
            else:
                messages.error(request, 'No se proporcionó ninguna imagen')

        except Categoriasproductos.DoesNotExist:
            messages.error(request, 'La categoría seleccionada no existe')
        except Proveedoresproductos.DoesNotExist:
            messages.error(request, 'El proveedor seleccionado no existe')
        except Exception as e:
            messages.error(request, f'Error al crear el producto: {str(e)}')

    categorias = Categoriasproductos.objects.all()
    proveedores = Proveedoresproductos.objects.all()
    return render(request, "crudAdmin/CreateProducto.html", {"categorias": categorias, "proveedores": proveedores})

def editarProducto(request, idproducto):
    try:
        producto = Productos.objects.get(idproducto=idproducto)
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
            imagen = request.FILES.get('imagen')

            categoria = Categoriasproductos.objects.get(idcategoriaproducto=idcategoriaproducto)
            proveedor = Proveedoresproductos.objects.get(idproveedorproducto=idproveedorproducto)

            if imagen:
                # Guardar la nueva imagen en la carpeta de medios
                nombre_imagen = imagen.name
                path_imagen = os.path.join(settings.MEDIA_ROOT[2], 'static', 'images', 'productos', nombre_imagen)
                with open(path_imagen, 'wb+') as file:
                    for chunk in imagen.chunks():
                        file.write(chunk)
                # Actualizar la imagen del producto
                producto.imagen = os.path.join('productos', nombre_imagen)

            # Obtener la instancia de categoría
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
            producto.save()

            messages.success(request, 'Producto modificado correctamente')
            return redirect('homeProductos')

        return render(request, "crudAdmin/EditarProducto.html", {"producto": producto, "categorias": categorias, "proveedores": proveedores})
    
    except Productos.DoesNotExist:
        messages.error(request, 'El producto especificado no existe')
        return redirect('homeProductos')
    except Categoriasproductos.DoesNotExist:
        messages.error(request, 'La categoría seleccionada no existe')
        return redirect('homeProductos')
    except Proveedoresproductos.DoesNotExist:
        messages.error(request, 'El proveedor seleccionado no existe')
        return redirect('homeProductos')
    except Exception as e:
        messages.error(request, f'Error al editar el producto: {str(e)}')
        return redirect('homeProductos')

def eliminarProducto(request, idproducto):
    producto = Productos.objects.get(idproducto=idproducto)
    producto.delete()
    messages.success(request, 'Producto eliminado correctamente')
    return redirect('homeProductos')
