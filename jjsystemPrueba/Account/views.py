import base64
from django.utils.encoding import force_bytes
from django.shortcuts import render, HttpResponse
from django.views import View
from .forms import LoginForm, NewPasswordForm, RegisterForm
from .models import Roles, Estadosusuarios, Usuarios
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.contrib.auth import login , logout 
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password, check_password
from django.utils.encoding import force_bytes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

def registerView(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Cifrar la contraseña antes de guardarla
            user.password = make_password(form.cleaned_data['password'])
            user.idrol = Roles.objects.get(idrol=2)  # Asigna el rol de cliente
            user.idestadosusuarios = Estadosusuarios.objects.get(idestadousuario=1)  # Asigna el estado de usuario activo
            user.save()
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

def userLogin(request):
    if request.user.is_authenticated:
        # Si el usuario ya está autenticado, redirige según su rol
        if request.user.idrol.idrol == 1:
            return redirect('inicio')
        elif request.user.idrol.idrol == 2:
            return redirect('productos')
        elif request.user.idrol.idrol == 3:
            return redirect('homeTecnicosEnvios')
        else:
            return redirect('Ingrese con un rol valido')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # Buscar el usuario por email en la base de datos
            try:
                user = Usuarios.objects.get(email=email)
            except Usuarios.DoesNotExist:
                user = None

            # Si se encontró el usuario y la contraseña coincide, iniciar sesión
            if user is not None and check_password(password, user.password):
                login(request, user)
                # Redirigir según el rol del usuario
                if user.idrol.idrol == 1:
                    return redirect('inicio')
                elif user.idrol.idrol == 2:
                    # Redireccionar al cliente a una vista especial
                    return redirect('productos')
                elif user.idrol.idrol == 3:
                    return redirect('homeTecnicosEnvios')
                else:
                    return redirect('vista_por_defecto')
            else:
                # Si las credenciales son incorrectas, mostrar un mensaje de error
                return HttpResponse('Credenciales incorrectas')
    else:
        form = LoginForm()

    return render(request, 'Login.html', {'form': form})



#decorador de vistas
def role_required(required_idrol):
    def decorator(view_func):
        def _wrapped_view_func(request, *args, **kwargs):
            if request.user.idrol.idrol == required_idrol:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden('No tienes permiso para acceder a esta página.')
        return _wrapped_view_func
    return decorator

#cierre de sesion
def logoutView(request):
    logout(request)
    return redirect('login')

#Restablecer contraseña

token_generator = PasswordResetTokenGenerator()
class PasswordResetRequestView(APIView):
    
    def post(self, request):
        email = request.data.get('email')
        user = Usuarios.objects.filter(email=email).first()
        if user:
            token_generator = PasswordResetTokenGenerator()
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = token_generator.make_token(user)
            reset_link = f'http://127.0.0.1:8000/account/reestablecer_password_enlace/{uidb64}/{token}'
            send_mail(
                    'Solicitud de restablecimiento de contraseña',
                    f'Por favor, sigue este enlace para restablecer tu contraseña: {reset_link}',
                    'jjsystemproject@gmail.com',
                    [email],
                    fail_silently=False,
                )
            return Response({'message': 'Correo electrónico de restablecimiento de contraseña enviado'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No se encontró ningún usuario con este correo electrónico'}, status=status.HTTP_404_NOT_FOUND)

class PasswordResetConfirmView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_bytes(base64.urlsafe_b64decode(uidb64))
            user = Usuarios.objects.get(pk=uid)
            if token_generator.check_token(user, token):
                form = NewPasswordForm()
                return render(request, 'password_reset_confirm.html', {'form': form, 'uidb64': uidb64, 'token': token})
            else:
                return HttpResponse('Token de restablecimiento de contraseña inválido', status=400)
        except (TypeError, ValueError, OverflowError, Usuarios.DoesNotExist):
            return HttpResponse('Enlace de restablecimiento de contraseña inválido', status=400)

    def post(self, request, uidb64, token):
        try:
            uid = force_bytes(base64.urlsafe_b64decode(uidb64))
            user = Usuarios.objects.get(pk=uid)
            if token_generator.check_token(user, token):
                form = NewPasswordForm(request.POST)
                if form.is_valid():
                    user.password = make_password(form.cleaned_data['new_password'])
                    user.save()
                    return redirect('login')
                else:
                    return render(request, 'password_reset_confirm.html', {'form': form})
            else:
                return HttpResponse('Token de restablecimiento de contraseña inválido', status=400)
        except (TypeError, ValueError, OverflowError, Usuarios.DoesNotExist):
            return HttpResponse('Enlace de restablecimiento de contraseña inválido', status=400)

def password_reset_request(request):
    return render(request, 'password_reset_form.html')

