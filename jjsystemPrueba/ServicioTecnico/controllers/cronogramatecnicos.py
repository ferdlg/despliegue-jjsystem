from datetime import datetime
from django.shortcuts import render, redirect
from rest_framework import viewsets
from Account.models import Cronogramatecnicos, Tecnicos, Citas
from .serializers import CronogramatecnicosSerializer


class cronogramatecnicosCRUD(viewsets.ModelViewSet):
    queryset = Cronogramatecnicos.objects.all()
    serializer_class = CronogramatecnicosSerializer
  
    def ver_agenda(request, idtecnico):
        try:
            cronograma = Cronogramatecnicos.objects.get(idtecnico = idtecnico)

            return render(request, 'mi_agenda.html',{'agenda':cronograma})
        except Cronogramatecnicos.DoesNotExist:
            return render(request, 'mi_agenda.html',{'agenda':'Aun no tienes agenda'})
        
    def citas_tecnico(self,request):
        usuario = request.user
        tecnico = Tecnicos.objects.get(numerodocumento=usuario.numerodocumento)
        todas_las_citas = Citas.objects.filter(idtecnico=tecnico.idtecnico)

        fecha_obj = None
        fecha_filtro = request.GET.get('fecha')
        if fecha_filtro:
            try:
                fecha_obj = datetime.strptime(fecha_filtro, '%Y-%m-%d').date()
                citas_filtradas = todas_las_citas.filter(fechacita=fecha_obj)
            except ValueError:
                mensaje = 'Formato de fecha inválido. Utilice el formato AAAA-MM-DD.'
                return render(request, 'mensaje.html', {'mensaje': mensaje})
        else:
            citas_filtradas = []

        return render(request, 'Tecnicos/mis_citas.html', {'todas_las_citas': todas_las_citas, 'citas_filtradas': citas_filtradas, 'fecha_obj':fecha_obj})
    
    
