from rest_framework import viewsets
from Account.models import Proveedoresproductos
from .serializers import ProveedoresProductosSerializer
from django.shortcuts import redirect, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from Account.models import Proveedoresproductos


class proveedoresCRUD(viewsets.ModelViewSet):
    queryset = Proveedoresproductos.objects.all()
    serializer_class = ProveedoresProductosSerializer

def home_proveedorProductos(request):
    proveedores_list = Proveedoresproductos.objects.all()

    paginator = Paginator(proveedores_list, 20)
    page_number = request.GET.get('page')
    try:
        proveedores = paginator.page(page_number)
    except PageNotAnInteger:
        proveedores = paginator.page(1)
    except EmptyPage:
        proveedores = paginator.page(paginator.num_pages)

    return render(request, "crudAdmin/proveedoresProductos.html", {"proveedores": proveedores})

def createProveedorProductoView(request):
    if request.method == 'POST':
        nombreproveedor = request.POST.get('nombreProveedor')
        proveedor = Proveedoresproductos.objects.create(
            nombreproveedor=nombreproveedor
        )
        return redirect('proveedorProductos')

    return render(request, "crudAdmin/proveedoresProductos.html")

def editarProveedorProductoView(request, idProveedorProducto):
    proveedor = Proveedoresproductos.objects.get(idproveedorproducto=idProveedorProducto)
    if request.method == 'POST':
        nombreproveedor = request.POST.get('nombreProveedor')
        proveedor.nombreproveedor = nombreproveedor
        proveedor.save()
        return redirect('proveedorProductos')

    return render(request, "crudAdmin/proveedoresProductos.html", {"proveedor": proveedor})

def eliminarProveedorProductoView(request, idProveedorProducto):
    proveedor = Proveedoresproductos.objects.get(idproveedorproducto=idProveedorProducto)
    proveedor.delete()
    return redirect('proveedorProductos')
