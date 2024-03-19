from django import forms
from Account.models import Tecnicos, Usuarios
from Account.models import Roles
from Account.models import Estadosusuarios

class RegisterForm(forms.ModelForm):
    numerodocumento = forms.IntegerField(label='Numero de documento', widget=forms.NumberInput(attrs={'class': 'form-control border-0', 'required': True}))
    nombre = forms.CharField(label='Nombre', widget=forms.TextInput(attrs={'class': 'form-control', 'required': True}))
    apellido = forms.CharField(label='Apellido', widget=forms.TextInput(attrs={'class': 'form-control', 'required': True}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control', 'required': True}))
    numerocontacto = forms.IntegerField(label='Numero de contacto', widget=forms.NumberInput(attrs={'class': 'form-control', 'required': True}))

    class Meta:
        model = Usuarios
        exclude = ['password','idrol', 'idestadosusuarios', 'last_login']

class EditTecnicosForm(forms.ModelForm):
    especialidad = forms.CharField(label='Especialidad', widget=forms.TextInput(attrs={'class': 'form-control', 'required': True}))

    class Meta:
        model = Tecnicos
        fields = ['numerodocumento', 'especialidad']
        exclude = ['numerodocumento']

