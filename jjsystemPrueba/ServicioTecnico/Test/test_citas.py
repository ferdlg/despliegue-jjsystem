import os
from unittest import TestCase
import django
import pytest

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jjsystemPrueba.settings')
django.setup()

from Account.models import Citas, Tecnicos, Administrador, Cotizaciones, Estadoscitas

class TestCita(TestCase):

    def setUp(self):
        tecnico = Tecnicos.objects.get(idtecnico=5)
        administrador = Administrador.objects.get(idadministrador=1)
        cotizacion = Cotizaciones.objects.get(idcotizacion=1)
        estado_cita = Estadoscitas.objects.get(idestadocita=1)
        self.cita = Citas.objects.create(
            fechacita='',
            direccioncita='',
            contactocliente=123456789,  # Número de contacto de ejemplo
            descripcioncita='prueba test',
            idtecnico=tecnico,
            idadministrador=administrador,
            idcotizacion=cotizacion,
            idestadocita=estado_cita
        )

    def test_cita_crear(self):
        cita = Citas.objects.get(idcita=self.cita.idcita)
        self.assertEqual(cita.fechacita, '')  
        self.assertEqual(cita.direccioncita, '')  
        self.assertEqual(cita.descripcioncita, 'prueba test')
        self.assertEqual(cita.contactocliente, 123456789) 

    def test_cita_actualizar(self):
        cita = Citas.objects.get(idcita=self.cita.idcita)
        
        cita.descripcioncita = 'Nueva descripción'
        cita.save()

        cita_actualizada = Citas.objects.get(idcita=self.cita.idcita)
        self.assertEqual(cita_actualizada.descripcioncita, 'Nueva descripción')
    
    def test_cita_eliminar(self):
        cita = Citas.objects.get(idcita=self.cita.idcita)

        cita.delete()

