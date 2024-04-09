import base64
from django.conf import settings
from django.utils.encoding import force_bytes
from django.shortcuts import get_object_or_404, render, HttpResponse
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
from django.contrib import messages
from django.core.exceptions import ValidationError
from Account.envio_correo import enviar_correo_registro
from django.template.loader import render_to_string


def registerView(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            # Verificar si el correo electrónico ya está registrado
            if Usuarios.objects.filter(email=email).exists():
                messages.error(request, 'Este correo electrónico ya está registrado.')
            else:
                # Verificar la complejidad de la contraseña
                password = form.cleaned_data['password']
                if len(password) < 8:
                    messages.error(request, 'La contraseña debe tener al menos 8 caracteres.')
                elif not any(char.isupper() for char in password):
                    messages.error(request, 'La contraseña debe contener al menos una letra mayúscula.')
                elif not any(char.islower() for char in password):
                    messages.error(request, 'La contraseña debe contener al menos una letra minúscula.')
                elif not any(char.isdigit() for char in password):
                    messages.error(request, 'La contraseña debe contener al menos un número.')
                elif not any(char in '!@#$%^&*()_+=-{}[]:;\'\"|<>,.?/~`' for char in password):
                    messages.error(request, 'La contraseña debe contener al menos un caracter especial.')
                else:
                    # Validar longitud de número de documento y número de contacto
                    numerodocumento = form.cleaned_data['numerodocumento']
                    if len(str(numerodocumento)) != 10:
                        messages.error(request, 'El número de documento debe tener exactamente 10 dígitos.')
                    else:
                        numerocontacto = form.cleaned_data['numerocontacto']
                        if len(str(numerocontacto)) != 10:
                            messages.error(request, 'El número de contacto debe tener exactamente 10 dígitos.')
                        else:
                            # Si pasa todas las validaciones, guarda el usuario
                            user = form.save(commit=False)
                            user.password = make_password(password)
                            user.idrol = Roles.objects.get(idrol=2)  # Asigna el rol de cliente
                            user.idestadosusuarios = Estadosusuarios.objects.get(idestadousuario=1)  # Asigna el estado de usuario activo
                            user.save()
                            
                            # Enviar correo de agradecimiento
                            enviar_correo_registro(email)

                            messages.success(request, 'Se ha registrado correctamente')
                            return redirect('login')
        else:
            messages.error(request, 'Por favor, verifica tus datos e inténtalo de nuevo.')
    else:
        form = RegisterForm()

    return render(request, 'Register.html', {'form': form})


def userLogin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = get_object_or_404(Usuarios, email=email)
                if user is not None and check_password(password, user.password):
                    login(request, user)
                    messages.success(request, 'Inicio de sesión exitoso')
                    if user.idrol.idrol == 1:
                        return redirect('inicio')
                    elif user.idrol.idrol == 2:
                        return redirect('productos')
                    elif user.idrol.idrol == 3:
                        return redirect('tecnico_home')
                    else:
                        messages.error(request, 'Usuario autenticado con un rol no válido')
                else:
                    messages.error(request, 'Credenciales incorrectas')
                    return redirect('login')
            except Usuarios.DoesNotExist:
                messages.error(request, 'Usuario no encontrado')
                return redirect('login')
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
    messages.success(request, 'Se ha cerrado tu sesión')
    return redirect('login')

#Restablecer contraseña

token_generator = PasswordResetTokenGenerator()
class PasswordResetRequestView(APIView):
    
    def post(self, request):
        try:
            email = request.data.get('email')
            user = Usuarios.objects.filter(email=email).first()
            if user:
                token_generator = PasswordResetTokenGenerator()
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                token = token_generator.make_token(user)
                reset_link = f'https://jjsystem.onrender.com/account/reestablecer_password_enlace/{uidb64}/{token}'
                asunto = 'Solicitud de restablecimiento de contraseña'
                correo_origen = settings.EMAIL_HOST_USER
                html_message = render_to_string('correo_reset_password.html', {'usuario': user, 'reset_link':reset_link})
                user_email = user.email
                send_mail(asunto, '', correo_origen, [user_email], html_message=html_message)
                messages.success(request,'Se ha enviado el correo de restablecimiento de contraseña, correctamente')
            else:
                messages.error(request, 'Ocurrio un error al enviar el correo, intentalo de nuevo')
        except Exception as e:
            messages.error(request, f'Ocurrió un error: {str(e)}')
        return redirect('password_reset_request_form')
    
class PasswordResetConfirmView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_bytes(base64.urlsafe_b64decode(uidb64))
            user = Usuarios.objects.get(pk=uid)
            if token_generator.check_token(user, token):
                form = NewPasswordForm()
                return render(request, 'password_reset_confirm.html', {'form': form, 'uidb64': uidb64, 'token': token})
            else:
                messages.error(request, 'Token de restablecimiento de contraseña inválido')
        except ValidationError:
            messages.error(request, 'Enlace de restablecimiento de contraseña inválido', status=400)
        except Usuarios.DoesNotExist:
            messages.error(request, 'Enlace de restablecimiento de contraseña inválido', status=400)
        except (TypeError, ValueError, OverflowError):
            messages.error(request, 'Ocurrió un error al procesar el enlace de restablecimiento de contraseña', status=400)
    def post(self, request, uidb64, token):
        try:
            uid = force_bytes(base64.urlsafe_b64decode(uidb64))
            user = Usuarios.objects.get(pk=uid)
            if token_generator.check_token(user, token):
                form = NewPasswordForm(request.POST)
                if form.is_valid():
                    user.password = make_password(form.cleaned_data['new_password'])
                    user.save()
                    messages.success(request, 'Se ha cambiado tu contraseña correctamente')
                    return redirect('login')
                else:
                    return render(request, 'password_reset_confirm.html', {'form': form})
            else:
                return messages.error(request,'Token de restablecimiento de contraseña inválido')
        except (TypeError, ValueError, OverflowError, Usuarios.DoesNotExist):
            return messages.error(request,'Enlace de restablecimiento de contraseña inválido')

def password_reset_request(request):
    return render(request, 'password_reset_form.html')

