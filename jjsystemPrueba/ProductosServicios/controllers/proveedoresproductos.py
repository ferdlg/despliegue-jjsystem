from rest_framework import viewsets
from Account.models import Proveedoresproductos
from .serializers import ProveedoresProductosSerializer
from django.shortcuts import redirect, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from Account.models import Proveedoresproductos
from django.contrib import messages
from Account.views import role_required
from django.contrib.auth.decorators import login_required

class proveedoresCRUD(viewsets.ModelViewSet):
    queryset = Proveedoresproductos.objects.all()
    serializer_class = ProveedoresProductosSerializer

@login_required
@role_required(1)
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
@login_required
@role_required(1)
def createProveedorProductoView(request):
    if request.method == 'POST':
        nombreproveedor = request.POST.get('nombreProveedor')
        proveedor = Proveedoresproductos.objects.create(
            nombreproveedor=nombreproveedor
        )
        messages.success(request, 'Proveedor creado correctamente')
        return redirect('proveedorProductos')

    return render(request, "crudAdmin/proveedoresProductos.html")
@login_required
@role_required(1)
def editarProveedorProductoView(request, idproveedorproducto):
    proveedor = Proveedoresproductos.objects.get(idproveedorproducto=idproveedorproducto)
    if request.method == 'POST':
        nombreproveedor = request.POST.get('nombreProveedor')
        proveedor.nombreproveedor = nombreproveedor
        proveedor.save()
        messages.success(request, 'Proveedor modificado correctamente')
        return redirect('proveedorProductos')

    return render(request, "crudAdmin/proveedoresProductos.html", {"proveedor": proveedor})
@login_required
@role_required(1)
def eliminarProveedorProductoView(request, idproveedorproducto):
    proveedor = Proveedoresproductos.objects.get(idproveedorproducto=idproveedorproducto)
    proveedor.delete()
    messages.success(request, 'Proveedor eliminado correctamente')
    return redirect('proveedorProductos')
