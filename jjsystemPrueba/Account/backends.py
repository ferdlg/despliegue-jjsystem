from django.contrib.auth.backends import ModelBackend
from .models import Usuarios

class UsuariosBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = Usuarios.objects.get(email=email, password=password)
            if user.idestadosusuarios.idestadousuario== 1:  # Verifica si el usuario está activo
                return user
        except Usuarios.DoesNotExist:
            return None


    def get_user(self, numerodocumento):
        try:
            return Usuarios.objects.get(numerodocumento=numerodocumento)
        except Usuarios.DoesNotExist:
            return None
