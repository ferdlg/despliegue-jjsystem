from django.utils import timezone
from rest_framework import viewsets
from Account.models import *
from .serializers import RespuestaPqrsfSerializer
from django.shortcuts import redirect, render
from django.contrib import messages

class respuestaCRUD(viewsets.ModelViewSet):
    queryset = Pqrsf.objects.all()
    serializer_class = RespuestaPqrsfSerializer

    def crear_respuesta(self, request, id_pqrsf):

        try:
            if request.method == 'POST':
                numerodocumento = request.user.numerodocumento
                admin = Administrador.objects.get(numerodocumento = numerodocumento)
                fecha = timezone.now().date()
                informacionrespuesta = request.POST.get('informacionrespuesta')
                idpqrsf = Pqrsf.objects.get(idpqrsf = id_pqrsf)

                respuesta = Respuestas.objects.create(
                    fecha = fecha,
                    informacionrespuesta=informacionrespuesta,
                    idadministrador=admin,
                    idpqrsf=idpqrsf
                )
                messages.success(request, 'Respuesta registrada correctamente')
        except Administrador.DoesNotExist:
            messages.error(request,'Administrador no encontrado')
        except Pqrsf.DoesNotExist:
            messages.error(request,'PQRSF no encontrada')
        except Exception as e:
            messages.error(request, f'Error al intentar crear la respuesta: {str(e)}')
        
        return redirect('homePqrsf')
        