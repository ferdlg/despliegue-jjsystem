from django.shortcuts import redirect, render
from django.contrib.auth.hashers import make_password, check_password


def actualizar_datos_usuario(request, redirect_to):
    usuario = request.user
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        email = request.POST.get('email')
        numerodocumento = request.POST.get('numerodocumento')
        numerocontacto = request.POST.get('numerocontacto')

        usuario.nombre = nombre
        usuario.apellido = apellido
        usuario.email = email
        usuario.numerodocumento = numerodocumento
        usuario.numerocontacto = numerocontacto
        usuario.save()

        return redirect(redirect_to)

    return render(request, redirect_to + '.html', {'usuario': usuario})

def validar_password(self, request):
    usuario = request.user
    password = make_password(request.POST.get('password'))
    if check_password(password, usuario.password):
        password_correct = True
    else:
        password_correct = False

    if usuario.idrol.idrol == 1 or usuario.idrol.idrol == 3:
        return redirect('mi_perfil',{'password_correct':password_correct})
    elif usuario.idrol.idrol == 2:
        return redirect('ver_perfil',{'password_correct':password_correct})
    else:
        return redirect('pagina_error',{'password_correct':password_correct})

def cambiar_password(self, request):
    usuario = request.user
    new_password = request.POST.get('new_password')

    usuario.password = make_password(new_password)
    usuario.save()

    if usuario.idrol.idrol == 1 or usuario.idrol.idrol == 3:
        return redirect('mi_perfil')
    elif usuario.idrol.idrol == 2:
        return redirect('ver_perfil')
    else:
        return redirect('pagina_error')