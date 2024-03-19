from django.shortcuts import render, redirect
from rest_framework import viewsets
from Account.models import Clientes, Usuarios
from .serializers import ClientesSerializer
from django.core.paginator import Paginator , EmptyPage , PageNotAnInteger



class ClientesCRUD(viewsets.ModelViewSet):
    queryset = Clientes.objects.all()
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
    
    def actualizar_datos(self, request, idcliente):
        cliente = Clientes.objects.get(idcliente = idcliente)
        usuario = Usuarios.objects.get(numerodocumento = cliente.numerodocumento.numerodocumento)

        if request.method == 'POST':
            nombre = request.POST.get('nombre')
            apellido = request.POST.get('apellido')
            email = request.POST.get('email')

        # Actualizar los datos del cliente
            usuario.nombre = nombre
            usuario.apellido = apellido
            usuario.email = email
            usuario.save()
            
            return redirect('ver_clientes')

        return redirect('ver_clientes')

