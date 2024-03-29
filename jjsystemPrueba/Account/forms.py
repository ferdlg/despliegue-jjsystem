from django import forms
from .models import Usuarios
from .models import Roles
from .models import Estadosusuarios

class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class RegisterForm(forms.ModelForm):
    numerodocumento = forms.IntegerField(label='Numero de documento', widget=forms.NumberInput(attrs={'class': 'form-control border-0 ','style': 'max-width: 94%; border-top-right-radius: 100px;', 'required': True}))
    nombre = forms.CharField(label='Nombre', widget=forms.TextInput(attrs={'class': 'form-control', 'required': True}))
    apellido = forms.CharField(label='Apellido', widget=forms.TextInput(attrs={'class': 'form-control', 'required': True}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control', 'required': True}))
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control', 'required': True}))
    numerocontacto = forms.IntegerField(label='Numero de contacto', widget=forms.NumberInput(attrs={'class': 'form-control', 'required': True}))

    class Meta:
        model = Usuarios
        exclude = ['idrol', 'idestadosusuarios', 'last_login']


class NewPasswordForm(forms.Form):
    new_password = forms.CharField(label='Nueva Contraseña', widget=forms.PasswordInput)

    def clean_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        if not new_password:
            raise forms.ValidationError('Debes ingresar una nueva contraseña.')
        return new_password