from django.shortcuts import render, redirect
from rest_framework import viewsets
from Account.models import Citas , Cotizaciones, Tecnicos, Administrador , Estadoscitas, Usuarios
from .serializers import CitasSerializer
from django.core.paginator import Paginator , EmptyPage , PageNotAnInteger



class citasCRUD(viewsets.ModelViewSet):
    queryset = Citas.objects.all()
    serializer_class = CitasSerializer

    #Metodo para obtener solo las citas de analisis
    def cita_analisis(self, request):
        
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
        return render(request, 'Admin-Citas/citaAnalisis.html', {'citas': citas_data, 'citas_page': citas_page})
    #Metodo para obtener solo las citas de instalacion
    def cita_instalacion(self, request):
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
        return render(request, 'Admin-Citas/citaInstalacion.html', {'citas': citas_data, 'citas_page': citas_page})
    
    def cita_mantenimiento(self, request):
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

        return render(request, 'Admin-Citas/citaMantenimiento.html', {'citas': citas_data, 'citas_page': citas_page})
    
    def crear_citas(self, request):
        if request.method == 'POST':
            fechacita = request.POST.get('fechacita')
            horacita = request.POST.get('horacita')
            direccioncita = request.POST.get('direccioncita')
            descripcioncita = request.POST.get('descripcioncita')
            idtecnico = request.POST.get('idtecnico')
            idcotizacion = request.POST.get('idcotizacion')
            idestadocita = request.POST.get('idestadocita')
            
            try:
                tecnico = Tecnicos.objects.get(idtecnico=idtecnico)
                cotizacion = Cotizaciones.objects.get(idcotizacion=idcotizacion)
                numerodocumento = request.user.numerodocumento
                administrador = Administrador.objects.get(numerodocumento = numerodocumento)
                estadocita = Estadoscitas.objects.get(idestadocita=idestadocita)
                contactocliente = cotizacion.idcliente.numerodocumento.numerocontacto

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
                
                return redirect('cita_analisis')

            except Tecnicos.DoesNotExist:
                # Mensaje de error para el usuario
                mensaje = ('No se encontro el tecnico seleccionado')
                return render( request, 'mensaje.html', {'mensaje':mensaje})
            except Estadoscitas.DoesNotExist:
                # Mensaje de error para el usuario
                mensaje = ('No se encontró el estado de la cita.')
                return render( request, 'mensaje.html', {'mensaje':mensaje})

        return redirect('cita_analisis')

    
    def editar_citas(self, request, idcita):
        cita = Citas.objects.get(idcita=idcita)
        estados = Estadoscitas.objects.all()
        tecnicos = Tecnicos.objects.all()

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

                return redirect('index')

            except Tecnicos.DoesNotExist:
                # Mensaje de error para el usuario
                mensaje = 'No se encontró el técnico seleccionado'
                return render(request, 'mensaje.html', {'mensaje': mensaje})
            except Estadoscitas.DoesNotExist:
                # Mensaje de error para el usuario
                mensaje = 'No se encontró el estado de la cita.'
                return render(request, 'mensaje.html', {'mensaje': mensaje})

        return render(request, 'editar_citas.html', {'cita': cita, 'estados': estados, 'tecnicos': tecnicos})

    def eliminar_citas(self, request, idcita):
        cita_eliminada = Citas.objects.delete(idcita = idcita)
        cita_eliminada.delete()
        return render('index')