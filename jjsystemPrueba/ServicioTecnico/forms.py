from django import forms
from Account.models import Tecnicos, Usuarios, Especialidadtecnicos
from Account.models import Roles
from Account.models import Estadosusuarios

class RegisterForm(forms.ModelForm):
    numerodocumento = forms.IntegerField(label='Numero de documento', widget=forms.NumberInput(attrs={'class': 'form-control', 'required': True}))
    nombre = forms.CharField(label='Nombre', widget=forms.TextInput(attrs={'class': 'form-control', 'required': True}))
    apellido = forms.CharField(label='Apellido', widget=forms.TextInput(attrs={'class': 'form-control', 'required': True}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control', 'required': True}))
    numerocontacto = forms.IntegerField(label='Numero de contacto', widget=forms.NumberInput(attrs={'class': 'form-control', 'required': True}))

    class Meta:
        model = Usuarios
        exclude = ['password','idrol', 'idestadosusuarios', 'last_login']

class EditTecnicosForm(forms.ModelForm):
    id_especialidad_fk = forms.ModelChoiceField(queryset=Especialidadtecnicos.objects.all(), label='Especialidad', widget=forms.Select(attrs={'class': 'form-control', 'required': True}))

    class Meta:
        model = Tecnicos
        fields = ['id_especialidad_fk']
        exclude = ['numerodocumento']