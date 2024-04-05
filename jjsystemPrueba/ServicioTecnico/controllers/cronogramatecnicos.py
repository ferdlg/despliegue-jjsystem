from datetime import datetime, time, timedelta
from django.shortcuts import render, redirect
from rest_framework import viewsets
from Account.models import Clientes, Cronogramatecnicos, Tecnicos, Citas
from .serializers import CronogramatecnicosSerializer
import json
from django.contrib import messages

def es_fin_de_semana(fecha):
    return fecha.weekday() in [5, 6] 
    
def obtener_disponibilidad_tecnico(idtecnico):
    tecnico = Tecnicos.objects.get(idtecnico=idtecnico)
    citas_programadas_tecnico = Citas.objects.filter(idtecnico=idtecnico)
    hoy = datetime.today()
    disponibilidad = []

    # Iterar sobre los días de los próximos 30 días
    for i in range(30):
        fecha = hoy + timedelta(days=i)
        if not es_fin_de_semana(fecha):
            horas_ocupadas = [cita.horacita.hour for cita in citas_programadas_tecnico if cita.fechacita == fecha]
            horas_disponibles = [hora for hora in range(7, 19) if hora not in horas_ocupadas]
            disponibilidad.append({'fecha': fecha, 'horas_disponibles': horas_disponibles})
        
    return disponibilidad
class cronogramatecnicosCRUD(viewsets.ModelViewSet):
    queryset = Cronogramatecnicos.objects.all()
    serializer_class = CronogramatecnicosSerializer

    def ver_agenda(request):
        try:
            return render(request, 'mi_agenda.html')
        except Cronogramatecnicos.DoesNotExist:
            return render(request, 'mi_agenda.html',{'agenda':'Aun no tienes agenda'})
        
    def citas_tecnico(self,request):
        usuario = request.user
        tecnico = Tecnicos.objects.get(numerodocumento=usuario.numerodocumento)
        todas_las_citas = Citas.objects.filter(idtecnico=tecnico.idtecnico)

        cliente_cita = []
        for cita in todas_las_citas:
            cliente = Clientes.objects.get(numerodocumento = cita.idcotizacion.idcliente.numerodocumento)
            cliente_cita.append({'cita':cita, 'cliente':cliente})

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

        return render(request, 'Tecnicos/mis_citas.html', {'todas_las_citas': todas_las_citas, 'citas_filtradas': citas_filtradas, 'fecha_obj':fecha_obj, 'cliente_cita':cliente_cita})
    
    def citas_eventos_tecnicos(self,request):
        usuario = request.user
        tecnico = Tecnicos.objects.get(numerodocumento=usuario.numerodocumento)
        todas_las_citas = Citas.objects.filter(idtecnico=tecnico.idtecnico)
        fechas_disponibles = obtener_disponibilidad_tecnico(idtecnico=tecnico.idtecnico)
        eventos = []
        for cita in todas_las_citas:
            fecha_hora_inicio = datetime.combine(cita.fechacita, cita.horacita)
            eventos.append({
                'title': cita.descripcioncita,
                'start': fecha_hora_inicio.strftime('%Y-%m-%d %H:%M:%S'),
                
            })
        
        for fecha_disponible in fechas_disponibles:
            for hora_disponible in fecha_disponible['horas_disponibles']:
                # Crear una fecha y hora combinadas
                fecha_hora_disponible = datetime.combine(fecha_disponible['fecha'], time(hour=hora_disponible))
                eventos.append({
                    'title': 'Disponible',
                    'start': fecha_hora_disponible.strftime('%Y-%m-%d %H:%M:%S'),
                    'color': 'green'
                })

        eventos_json = json.dumps(eventos)
        return render(request, 'Tecnicos/mi_agenda.html', {'eventos_json': eventos_json})
    
    #vista Administrador ve agenda del tecnico 
    def admin_ver_agenda_tecnico(self, request, idtecnico):
        try:
            tecnico = Tecnicos.objects.get(idtecnico=idtecnico)
            todas_las_citas = Citas.objects.filter(idtecnico=idtecnico)
            eventos = []
            for cita in todas_las_citas:
                fecha_hora_inicio = datetime.combine(cita.fechacita, cita.horacita)
                eventos.append({
                'title': cita.descripcioncita,
                'start': fecha_hora_inicio.strftime('%Y-%m-%d %H:%M:%S'),
                })

            eventos_json = json.dumps(eventos)
            cliente_cita = []
            for cita in todas_las_citas:
                cliente = Clientes.objects.get(numerodocumento=cita.idcotizacion.idcliente.numerodocumento)
                cliente_cita.append({'cita': cita, 'cliente': cliente})

            fecha_obj = None
            fecha_filtro = request.GET.get('fechacita')
            if fecha_filtro:
                try:
                    fecha_obj = datetime.strptime(fecha_filtro, '%Y-%m-%d').date()
                    citas_filtradas = todas_las_citas.filter(fechacita=fecha_obj)
                except ValueError:
                    messages.error(request,'Formato de fecha inválido. Utilice el formato AAAA-MM-DD.')
            else:
                citas_filtradas = []

            fechas_disponibles=obtener_disponibilidad_tecnico(idtecnico=idtecnico)
            return render(request, 'Admin-Agendas/tecnico_agenda.html', {
                'todas_las_citas': todas_las_citas,
                'citas_filtradas': citas_filtradas,
                'fecha_obj': fecha_obj,
                'cliente_cita': cliente_cita,
                'tecnico':tecnico,
                'eventos_json': eventos_json,
                'fechas_disponibles':fechas_disponibles})
        except Tecnicos.DoesNotExist:
            return render(request, 'Admin-Agendas/tecnico_agenda.html', {'mensaje': 'El técnico especificado no existe'})
        


