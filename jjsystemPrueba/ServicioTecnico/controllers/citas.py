from django.shortcuts import render, redirect
from rest_framework import viewsets
from Account.models import Citas , Servicios, Cotizaciones, Categoriasservicios, Tecnicos, Administrador , Estadoscitas
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
        estados = Estadoscitas.objects.all()
        tecnico = Tecnicos.objects.all()
        if request.method == 'POST':
            fechacita = request.POST.get('fechacita')
            horacita = request.POST.get('horacita')
            direccioncita = request.POST.get('direccioncita')
            contactocliente = request.POST.get('contactocliente')
            descripcioncita = request.POST.get('descripcioncita')
            idtecnico = request.POST.get('idtecnico')
            idadministrador = request.POST.get('idadministrador')
            idcotizacion = request.POST.get('idcotizacion')
            idestadocita = request.POST.get('idestadocita')
            try:
                idtecnico = int(idtecnico)
                tecnico = Tecnicos.objects.get(idtecnico=idtecnico)
                idadministrador = int(idadministrador)
                administrador = Administrador.objects.get(idadministrador=idadministrador)
                idcotizacion = int(idcotizacion)
                cotizacion = Cotizaciones.objects.get(idcotizacion=idcotizacion)
                idestadocita = int(idestadocita)
                estadocita = Estadoscitas.objects.get(idestadocita=idestadocita)
                # Crear la instancia de la cita
                cita = Citas.objects.create(
                    fechacita=fechacita,
                    horacita = horacita,
                    direccioncita=direccioncita,
                    contactocliente=contactocliente,
                    descripcioncita=descripcioncita,
                    idtecnico=tecnico,
                    idadministrador=administrador,
                    idcotizacion=cotizacion,
                    idestadocita=estadocita
                )

                return redirect('cita_analisis')

            except Tecnicos.DoesNotExist:
                print("Error: No se encontró el Técnico.")
            except Estadoscitas.DoesNotExist:
                print("Error: No se encontró el estado de la cita.")

    

        return render(request, 'Admin-Citas/citaAnalisis.html', {'estados': estados , 'tecnico':tecnico})
        
    
    def editar_citas(request, idcita):
        cita = Citas.objects.get(idcita=idcita)
        estados = Estadoscitas.objects.all()
        tecnicos = Tecnicos.objects.all()

        if request.method == 'POST':
            # Obtener los datos de la petición
            fechacita = request.POST.get('fechacita')
            horacita = request.POST.get('horacita')
            direccioncita = request.POST.get('direccioncita')
            contactocliente = request.POST.get('contactocliente')
            descripcioncita = request.POST.get('descripcioncita')
            idtecnico = int(request.POST.get('idtecnico'))
            idadministrador = int(request.POST.get('idadministrador'))
            idcotizacion = int(request.POST.get('idcotizacion'))
            idestadocita = int(request.POST.get('idestadocita'))

            # Obtener las instancias de Tecnicos, Administrador, Cotizaciones y Estadoscitas
            idtecnico = Tecnicos.objects.get(idtecnico=idtecnico)
            idadministrador = Administrador.objects.get(idadministrador=idadministrador)
            idcotizacion = Cotizaciones.objects.get(idcotizacion=idcotizacion)
            idestadocita = Estadoscitas.objects.get(idestadocita=idestadocita)

            # Actualizar los campos del objeto cita
            cita.fechacita = fechacita
            cita.horacita = horacita
            cita.direccioncita = direccioncita
            cita.contactocliente = contactocliente
            cita.descripcioncita = descripcioncita
            cita.idtecnico = idtecnico
            cita.idadministrador = idadministrador
            cita.idcotizacion = idcotizacion
            cita.idestadocita = idestadocita
            cita.save()

            return redirect('index')  

        return render(request,'Templates/Admin-Citas/EditarCitas.html', {"citas": cita , "tecnicos":tecnicos , "estados":estados})

    def eliminar_citas(self, request, idcita):
        cita_eliminada = Citas.objects.delete(idcita = idcita)
        cita_eliminada.delete()
        return render('index')