from django.shortcuts import render, redirect
from rest_framework import viewsets
from Account.models import Clientes, Usuarios
from .serializers import ClientesSerializer
from django.core.paginator import Paginator , EmptyPage , PageNotAnInteger
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist


class ClientesCRUD(viewsets.ModelViewSet):
    queryset = Clientes.objects.all().order_by('numerodocumento')
    serializer_class = ClientesSerializer

    def listar_clientes(self, request):
        clientes_list = self.get_queryset()
        paginator = Paginator(clientes_list, 5)
        page_number = request.GET.get('page', 1)
        try:
            clientes = paginator.page(page_number)
        except PageNotAnInteger:
            clientes = paginator.page(1)
        except EmptyPage:
            clientes = paginator.page(paginator.num_pages)
        return render(request, 'clientes.html', {'clientes': clientes})
    
    def actualizar_datos(self,request, idcliente):
        try:
            cliente = Clientes.objects.get(idcliente=idcliente)
            usuario = Usuarios.objects.get(numerodocumento=cliente.numerodocumento.numerodocumento)
        except ObjectDoesNotExist:
            messages.error(request, 'No se pudo encontrar el cliente.')
            return redirect('ver_clientes')

        if request.method == 'POST':
            try:
                nombre = request.POST.get('nombre')
                apellido = request.POST.get('apellido')
                email = request.POST.get('email')

                usuario.nombre = nombre
                usuario.apellido = apellido
                usuario.email = email
                usuario.save()
                
                messages.success(request, 'Datos actualizados correctamente')
            except Exception as e:
                messages.error(request, f'Ocurrió un error al actualizar los datos: {str(e)}')
        else:
            messages.error(request, 'Ocurrió un error al actualizar los datos')

        return redirect('ver_clientes')

