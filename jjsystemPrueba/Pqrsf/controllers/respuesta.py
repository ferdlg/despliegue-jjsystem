from django.utils import timezone
from rest_framework import viewsets
from Account.models import *
from ..correos import correo_respuesta_cliente
from .serializers import RespuestaPqrsfSerializer
from django.shortcuts import redirect, render
from django.contrib import messages

class respuestaCRUD(viewsets.ModelViewSet):
    queryset = Pqrsf.objects.all()
    serializer_class = RespuestaPqrsfSerializer

    def crear_respuesta(self, request, id_pqrsf):
        try:
            # Verificar si ya existe una respuesta para la PQRSF
            if Respuestas.objects.filter(idpqrsf=id_pqrsf).exists():
                messages.error(request, 'Ya existe una respuesta para esta PQRSF')
                return redirect('homePqrsf')
            
            if request.method == 'POST':
                numerodocumento = request.user.numerodocumento
                admin = Administrador.objects.get(numerodocumento=numerodocumento)
                fecha = timezone.now().date()
                informacionrespuesta = request.POST.get('informacionrespuesta')
                pqrsf = Pqrsf.objects.get(idpqrsf=id_pqrsf)

                respuesta = Respuestas.objects.create(
                    fecha=fecha,
                    informacionrespuesta=informacionrespuesta,
                    idadministrador=admin,
                    idpqrsf=pqrsf
                )
                
                messages.success(request, 'Respuesta registrada correctamente')
                correo_respuesta_cliente(request, idpqrsf=id_pqrsf)
        except Administrador.DoesNotExist:
            messages.error(request, 'Administrador no encontrado')
        except Pqrsf.DoesNotExist:
            messages.error(request, 'PQRSF no encontrada')
        except Exception as e:
            messages.error(request, f'Error al intentar crear la respuesta: {str(e)}')

        return redirect('homePqrsf')
