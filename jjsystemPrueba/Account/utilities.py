from django.shortcuts import redirect, render
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from Account.forms import NewPasswordForm
from .models import Usuarios

def actualizar_datos_usuario(request, redirect_to):
    usuario = request.user
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        email = request.POST.get('email')
        numerodocumento = request.POST.get('numerodocumento')
        numerocontacto = request.POST.get('numerocontacto')

        # Verificar si el correo electrónico ya está registrado en otro usuario
        if Usuarios.objects.exclude(id=usuario.id).filter(email=email).exists():
            messages.error(request, 'Este correo electrónico ya está registrado. Por favor, ingresa uno diferente.')
        else:
            usuario.nombre = nombre
            usuario.apellido = apellido
            usuario.email = email
            usuario.numerodocumento = numerodocumento
            usuario.numerocontacto = numerocontacto
            
            # Validar los campos
            if len(numerodocumento) != 10:
                messages.error(request, 'El número de documento debe tener exactamente 10 dígitos.')
            elif len(numerocontacto) != 10:
                messages.error(request, 'El número de contacto debe tener exactamente 10 dígitos.')
            else:
                usuario.save()
                messages.success(request, 'Se han actualizado tus datos correctamente.')
                return redirect(redirect_to)
    return render(request, redirect_to + '.html', {'usuario': usuario})


def validar_password(request):
    usuario = request.user
    password = request.POST.get('password')

    if check_password(password, usuario.password):
        password_correct = True
    else:
        password_correct = False

    if usuario.idrol.idrol == 1 or usuario.idrol.idrol == 3:
        return render(request, 'cambiar_password.html', {'password_correct': password_correct})
    elif usuario.idrol.idrol == 2:
        return render(request, 'cliente/cambiar_password.html', {'password_correct': password_correct})
    else:
        return redirect('pagina_error')

def cambiar_password(request):
    if request.method == 'POST':
        form = NewPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            usuario = request.user

            # Verificar la complejidad de la nueva contraseña
            if len(new_password) < 8:
                messages.error(request, 'La contraseña debe tener al menos 8 caracteres.')
            elif not any(char.isupper() for char in new_password):
                messages.error(request, 'La contraseña debe contener al menos una letra mayúscula.')
            elif not any(char.islower() for char in new_password):
                messages.error(request, 'La contraseña debe contener al menos una letra minúscula.')
            elif not any(char.isdigit() for char in new_password):
                messages.error(request, 'La contraseña debe contener al menos un número.')
            elif not any(char in '!@#$%^&*()_+=-{}[]:;\'\"|<>,.?/~`' for char in new_password):
                messages.error(request, 'La contraseña debe contener al menos un caracter especial.')
            else:
                # Guardar la nueva contraseña
                usuario.password = make_password(new_password)
                usuario.save()

                if usuario.idrol.idrol == 1 or usuario.idrol.idrol == 3:
                    return redirect('mi_perfil')
                elif usuario.idrol.idrol == 2:
                    return redirect('actualizar_mis_datos')
                else:
                    mensaje = 'Ocurrió un error al intentar actualizar la contraseña.'
                    return render(request, 'mensaje.html', {'mensaje': mensaje})
    else:
        form = NewPasswordForm()

    return render(request, 'cambiar_password.html', {'form': form})