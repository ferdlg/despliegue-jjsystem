import os
from unittest import TestCase
import django
import pytest

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jjsystemPrueba.settings')
django.setup()

from Account.models import Servicios, Categoriasservicios

class TestServicio(TestCase):

    def setUp(self):
        categoria = Categoriasservicios.objects.get(idcategoriaservicio = 1)
        self.servicio = Servicios.objects.create(
            nombreservicio='prueba',
            descripcionservicio='prueba test',
            idcategoriaservicio= categoria
        )

    def test_servicio_crear(self):
        servicio = Servicios.objects.get(idservicio=self.servicio.idservicio)
        self.assertEqual(servicio.nombreservicio, 'prueba')
        self.assertEqual(servicio.descripcionservicio, 'prueba test')

    def test_servicio_actualizar(self):
        servicio = Servicios.objects.get(idservicio=self.servicio.idservicio)
        servicio.nombreservicio = 'Nuevo nombre de servicio'
        servicio.descripcionservicio = 'Nueva descripción de servicio'
        servicio.save()
        servicio_actualizado = Servicios.objects.get(idservicio=self.servicio.idservicio)
        self.assertEqual(servicio_actualizado.nombreservicio, 'Nuevo nombre de servicio')
        self.assertEqual(servicio_actualizado.descripcionservicio, 'Nueva descripción de servicio')

    def test_servicio_eliminar(self):
        servicio = Servicios.objects.get(idservicio=self.servicio.idservicio)
        servicio.delete()
        with self.assertRaises(Servicios.DoesNotExist):
            Servicios.objects.get(idservicio=self.servicio.idservicio)