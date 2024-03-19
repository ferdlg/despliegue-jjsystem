from rest_framework.response import Response
from rest_framework import viewsets, status
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from Account.forms import RegisterForm
from Account.models import Estadosusuarios, Roles, Tecnicos
from .serializers import TecnicosSerializer
from django.core.paginator import Paginator , EmptyPage , PageNotAnInteger
from ServicioTecnico.forms import  RegisterForm, EditTecnicosForm

class tecnicosCRUD(viewsets.ModelViewSet):
    queryset = Tecnicos.objects.all()
    serializer_class = TecnicosSerializer

    @classmethod
    def listar_tecnicos(cls, request):
        tecnicos_list = cls.queryset

        paginator = Paginator(tecnicos_list, 5)  # Mostrar 10 productos por página
        page_number = request.GET.get('page') 
        form = RegisterForm(request.POST)
        edit_form = EditTecnicosForm()
        # Obtener el número de página solicitado
        try:
            tecnico = paginator.page(page_number)
        except PageNotAnInteger:
            tecnico = paginator.page(1)
        except EmptyPage:
            tecnico = paginator.page(paginator.num_pages)
        return render(request, 'vertecnicos.html', {'tecnicos': tecnico,'form': form, 'edit_form': edit_form })
    
    
    def registrar_tecnico(cls, request):
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                # Cifrar la contraseña antes de guardarla
                numerodocumento_str = str(form.cleaned_data['numerodocumento'])  # Convertir a cadena
                user.password = make_password(numerodocumento_str)
                user.idrol = Roles.objects.get(idrol=3)  # Asigna el rol de tecnico
                user.idestadosusuarios = Estadosusuarios.objects.get(idestadousuario=1)  # Asigna el estado de usuario activo
                user.save()

                return redirect('verTecnicos')
        else:
            form = RegisterForm()

        return render(request, 'vertecnicos.html', {'form': form})
    @classmethod
    def editar_tecnico(cls, request, idtecnico):
        tecnico = Tecnicos.objects.get(idtecnico=idtecnico)
        if request.method == 'POST':
            edit_form = EditTecnicosForm(request.POST, instance=tecnico)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('verTecnicos')
        else:
            form = EditTecnicosForm(instance=tecnico)
        
        return render(request, 'verTecnicos.html', {'edit_form': edit_form, 'idtecnico': idtecnico})
    
    def eliminar_tecnico(self, request, idtecnico):
            tecnico = Tecnicos.objects.get(idtecnico=idtecnico)
            tecnico.delete()
            
            # Obtener el número de página actual
            current_page = request.GET.get('page')
            
            # Redireccionar a la página de listar técnicos manteniendo la paginación
            return redirect('verTecnicos')
    #registrar tecnicos
    #actualizar datos de tecnicos
    #eliminar tecnicos
    #que la contraseña inicialmente sea el numero de documento 