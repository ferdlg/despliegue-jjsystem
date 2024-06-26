from django.shortcuts import render, redirect
from Account.models import Pqrsf, Respuestas
from Account.models import Estadospqrsf
from Account.models import Tipospqrsf
from django.core.paginator import Paginator , EmptyPage , PageNotAnInteger
from Account.views import role_required
from django.contrib.auth.decorators import login_required

# Admin
@login_required
@role_required(1)
def home_pqrsf(request):
    # Obtener los tipos de PQRSF para el filtro
    tipos = Tipospqrsf.objects.all()

    # Filtrar las PQRSF si se seleccionó un tipo específico
    tipo_seleccionado = request.GET.get('tipopqrsf', '-1')
    pqrsf_list = Pqrsf.objects.all()
    if tipo_seleccionado and tipo_seleccionado != '-1':
        pqrsf_list = pqrsf_list.filter(idtipopqrsf=tipo_seleccionado)

    respuestas = Respuestas.objects.all()
    paginator = Paginator(pqrsf_list, 5)
    page_number = request.GET.get('page')
    try:
        pqrsf_item = paginator.page(page_number)
    except PageNotAnInteger:
        pqrsf_item = paginator.page(1)
    except EmptyPage:
        pqrsf_item = paginator.page(paginator.num_pages)
    
    return render(request, "admin/pqrsf.html", {"pqrsf": pqrsf_item, 'tipos': tipos, 'respuestas':respuestas})

    
@login_required
@role_required(1)
def indexPqrsf(request):
    return render(request, 'admin/indexPqrsf.html')

@login_required
@role_required(1)
def editarPqrsf(request, idpqrsf):
    pqrsf_item = Pqrsf.objects.get(idpqrsf=idpqrsf)
    estados = Estadospqrsf.objects.all()
    tipos = Tipospqrsf.objects.all()

    if request.method == 'POST':
        #obtener los datos de la petición
        fechapqrsf = request.POST.get('fecha')
        informacionpqrsf = request.POST.get('informacion')
        idestadopqrsf= request.POST.get('estado')
        idtipopqrsf = request.POST.get('tipo')

        #obtener la instancia de EstadosPqrsf
        idestadopqrsf= Estadospqrsf.objects.get(idestadopqrsf=idestadopqrsf)

        #obtener la instancia de TiposPqrsf
        idtipopqrsf = Tipospqrsf.objects.get(idtipopqrsf=idtipopqrsf)

        #actualizar los campos del objeto pqrsf
        pqrsf_item.fechapqrsf = fechapqrsf
        pqrsf_item.informacionpqrsf = informacionpqrsf
        pqrsf_item.idestadopqrsf= idestadopqrsf
        pqrsf_item.idtipopqrsf = idtipopqrsf
        pqrsf_item.save()

        return redirect('indexPqrsf')

    return render(request, "editarPqrsf.html", {"pqrsf": pqrsf_item, "estados": estados, "tipos": tipos})
@login_required
@role_required(1)
def eliminarPqrsf(request, idpqrsf):
    pqrsf = Pqrsf.objects.get(idpqrsf = idpqrsf)
    pqrsf.delete()

    return redirect('indexPqrsf')