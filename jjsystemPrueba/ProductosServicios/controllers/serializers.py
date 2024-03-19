from rest_framework import serializers
from Account.models import *

#creamos una clase serializers para cada tabla
class RolesSerializers(serializers.ModelSerializer):
    #incluimos la clase Meta, para que le de instrucciones al serializador
    class Meta:
    #le indicamos el modelo que debe buscar
        model = Roles
    #le especificamos los campos que debe serializar
        fields = '__all__'

class PermisosSerializers(serializers.ModelSerializer):
    class Meta:
        model = Permisos
        fields = '__all__'

class Rol_has_permisosSerializers(serializers.ModelSerializer):
    class Meta:
        model = RolesHasPermisos
        fields = '__all__'
'''
Nota: en tablas en las que debemos traer opciones,
se deben especificar uno por uno los campos a serializar
'''

class UsuariosSerializers(serializers.ModelSerializer):
    class Meta:
        model = Usuarios
        fields = '__all__'


class ClientesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Clientes
        fields = '__all__'

class CategoriasProductosSerializers(serializers.ModelSerializer):
    class Meta:
        model = Categoriasproductos
        fields = '__all__'

class CategoriasServiciosSerializers(serializers.ModelSerializer):
    class Meta:
        model = Categoriasservicios
        fields = '__all__'

class ProductosSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Productos
        fields = '__all__'

class ServiciosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicios
        fields = '__all__'

class ProveedoresProductosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedoresproductos
        fields = '__all__'
    
class VentasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ventas
        fields = '__all__'

class DetalleVentasSerializer(serializers.ModelSerializer):
    class Meta:
        model =Detallesventas
        fields = '__all__'