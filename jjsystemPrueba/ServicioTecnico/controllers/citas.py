from django.shortcuts import render, redirect
from rest_framework import viewsets
from Account.models import Citas , Cotizaciones, Tecnicos, Administrador , Estadoscitas, Usuarios
from ..correos import correo_cita_agendada
from .serializers import CitasSerializer
from django.core.paginator import Paginator , EmptyPage , PageNotAnInteger
from django.contrib import messages
import datetime
import pytz

class citasCRUD(viewsets.ModelViewSet):
    queryset = Citas.objects.all()
    serializer_class = CitasSerializer

    #Metodo para obtener solo las citas de analisis
    def cita_analisis(self, request):
        estados = Estadoscitas.objects.all()
        tecnicos = Tecnicos.objects.all()
        cotizaciones = Cotizaciones.objects.all()
        # Obtener datos de la cita
        citas_queryset = Citas.objects.filter(idcotizacion__cotizacionesservicios__idservicio__idcategoriaservicio=3)
        paginator = Paginator(citas_queryset, 5)  # Mostrar 5 citas por página

        page_number = request.GET.get('page')

        try:
            citas_page = paginator.page(page_number)
        except PageNotAnInteger:
            citas_page = paginator.page(1)
        except EmptyPage:
            citas_page = paginator.page(paginator.num_pages)

        # Obtener los datos de la página de citas
        citas_serializer = CitasSerializer(citas_page, many=True)
        citas_data = citas_serializer.data

        # Devolver la página renderizada con las citas y la paginación
        return render(request, 'Admin-Citas/citaAnalisis.html', {'citas': citas_data, 'citas_page': citas_page, 'estados': estados, 'tecnicos': tecnicos, 'cotizaciones':cotizaciones})
    
    #Metodo para obtener solo las citas de instalacion
    def cita_instalacion(self, request):
        estados = Estadoscitas.objects.all()
        tecnicos = Tecnicos.objects.all()
        cotizaciones = Cotizaciones.objects.all()

        # Obtener datos de la cita
        citas_queryset = Citas.objects.filter(idcotizacion__cotizacionesservicios__idservicio__idcategoriaservicio=2)
        paginator = Paginator(citas_queryset, 5)  # Mostrar 5 citas de instalación por página

        page_number = request.GET.get('page')

        try:
            citas_page = paginator.page(page_number)
        except PageNotAnInteger:
            citas_page = paginator.page(1)
        except EmptyPage:
            citas_page = paginator.page(paginator.num_pages)

        # Obtener los datos de la página de citas
        citas_serializer = CitasSerializer(citas_page, many=True)
        citas_data = citas_serializer.data

        # Devolver la página renderizada con las citas y la paginación
        return render(request, 'Admin-Citas/citaInstalacion.html', {'citas': citas_data, 'citas_page': citas_page, 'estados': estados, 'tecnicos': tecnicos, 'cotizaciones':cotizaciones})
    
    def cita_mantenimiento(self, request):
        estados = Estadoscitas.objects.all()
        tecnicos = Tecnicos.objects.all()
        cotizaciones = Cotizaciones.objects.all()


        citas_queryset = Citas.objects.filter(idcotizacion__cotizacionesservicios__idservicio__idcategoriaservicio=4)
        paginator = Paginator(citas_queryset, 5)  # Mostrar 5 citas de mantenimiento por página

        page_number = request.GET.get('page')

        try:
            citas_page = paginator.page(page_number)
        except PageNotAnInteger:
            citas_page = paginator.page(1)
        except EmptyPage:
            citas_page = paginator.page(paginator.num_pages)

        citas_serializer = CitasSerializer(citas_page, many=True)
        citas_data = citas_serializer.data

        return render(request, 'Admin-Citas/citaMantenimiento.html', {'citas': citas_data, 'citas_page': citas_page, 'estados': estados, 'tecnicos': tecnicos, 'cotizaciones':cotizaciones})
    
    def crear_citas(self, request):
        if request.method == 'POST':
            fechacita = request.POST.get('fechacita')
            horacita = request.POST.get('horacita')
            direccioncita = request.POST.get('direccioncita')
            descripcioncita = request.POST.get('descripcioncita')
            idtecnico = request.POST.get('idtecnico')
            idcotizacion = request.POST.get('idcotizacion')
            idestado = request.POST.get('idestadocita')

            estadocita = Estadoscitas.objects.get(idestadocita =idestado )
            tecnico = Tecnicos.objects.get(idtecnico=idtecnico)
            cotizacion = Cotizaciones.objects.get(idcotizacion=idcotizacion)
            numerodocumento = request.user.numerodocumento
            administrador = Administrador.objects.get(numerodocumento = numerodocumento)
            contactocliente = cotizacion.idcliente.numerodocumento.numerocontacto
            
            fechacita = datetime.datetime.strptime(fechacita, '%Y-%m-%d').date()
            horacita = datetime.datetime.strptime(horacita, '%H:%M').time()

            fecha_actual = datetime.datetime.now().date()
            hora_actual = datetime.datetime.now().time()

            if fechacita.weekday() >= 5 or fechacita <= fecha_actual:
                messages.error(request, 'No se pueden programar citas para fines de semana, fechas anteriores, o el mismo dia')
                return redirect('index')

            hora_inicio = datetime.time(7, 0)  # 7:00 am
            hora_fin = datetime.time(17, 0)    # 5:00 pm
            if horacita < hora_inicio or horacita > hora_fin:
                messages.error(request, 'La cita debe programarse entre las 7:00 am y las 5:00 pm.')
                return redirect('index')

            try:
                cita = Citas.objects.create(
                    fechacita=fechacita,
                    horacita=horacita,
                    direccioncita=direccioncita,
                    contactocliente=contactocliente,
                    descripcioncita=descripcioncita,
                    idtecnico=tecnico,
                    idadministrador = administrador,
                    idcotizacion=cotizacion,
                    idestadocita=estadocita
                )
                cliente = cita.idcotizacion.idcliente.idcliente
                messages.success (request,'Se ha registrado exitosamente')
                correo_cita_agendada(request, idcliente=cliente, idtecnico=cita.idtecnico.idtecnico, idcita=cita.idcita)

                return redirect('index')
            except Tecnicos.DoesNotExist:
                messages.error (request,'No se encontro el tecnico seleccionado')
            except Estadoscitas.DoesNotExist:
                messages.error (request,'No se encontró el estado de la cita.')
            except Exception as e:
                messages.error(request, f'Error al intentar crear la cita: {str(e)}')
        else:
            messages.error(request,'Ocurrio un error al intentar registrar la cita, intentalo de nuevo.')
        return redirect('index')

    
    def editar_citas(self, request, idcita):
        cita = Citas.objects.get(idcita=idcita)
        if request.method == 'POST':
            # Obtener los datos de la petición
            fechacita = request.POST.get('fechacita')
            horacita = request.POST.get('horacita')
            direccioncita = request.POST.get('direccioncita')
            descripcioncita = request.POST.get('descripcioncita')
            idtecnico = request.POST.get('idtecnico')
            idcotizacion = request.POST.get('idcotizacion')
            idestadocita = request.POST.get('idestadocita')

            try:
                # Obtener las instancias de Tecnicos, Cotizaciones y Estadoscitas
                tecnico = Tecnicos.objects.get(idtecnico=idtecnico)
                cotizacion = Cotizaciones.objects.get(idcotizacion=idcotizacion)
                estadocita = Estadoscitas.objects.get(idestadocita=idestadocita)
                numerodocumento = request.user.numerodocumento
                administrador = Administrador.objects.get(numerodocumento=numerodocumento)
                contactocliente = cotizacion.idcliente.numerodocumento.numerocontacto

                # Actualizar los campos del objeto cita
                cita.fechacita = fechacita
                cita.horacita = horacita
                cita.direccioncita = direccioncita
                cita.contactocliente = contactocliente
                cita.descripcioncita = descripcioncita
                cita.idtecnico = tecnico
                cita.idadministrador = administrador
                cita.idcotizacion = cotizacion
                cita.idestadocita = estadocita
                cita.save()
                messages.success(request,'Cita editada correctamente')
            except Tecnicos.DoesNotExist:
                messages.error(request,'No se encontró el técnico seleccionado')
            except Estadoscitas.DoesNotExist:
                messages.error(request,'No se encontró el estado de la cita.')
            except Exception as e:
                messages.error(request, f'Error al intentar editar la cita: {str(e)}')
        
        contexto =  {'cita': cita}
        return render(request, 'index.html', contexto)

    def eliminar_citas(self, request, idcita):
        try:
            cita_a_eliminar = Citas.objects.get(idcita=idcita)
            cita_a_eliminar.delete()
            messages.success(request,'Cita eliminada correctamente')
        except Exception as e:
            messages.error(request, f'Error al intentar eliminar la cita: {str(e)}')
        return redirect('index')