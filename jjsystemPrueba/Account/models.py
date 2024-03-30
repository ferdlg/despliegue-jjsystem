from django.db import models


class Actividadescronogramatecnicos(models.Model):
    idactividadcronogramatecnico = models.AutoField(db_column='idActividadCronogramaTecnico', primary_key=True)  # Field name made lowercase.
    nombreactividad = models.CharField(db_column='nombreActividad', max_length=30)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'actividadescronogramatecnicos'


class Administrador(models.Model):
    idadministrador = models.AutoField(db_column='idAdministrador', primary_key=True)  # Field name made lowercase.
    numerodocumento = models.ForeignKey('Usuarios', models.CASCADE, db_column='numeroDocumento')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'administrador'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Categoriasproductos(models.Model):
    idcategoriaproducto = models.AutoField(db_column='idCategoriaProducto', primary_key=True)  # Field name made lowercase.
    nombrecategoria = models.CharField(db_column='nombreCategoria', max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'categoriasproductos'


class Categoriasservicios(models.Model):
    idcategoriaservicio = models.AutoField(db_column='idCategoriaServicio', primary_key=True)  # Field name made lowercase.
    nombrecategoria = models.CharField(db_column='nombreCategoria', max_length=30, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'categoriasservicios'


class Citas(models.Model):
    idcita = models.AutoField(db_column='idCita', primary_key=True)  # Field name made lowercase.
    fechacita = models.DateField(db_column='fechaCita') 
    horacita = models.TimeField(db_column='horaCita')
    direccioncita = models.CharField(db_column='direccionCita', max_length=50)  # Field name made lowercase.
    contactocliente = models.BigIntegerField(db_column='contactoCliente')  # Field name made lowercase.
    descripcioncita = models.TextField(db_column='descripcionCita')  # Field name made lowercase.
    idtecnico = models.ForeignKey('Tecnicos', models.DO_NOTHING, db_column='idTecnico')  # Field name made lowercase.
    idadministrador = models.ForeignKey(Administrador, models.DO_NOTHING, db_column='idAdministrador')  # Field name made lowercase.
    idcotizacion = models.ForeignKey('Cotizaciones', models.DO_NOTHING, db_column='idCotizacion')  # Field name made lowercase.
    idestadocita = models.ForeignKey('Estadoscitas', models.DO_NOTHING, db_column='idEstadoCita')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'citas'


class Clientes(models.Model):
    idcliente = models.AutoField(db_column='idCliente', primary_key=True)  # Field name made lowercase.
    direccioncliente = models.CharField(db_column='direccionCliente', max_length=50)  # Field name made lowercase.
    numerodocumento = models.ForeignKey('Usuarios', models.CASCADE, db_column='numeroDocumento')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'clientes'


class Cotizaciones(models.Model):
    idcotizacion = models.AutoField(db_column='idCotizacion', primary_key=True)  # Field name made lowercase.
    fechacotizacion = models.DateField(db_column='fechaCotizacion', auto_now_add=True)
    totalcotizacion = models.FloatField(db_column='totalCotizacion')  # Field name made lowercase.
    descripcioncotizacion = models.TextField(db_column='descripcionCotizacion')  # Field name made lowercase.
    idcliente = models.ForeignKey(Clientes, models.DO_NOTHING, db_column='idCliente')  # Field name made lowercase.
    idestadocotizacion = models.ForeignKey('Estadoscotizaciones', models.DO_NOTHING, db_column='idEstadoCotizacion')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'cotizaciones'

class Productos(models.Model):
    idproducto = models.AutoField(db_column='idProducto', primary_key=True)  # Field name made lowercase.
    nombreproducto = models.TextField(db_column='nombreProducto')  # Field name made lowercase.
    descripcionproducto = models.TextField(db_column='descripcionProducto')  # Field name made lowercase.
    precioproducto = models.FloatField(db_column='precioProducto')  # Field name made lowercase.
    cantidad = models.IntegerField()
    imagen = models.BinaryField(blank=True, null=True)
    idadministrador = models.ForeignKey(Administrador, models.DO_NOTHING, db_column='idAdministrador', blank=True, null=True)  # Field name made lowercase.
    idcategoriaproducto = models.ForeignKey(Categoriasproductos, models.DO_NOTHING, db_column='idCategoriaProducto', blank=True, null=True)  # Field name made lowercase.
    idproveedorproducto = models.ForeignKey('Proveedoresproductos', models.DO_NOTHING, db_column='idProveedorProducto', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'productos'

class CotizacionesProductos(models.Model):
    idcotizacion = models.ForeignKey(Cotizaciones, models.DO_NOTHING, db_column='idCotizacion', blank=True, null=True)  # Field name made lowercase.
    idproducto = models.ForeignKey(Productos, models.DO_NOTHING, db_column='idProducto', blank=True, null=True)  # Field name made lowercase.
    cantidad = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cotizaciones_productos'


class CotizacionesServicios(models.Model):
    idcotizacion = models.ForeignKey(Cotizaciones, models.DO_NOTHING, db_column='idCotizacion', blank=True, null=True)  # Field name made lowercase.
    idservicio = models.ForeignKey('Servicios', models.DO_NOTHING, db_column='idServicio', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'cotizaciones_servicios'


class Cronogramatecnicos(models.Model):
    idcronogramatecnico = models.AutoField(db_column='idCronogramaTecnico', primary_key=True)  # Field name made lowercase.
    idtecnico = models.ForeignKey('Tecnicos', models.CASCADE, db_column='idTecnico', blank=True, null=True)  # Field name made lowercase.
    idcita = models.ForeignKey(Citas, models.CASCADE, db_column='idCita', blank=True, null=True)  # Field name made lowercase.
    iddisponibilidadcronograma = models.ForeignKey('Disponibilidadcronogramas', models.DO_NOTHING, db_column='idDisponibilidadCronograma', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'cronogramatecnicos'


class DetalleEnviosVentas(models.Model):
    idenvio = models.IntegerField(primary_key=True)
    direccionenvio = models.CharField(max_length=255, blank=True, null=True)
    detallesventa = models.CharField(max_length=255, blank=True, null=True)
    tecnicoasignado = models.IntegerField(blank=True, null=True)
    nombretecnico = models.CharField(max_length=255, blank=True, null=True)
    numerodocumento = models.CharField(max_length=255, blank=True, null=True)
    fechaventa = models.DateField(blank=True, null=True)
    idventa = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'detalle_envios_y_ventas'


class Detallesactividadcronograma(models.Model):
    iddetalleactividad = models.AutoField(db_column='idDetalleActividad', primary_key=True)  # Field name made lowercase.
    idcronogramatecnico = models.ForeignKey(Cronogramatecnicos, models.DO_NOTHING, db_column='idCronogramaTecnico', blank=True, null=True)  # Field name made lowercase.
    idactividadcronogramatecnico = models.ForeignKey(Actividadescronogramatecnicos, models.DO_NOTHING, db_column='idActividadCronogramaTecnico', blank=True, null=True)  # Field name made lowercase.
    fechaactividadcronograma = models.DateTimeField(db_column='fechaActividadCronograma')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'detallesactividadcronograma'


class Detallesventas(models.Model):
    iddetalleventa = models.AutoField(db_column='idDetalleVenta', primary_key=True)  # Field name made lowercase.
    detallesventa = models.CharField(db_column='detallesVenta', max_length=300)  # Field name made lowercase.
    subtotalventa = models.FloatField(db_column='subtotalVenta')  # Field name made lowercase.
    totalventa = models.FloatField(db_column='totalVenta')  # Field name made lowercase.
    idventa = models.ForeignKey('Ventas', models.DO_NOTHING, db_column='idVenta')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'detallesventas'


class Disponibilidadcronogramas(models.Model):
    iddisponibilidadcronograma = models.AutoField(db_column='idDisponibilidadCronograma', primary_key=True)  # Field name made lowercase.
    nombredisponibilidad = models.CharField(db_column='nombreDisponibilidad', max_length=30)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'disponibilidadcronogramas'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Envios(models.Model):
    idenvio = models.AutoField(db_column='idEnvio', primary_key=True)  # Field name made lowercase.
    direccionenvio = models.CharField(db_column='direccionEnvio', max_length=50)  # Field name made lowercase.
    idtecnico = models.ForeignKey('Tecnicos', models.DO_NOTHING, db_column='idTecnico', blank=True, null=True)  # Field name made lowercase.
    idestadoenvio = models.ForeignKey('Estadosenvios', models.DO_NOTHING, db_column='idEstadoEnvio', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'envios'


class Enviosentregados(models.Model):
    idenvio = models.IntegerField(db_column='idEnvio', primary_key=True)  # Field name made lowercase.
    fecha = models.DateTimeField(blank=True, null=True)
    idtecnicoencargado = models.IntegerField(db_column='idTecnicoEncargado', blank=True, null=True)  # Field name made lowercase.
    documentotecnico = models.BigIntegerField(db_column='documentoTecnico', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'enviosentregados'


class Estadoscitas(models.Model):
    idestadocita = models.AutoField(db_column='idEstadoCita', primary_key=True)  # Field name made lowercase.
    nombreestadocita = models.CharField(db_column='nombreEstadoCita', max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'estadoscitas'


class Estadoscotizaciones(models.Model):
    idestadocotizacion = models.AutoField(db_column='idEstadoCotizacion', primary_key=True)  # Field name made lowercase.
    nombreestadocotizacion = models.CharField(db_column='nombreEstadoCotizacion', max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'estadoscotizaciones'


class Estadosenvios(models.Model):
    idestadoenvio = models.AutoField(db_column='idEstadoEnvio', primary_key=True)  # Field name made lowercase.
    nombreestadoenvio = models.CharField(db_column='nombreEstadoEnvio', max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'estadosenvios'


class Estadospqrsf(models.Model):
    idestadopqrsf = models.AutoField(db_column='idEstadoPQRSF', primary_key=True)  # Field name made lowercase.
    nombreestadopqrsf = models.CharField(db_column='nombreEstadoPQRSF', max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'estadospqrsf'


class Estadosusuarios(models.Model):
    idestadousuario = models.AutoField(db_column='idEstadoUsuario', primary_key=True)  # Field name made lowercase.
    nombreestadousuario = models.CharField(db_column='nombreEstadoUsuario', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'estadosusuarios'


class Historialcotizaciones(models.Model):
    idcotizacion = models.ForeignKey(Cotizaciones, models.DO_NOTHING, db_column='idCotizacion', blank=True, null=True)  # Field name made lowercase.
    fechacreada = models.DateTimeField(db_column='fechaCreada', blank=True, null=True)  # Field name made lowercase.
    fechaactualizacion = models.DateTimeField(db_column='fechaActualizacion', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'historialcotizaciones'


class Historialpqrsfportipoestado(models.Model):
    idregistro = models.AutoField(db_column='idRegistro', primary_key=True)  # Field name made lowercase.
    idpqrsf = models.ForeignKey('Pqrsf', models.DO_NOTHING, db_column='idPQRSF', blank=True, null=True)  # Field name made lowercase.
    idtipopqrsf = models.IntegerField(db_column='idTipoPQRSF', blank=True, null=True)  # Field name made lowercase.
    idestadopqrsf = models.IntegerField(db_column='idEstadoPQRSF', blank=True, null=True)  # Field name made lowercase.
    fecharegistro = models.DateTimeField(db_column='fechaRegistro', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'historialpqrsfportipoestado'


class Permisos(models.Model):
    idpermiso = models.AutoField(db_column='idPermiso', primary_key=True)  # Field name made lowercase.
    nombrepermiso = models.CharField(db_column='nombrePermiso', max_length=20, blank=True, null=True)  # Field name made lowercase.
    idrol = models.ForeignKey('Roles', models.DO_NOTHING, db_column='idRol', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'permisos'


class Pqrsf(models.Model):
    idpqrsf = models.AutoField(db_column='idPQRSF', primary_key=True)  # Field name made lowercase.
    fechapqrsf = models.DateField(db_column='fechaPQRSF',  auto_now_add=True)  # Field name made lowercase.
    informacionpqrsf = models.TextField(db_column='informacionPQRSF')  # Field name made lowercase.
    idcliente = models.ForeignKey(Clientes, models.DO_NOTHING, db_column='idCliente')  # Field name made lowercase.
    idtipopqrsf = models.ForeignKey('Tipospqrsf', models.DO_NOTHING, db_column='idTipoPQRSF')  # Field name made lowercase.
    idestadopqrsf = models.ForeignKey(Estadospqrsf, models.DO_NOTHING, db_column='idEstadoPQRSF')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'pqrsf'

class Proveedoresproductos(models.Model):
    idproveedorproducto = models.AutoField(db_column='idProveedorProducto', primary_key=True)  # Field name made lowercase.
    nombreproveedor = models.CharField(db_column='nombreProveedor', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'proveedoresproductos'


class Respuestas(models.Model):
    idrespuesta = models.AutoField(db_column='idRespuesta', primary_key=True)  # Field name made lowercase.
    fecha = models.DateField(blank=True, null=True)
    informacionrespuesta = models.TextField(db_column='informacionRespuesta', blank=True, null=True)  # Field name made lowercase.
    idadministrador = models.ForeignKey(Administrador, models.DO_NOTHING, db_column='idAdministrador', blank=True, null=True)  # Field name made lowercase.
    idpqrsf = models.ForeignKey(Pqrsf, models.DO_NOTHING, db_column='idPQRSF', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'respuestas'


class Roles(models.Model):
    idrol = models.AutoField(db_column='idRol', primary_key=True)  # Field name made lowercase.
    nombrerol = models.CharField(db_column='nombreRol', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'roles'


class RolesHasPermisos(models.Model):
    idrol = models.ForeignKey(Roles, models.DO_NOTHING, db_column='idRol', blank=True, null=True)  # Field name made lowercase.
    idpermiso = models.ForeignKey(Permisos, models.DO_NOTHING, db_column='idPermiso', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'roles_has_permisos'


class Servicios(models.Model):
    idservicio = models.AutoField(db_column='idServicio', primary_key=True)  # Field name made lowercase.
    nombreservicio = models.TextField(db_column='nombreServicio')  # Field name made lowercase.
    descripcionservicio = models.TextField(db_column='descripcionServicio')  # Field name made lowercase.
    precioservicio = models.FloatField(db_column='precioServicio', blank=True, null=True)  # Field name made lowercase.
    idcategoriaservicio = models.ForeignKey(Categoriasservicios, models.DO_NOTHING, db_column='idCategoriaServicio', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'servicios'


class Especialidadtecnicos(models.Model):
    id_especialidad = models.AutoField(primary_key=True)
    nombre_especialidad = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre_especialidad

    class Meta:
        managed = False
        db_table = 'Especialidad_tecnicos'

class Tecnicos(models.Model):
    idtecnico = models.AutoField(primary_key=True)
    id_especialidad_fk = models.ForeignKey('Especialidadtecnicos', models.DO_NOTHING, db_column='id_especialidad_fk')
    numerodocumento = models.ForeignKey('Usuarios', models.CASCADE, db_column='numeroDocumento')

    def __str__(self):
        return str(self.idtecnico)

    class Meta:
        managed = False
        db_table = 'Tecnicos'

class Tipospqrsf(models.Model):
    idtipopqrsf = models.AutoField(db_column='idTipoPQRSF', primary_key=True)  # Field name made lowercase.
    nombretipopqrsf = models.CharField(db_column='nombreTipoPQRSF', max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tipospqrsf'


class Usuarios(models.Model):
    numerodocumento = models.BigIntegerField(db_column='numeroDocumento', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=50, blank=True, null=True)
    apellido = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=120, blank=True, null=True)
    password = models.CharField(max_length=200, blank=True, null=True)
    numerocontacto = models.FloatField(db_column='numeroContacto', blank=True, null=True)  # Field name made lowercase.
    idrol = models.ForeignKey(Roles, models.DO_NOTHING, db_column='idRol')  # Field name made lowercase.
    idestadosusuarios = models.ForeignKey(Estadosusuarios, models.DO_NOTHING, db_column='idEstadosUsuarios')  # Field name made lowercase.
    last_login = models.DateTimeField(null=True, blank=True)

    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True

    @classmethod
    def get_email_field_name(cls):
        return 'email'

    class Meta:
        managed = False
        db_table = 'usuarios'

class Ventas(models.Model):
    idventa = models.AutoField(db_column='idVenta', primary_key=True)  # Field name made lowercase.
    fechaventa = models.DateField(db_column='fechaVenta')  # Field name made lowercase.
    idenvio = models.ForeignKey(Envios, models.DO_NOTHING, db_column='idEnvio')  # Field name made lowercase.
    idcotizacion = models.ForeignKey(Cotizaciones, models.DO_NOTHING, db_column='idCotizacion')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ventas'

class EnviosClientes(models.Model):
    idenvio = models.IntegerField(primary_key=True)
    direccionenvio = models.CharField(max_length=100)
    idtecnico = models.IntegerField()
    nombreestadoenvio = models.CharField(max_length=100)
    idcliente = models.IntegerField()
    direccioncliente = models.CharField(max_length=100)
    documentocliente = models.IntegerField()

    class Meta:
        managed = False  
        db_table = 'vistaenviosclientes'

