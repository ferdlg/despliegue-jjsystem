# tests/test_models.py
from django.test import TestCase
from unittest import TestCase
from Account.models import Envios, Tecnicos, Estadosenvios

class TestEnvio(TestCase):

    def setUp(self):
        tecnico = Tecnicos.objects.get(idtecnico=5)
        estado_envio = Estadosenvios.objects.get(idestadoenvio=1)
        self.envio = Envios.objects.create(
            direccionenvio='',
            idtecnico=tecnico,
            idestadoenvio=estado_envio
        )

    def test_envio_crear(self):
        envio = Envios.objects.get(idenvio=self.envio.idenvio)
        self.assertEqual(envio.direccionenvio, '')  
        self.assertEqual(envio.idtecnico, Tecnicos.objects.get(idtecnico=5))
        self.assertEqual(envio.idestadoenvio, Estadosenvios.objects.get(idestadoenvio=1))

    def test_envio_actualizar(self):
        envio = Envios.objects.get(idenvio=self.envio.idenvio)
        
        nuevo_estado = Estadosenvios.objects.get(idestadoenvio=2)
        envio.idestadoenvio = nuevo_estado
        envio.save()

        envio_actualizado = Envios.objects.get(idenvio=self.envio.idenvio)
        self.assertEqual(envio_actualizado.idestadoenvio, nuevo_estado)
    
    def test_envio_eliminar(self):
        envio = Envios.objects.get(idenvio=self.envio.idenvio)

        envio.delete()
        with self.assertRaises(Envios.DoesNotExist):
            Envios.objects.get(idenvio=self.envio.idenvio)