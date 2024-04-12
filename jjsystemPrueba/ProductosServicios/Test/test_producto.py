import os
from unittest import TestCase
import django
import pytest

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jjsystemPrueba.settings')
django.setup()

from Account.models import Productos, Categoriasproductos, Administrador, Proveedoresproductos

class TestProducto(TestCase):

    def setUp(self):
        categoria = Categoriasproductos.objects.get(idcategoriaproducto = 1)
        administrador = Administrador.objects.get(idadministrador = 1)
        proveedor = Proveedoresproductos.objects.get(idproveedorproducto = 1)
        self.producto = Productos.objects.create(
            nombreproducto = 'producto nuevo',
            descripcionproducto = 'test de productos',
            precioproducto = 15000,
            cantidad = 45,
            idadministrador = administrador,
            idcategoriaproducto = categoria,
            idproveedorproducto = proveedor
        )

    def test_producto_crear(self):
        producto = Productos.objects.get(idproducto=self.producto.idproducto)
        self.assertEqual(producto.nombreproducto, 'producto nuevo')
        self.assertEqual(producto.descripcionproducto, 'test de productos')
        self.assertEqual(producto.precioproducto,15000 )
        self.assertEqual(producto.cantidad,45 )
    
    def test_producto_actualizar(self):
        producto = Productos.objects.get(idproducto=self.producto.idproducto)

        producto.nombreproducto = 'Nuevo nombre de producto'
        producto.descripcionproducto = 'Nueva descripción de producto'
        producto.precioproducto = 20000
        producto.cantidad = 50
        producto.save()  

        producto_actualizado = Productos.objects.get(idproducto=self.producto.idproducto)
        self.assertEqual(producto_actualizado.nombreproducto, 'Nuevo nombre de producto')
        self.assertEqual(producto_actualizado.descripcionproducto, 'Nueva descripción de producto')
        self.assertEqual(producto_actualizado.precioproducto, 20000)
        self.assertEqual(producto_actualizado.cantidad, 50)


def test_producto_eliminar(self):
    producto = Productos.objects.get(idproducto=self.producto.idproducto)
    producto.delete()  

    with self.assertRaises(Productos.DoesNotExist):
        Productos.objects.get(idproducto=self.producto.idproducto)

