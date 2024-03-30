from rest_framework.response import Response
from rest_framework import viewsets, status
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from Account.forms import RegisterForm
from Account.models import Estadosusuarios, Roles, Tecnicos, Especialidadtecnicos, Usuarios
from .serializers import TecnicosSerializer
from django.core.paginator import Paginator , EmptyPage , PageNotAnInteger
from ServicioTecnico.forms import  RegisterForm, EditTecnicosForm
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

class tecnicosCRUD(viewsets.ModelViewSet):
    queryset = Tecnicos.objects.all()
    serializer_class = TecnicosSerializer

    @classmethod
    def listar_tecnicos(cls, request):
        tecnicos_list = cls.queryset

        paginator = Paginator(tecnicos_list, 5)  
        page_number = request.GET.get('page') 
        form = RegisterForm(request.POST)
        edit_form = EditTecnicosForm()
        try:
            tecnico = paginator.page(page_number)
        except PageNotAnInteger:
            tecnico = paginator.page(1)
        except EmptyPage:
            tecnico = paginator.page(paginator.num_pages)
        return render(request, 'vertecnicos.html', {'tecnicos': tecnico,'form': form, 'edit_form': edit_form })
    
    @classmethod
    def registrar_tecnico(cls, request):
        try:
            if request.method == 'POST':
                form = RegisterForm(request.POST)
                if form.is_valid():
                    user = form.save(commit=False)
                    numerodocumento_str = str(form.cleaned_data['numerodocumento'])
                    user.password = make_password(numerodocumento_str)
                    user.idrol = Roles.objects.get(idrol=3)
                    user.idestadosusuarios = Estadosusuarios.objects.get(idestadousuario=1)
                    user.save()

                    messages.success(request, 'Técnico registrado correctamente')
                    return redirect('verTecnicos')
            else:
                form = RegisterForm()

            return render(request, 'vertecnicos.html', {'form': form})
        except Exception as e:
            messages.error(request, f'Ocurrió un error al intentar registrar el tecnico: {str(e)}')
            return redirect('verTecnicos')
        
    @classmethod
    def editar_especialidad(cls, request, idtecnico):
        try:
            tecnico = Tecnicos.objects.get(idtecnico=idtecnico)
        except ObjectDoesNotExist:
            messages.error(request, 'El técnico especificado no existe.')
            return redirect('verTecnicos')

        if request.method == 'POST':
            edit_form = EditTecnicosForm(request.POST, instance=tecnico)
            if edit_form.is_valid():
                edit_form.save()
                messages.success(request, 'Especialidad editada correctamente')
                return redirect('verTecnicos')
            else:
                messages.error(request, 'El formulario de edición no es válido. Por favor, corrija los errores.')
        else:
            form = EditTecnicosForm(instance=tecnico)
        
        return render(request, 'verTecnicos.html', {'edit_form': edit_form, 'tecnico':tecnico, 'idtecnico': idtecnico})
    
    @classmethod
    def editar_datos_tecnico(cls, request, idtecnico):
        try:
            tecnico = Tecnicos.objects.get(idtecnico=idtecnico)
            usuario = Usuarios.objects.get(numerodocumento=tecnico.numerodocumento.numerodocumento)
        except ObjectDoesNotExist:
            messages.error(request, 'No se pudo encontrar el técnico o el usuario asociado.')
            return redirect('verTecnicos')

        if request.method == 'POST':
            try:
                nombre = request.POST.get('nombre')
                apellido = request.POST.get('apellido')
                email = request.POST.get('email')

                usuario.nombre = nombre
                usuario.apellido = apellido
                usuario.email = email
                usuario.save()
                messages.success(request, 'Datos del técnico actualizados correctamente')
                return redirect('verTecnicos')
            except Exception as e:
                messages.error(request, f'Ocurrió un error al actualizar los datos del técnico: {str(e)}')
                return redirect('verTecnicos')
        else:
            return render(request, 'verTecnicos.html', {'tecnico': tecnico, 'idtecnico': idtecnico})
    @classmethod
    def eliminar_tecnico(self, request, idtecnico):
        try:
            tecnico = Tecnicos.objects.get(idtecnico=idtecnico)
            tecnico.delete()
            messages.success(request, 'Técnico eliminado correctamente')
        except ObjectDoesNotExist:
            messages.error(request, 'No se pudo encontrar el técnico a eliminar.')
        except Exception as e:
            messages.error(request, f'Ocurrió un error al eliminar el técnico: {str(e)}')
            
        current_page = request.GET.get('page')
        return redirect('verTecnicos')

#dashboards de los tecnicos 
def tecnico_home(request):
    return render(request, 'Tecnicos/home.html')
def mi_agenda(request):
    return render(request, 'Tecnicos/mi_agenda.html')
def mis_citas(request):
    return render(request, 'Tecnicos/mis_citas.html')
def mis_actividades(request):
    return render(request, 'Tecnicos/mis_actividades.html')