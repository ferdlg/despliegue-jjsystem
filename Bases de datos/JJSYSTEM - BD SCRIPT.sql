DROP DATABASE IF EXISTS jjsystem_db;
CREATE DATABASE jjsystem_db;
USE jjsystem_db;

CREATE TABLE IF NOT EXISTS Roles(
    idRol INT NOT NULL AUTO_INCREMENT,
    nombreRol VARCHAR(20),
    PRIMARY KEY (idRol)
);

CREATE TABLE IF NOT EXISTS Permisos(
   idPermiso INT NOT NULL AUTO_INCREMENT,
   nombrePermiso VARCHAR(20),
   idRol INT,
   PRIMARY KEY (idPermiso),
   FOREIGN KEY (idRol) REFERENCES Roles (idRol)
);

CREATE TABLE IF NOT EXISTS Roles_has_Permisos(
   idRol INT,
   idPermiso INT,
   FOREIGN KEY (idRol) REFERENCES Roles (idRol),
   FOREIGN KEY (idPermiso) REFERENCES Permisos (idPermiso)
);

CREATE TABLE IF NOT EXISTS EstadosUsuarios(
    idEstadoUsuario INT NOT NULL AUTO_INCREMENT,
    nombreEstadoUsuario VARCHAR(50) NOT NULL,
    PRIMARY KEY (idEstadoUsuario)
);

CREATE TABLE IF NOT EXISTS Usuarios(
    numeroDocumento BIGINT NOT NULL,
    nombre VARCHAR(50) DEFAULT NULL,
    apellido VARCHAR(50) DEFAULT NULL,
    email VARCHAR(120) DEFAULT NULL,
    password VARCHAR(200) DEFAULT NULL,
    numeroContacto FLOAT DEFAULT NULL,
    idRol INT NOT NULL,
    idEstadosUsuarios INT NOT NULL,
    last_login DATETIME NULL,
    PRIMARY KEY (numeroDocumento),
    FOREIGN KEY (idRol) REFERENCES Roles (idRol),
    FOREIGN KEY (idEstadosUsuarios) REFERENCES EstadosUsuarios (idEstadoUsuario)
);

CREATE TABLE IF NOT EXISTS Clientes(
    idCliente INT NOT NULL AUTO_INCREMENT,
    direccionCliente VARCHAR(50)  NULL,
    numeroDocumento BIGINT NOT NULL,
    PRIMARY KEY (idCliente),
    FOREIGN KEY (numeroDocumento) REFERENCES Usuarios (numeroDocumento)
);

CREATE TABLE IF NOT EXISTS Administrador(
    idAdministrador INT NOT NULL AUTO_INCREMENT,
    numeroDocumento BIGINT NOT NULL,
    PRIMARY KEY (idAdministrador),
    FOREIGN KEY (numeroDocumento) REFERENCES Usuarios (numeroDocumento)
);
CREATE TABLE IF NOT EXISTS Especialidad_tecnicos(
	id_especialidad int AUTO_INCREMENT primary key,
    nombre_especialidad VARCHAR(50)
);
CREATE TABLE IF NOT EXISTS Tecnicos (
    idTecnico INT NOT NULL AUTO_INCREMENT,
    id_especialidad_fk int NOT NULL,
    numeroDocumento BIGINT NOT NULL,
    PRIMARY KEY (idTecnico),
	FOREIGN KEY (id_especialidad_fk) REFERENCES Especialidad_tecnicos (id_especialidad),
    FOREIGN KEY (numeroDocumento) REFERENCES Usuarios (numeroDocumento)
);

CREATE TABLE IF NOT EXISTS EstadosEnvios(
    idEstadoEnvio INT NOT NULL AUTO_INCREMENT,
    nombreEstadoEnvio VARCHAR(20) NOT NULL,
    PRIMARY KEY (idEstadoEnvio)
);

CREATE TABLE IF NOT EXISTS Envios (
    idEnvio INT NOT NULL AUTO_INCREMENT,
    direccionEnvio VARCHAR(50) NOT NULL,
    idTecnico INT,
    idEstadoEnvio INT,
    PRIMARY KEY (idEnvio),
    FOREIGN KEY (idTecnico) REFERENCES Tecnicos (idTecnico),
    FOREIGN KEY (idEstadoEnvio) REFERENCES EstadosEnvios (idEstadoEnvio)
);

CREATE TABLE IF NOT EXISTS categoriasProductos(
    idCategoriaProducto INT NOT NULL AUTO_INCREMENT,
    nombreCategoria VARCHAR(20) NOT NULL,
    PRIMARY KEY(idCategoriaProducto)
);

CREATE TABLE IF NOT EXISTS proveedoresProductos(
    idProveedorProducto INT NOT NULL AUTO_INCREMENT,
    nombreProveedor VARCHAR(50) NOT NULL,
    PRIMARY KEY (idProveedorProducto)
);

CREATE TABLE IF NOT EXISTS Productos(
    idProducto INT NOT NULL AUTO_INCREMENT,
    nombreProducto TEXT(100) NOT NULL,
    descripcionProducto TEXT(200) NOT NULL,
    precioProducto FLOAT NOT NULL,
    cantidad INT NOT NULL,
    imagen VARCHAR(200) NULL,
    idAdministrador INT,
    idCategoriaProducto INT,
    idProveedorProducto INT,
    PRIMARY KEY(idProducto),
    FOREIGN KEY(idAdministrador) REFERENCES Administrador (idAdministrador),
    FOREIGN KEY(idCategoriaProducto) REFERENCES categoriasProductos (idCategoriaProducto),
    FOREIGN KEY(idProveedorProducto) REFERENCES proveedoresProductos (idProveedorProducto)
);

CREATE TABLE IF NOT EXISTS categoriasServicios(
    idCategoriaServicio INT NOT NULL AUTO_INCREMENT,
    nombreCategoria VARCHAR(30),
    PRIMARY KEY(idCategoriaServicio)
);

CREATE TABLE IF NOT EXISTS Servicios(
    idServicio INT NOT NULL AUTO_INCREMENT,
    nombreServicio TEXT(100) NOT NULL,
    descripcionServicio TEXT(200) NOT NULL,
    precioServicio FLOAT, 
    idCategoriaServicio INT,
    PRIMARY KEY (idServicio),
    FOREIGN KEY (idCategoriaServicio) REFERENCES categoriasServicios (idCategoriaServicio)
);

CREATE TABLE IF NOT EXISTS EstadosCotizaciones(
    idEstadoCotizacion INT NOT NULL AUTO_INCREMENT,
    nombreEstadoCotizacion VARCHAR(20) NOT NULL,
    PRIMARY KEY (idEstadoCotizacion)
);

CREATE TABLE IF NOT EXISTS Cotizaciones(
    idCotizacion INT NOT NULL AUTO_INCREMENT,
    fechaCotizacion DATE NOT NULL,
    totalCotizacion FLOAT NOT NULL,
    descripcionCotizacion TEXT(200) NOT NULL,
    idCliente INT NOT NULL,
    idEstadoCotizacion INT NOT NULL,
    PRIMARY KEY (idCotizacion),
    FOREIGN KEY (idCliente) REFERENCES Clientes (idCliente),
    FOREIGN KEY (idEstadoCotizacion) REFERENCES EstadosCotizaciones (idEstadoCotizacion)
);

CREATE TABLE IF NOT EXISTS Cotizaciones_Productos(
    idCotizacion INT,
    idProducto INT,
    cantidad INT,
    FOREIGN KEY (idCotizacion) REFERENCES Cotizaciones (idCotizacion),
    FOREIGN KEY (idProducto) REFERENCES Productos (idProducto)
);

CREATE TABLE IF NOT EXISTS Cotizaciones_Servicios(
    idCotizacion INT,
    idServicio INT,
    FOREIGN KEY (idCotizacion) REFERENCES Cotizaciones (idCotizacion),
    FOREIGN KEY (idServicio) REFERENCES Servicios (idServicio)
);

CREATE TABLE IF NOT EXISTS EstadosCitas(
    idEstadoCita INT NOT NULL AUTO_INCREMENT, 
    nombreEstadoCita VARCHAR(20) NOT NULL, 
    PRIMARY KEY (idEstadoCita)
);

CREATE TABLE IF NOT EXISTS Citas(
    idCita INT NOT NULL AUTO_INCREMENT,
    fechaCita DATE NOT NULL,
    direccionCita VARCHAR(50) NOT NULL,
    contactoCliente BIGINT NOT NULL,
    descripcionCita TEXT(200) NOT NULL,
    idTecnico INT NOT NULL,
    idAdministrador INT NOT NULL,
    idCotizacion INT NOT NULL,
    idEstadoCita INT NOT NULL,
    PRIMARY KEY (idCita),
    FOREIGN KEY (idTecnico) REFERENCES Tecnicos (idTecnico),
    FOREIGN KEY (idAdministrador) REFERENCES Administrador (idAdministrador),
    FOREIGN KEY (idCotizacion) REFERENCES Cotizaciones (idCotizacion),
    FOREIGN KEY (idEstadoCita) REFERENCES EstadosCitas (idEstadoCita)
);

CREATE TABLE IF NOT EXISTS DisponibilidadCronogramas(
    idDisponibilidadCronograma INT NOT NULL AUTO_INCREMENT,
    nombreDisponibilidad VARCHAR(30) NOT NULL,
    PRIMARY KEY (idDisponibilidadCronograma)
);

CREATE TABLE IF NOT EXISTS CronogramaTecnicos(
    idCronogramaTecnico INT NOT NULL AUTO_INCREMENT,
    idTecnico INT,
    idCita INT,
    idDisponibilidadCronograma INT,
    PRIMARY KEY (idCronogramaTecnico),
    FOREIGN KEY (idTecnico) REFERENCES Tecnicos (idTecnico), 
    FOREIGN KEY (idCita) REFERENCES Citas (idCita),
    FOREIGN KEY (idDisponibilidadCronograma) REFERENCES DisponibilidadCronogramas (idDisponibilidadCronograma)
);

CREATE TABLE IF NOT EXISTS ActividadesCronogramaTecnicos(
    idActividadCronogramaTecnico INT NOT NULL AUTO_INCREMENT,
    nombreActividad VARCHAR(30) NOT NULL,
    PRIMARY KEY (idActividadCronogramaTecnico)
);

CREATE TABLE IF NOT EXISTS DetallesActividadCronograma(
    idDetalleActividad INT NOT NULL AUTO_INCREMENT,
    idCronogramaTecnico INT,
    idActividadCronogramaTecnico INT,
    fechaActividadCronograma DATETIME NOT NULL,
    PRIMARY KEY(idDetalleActividad),
    FOREIGN KEY (idCronogramaTecnico) REFERENCES CronogramaTecnicos (idCronogramaTecnico),
    FOREIGN KEY (idActividadCronogramaTecnico) REFERENCES ActividadesCronogramaTecnicos (idActividadCronogramaTecnico)
);

CREATE TABLE IF NOT EXISTS Ventas(
    idVenta INT NOT NULL AUTO_INCREMENT,
    fechaVenta DATE NOT NULL,
    idEnvio INT NOT NULL,
    idCotizacion INT NOT NULL,
    PRIMARY KEY(idVenta),
    FOREIGN KEY(idEnvio) REFERENCES Envios (idEnvio),
    FOREIGN KEY(idCotizacion) REFERENCES Cotizaciones (idCotizacion)
);

CREATE TABLE IF NOT EXISTS DetallesVentas(
    idDetalleVenta INT NOT NULL AUTO_INCREMENT,
    detallesVenta VARCHAR(300) NOT NULL,
    subtotalVenta FLOAT NOT NULL,
    totalVenta FLOAT NOT NULL,
    idVenta INT NOT NULL,
    PRIMARY KEY (idDetalleVenta),
    FOREIGN KEY (idVenta) REFERENCES Ventas (idVenta)
);

CREATE TABLE IF NOT EXISTS TiposPQRSF(
    idTipoPQRSF INT NOT NULL AUTO_INCREMENT,
    nombreTipoPQRSF VARCHAR (20) NOT NULL,
    PRIMARY KEY (idTipoPQRSF)
);

CREATE TABLE IF NOT EXISTS EstadosPQRSF( 
    idEstadoPQRSF INT NOT NULL AUTO_INCREMENT,
    nombreEstadoPQRSF VARCHAR (20) NOT NULL,
    PRIMARY KEY (idEstadoPQRSF)
);

CREATE TABLE IF NOT EXISTS PQRSF(
    idPQRSF INT NOT NULL AUTO_INCREMENT,
    fechaPQRSF DATE NOT NULL,
    informacionPQRSF TEXT(200) NOT NULL,
    idCliente INT NOT NULL,
    idTipoPQRSF INT NOT NULL,
    idEstadoPQRSF INT NOT NULL,
    PRIMARY KEY (idPQRSF),
    FOREIGN KEY (idCliente) REFERENCES Clientes (idCliente),
    FOREIGN KEY (idTipoPQRSF) REFERENCES TiposPQRSF (idTipoPQRSF),
    FOREIGN KEY (idEstadoPQRSF) REFERENCES EstadosPQRSF (idEstadoPQRSF)
);

CREATE TABLE IF NOT EXISTS Respuestas (
    idRespuesta INT NOT NULL AUTO_INCREMENT,
    fecha DATE NULL,
    informacionRespuesta TEXT(200) NULL,
    idAdministrador INT NULL,
    idPQRSF INT NULL,
    PRIMARY KEY (idRespuesta),
    FOREIGN KEY (idAdministrador) REFERENCES Administrador (idAdministrador),
    FOREIGN KEY (idPQRSF) REFERENCES PQRSF (idPQRSF)
);

CREATE TABLE IF NOT EXISTS historialCotizaciones (
    idCotizacion int,
    fechaCreada datetime DEFAULT CURRENT_TIMESTAMP, 
    fechaActualizacion datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    foreign key(idCotizacion) references Cotizaciones (idCotizacion)
);
CREATE TABLE detalle_envios_ventas (
    idenvio INT PRIMARY KEY,
    direccionenvio VARCHAR(255),
    detallesventa VARCHAR(255),
    tecnicoasignado INT,
    numerodocumento VARCHAR(255),
    fechaventa DATE
);



INSERT INTO ROLES (idRol, nombreRol) 
VALUES
	(1, "Gerente"),
    (2, "Cliente"),
    (3, "Tecnico");
    
-- Inserción de permisos
INSERT INTO PERMISOS (nombrePermiso, idRol) 
VALUES
	('agregarProducto', 1),
    ('modificarProducto', 1),
    ('eliminarProducto', 1),
    ('agregarServicio', 1),
    ('modificarServicio', 1),
    ('eliminarServicio', 1),
    ('consultarCotizacion', 1),
    ('consultarVenta', 1),
    ('confirmarCita', 1),
    ('modificarCita', 1),
    ('cancelarCita', 1),
    ('asignarCita', 1),
    ('asignarActividad', 1),
    ('modificarActividad', 1),
    ('eliminarActividad', 1),
    ('consultarActividad', 1),
    ('asignarEnvio', 1),
    ('modificarEnvio', 1),
    ('ConsultarPQRSF', 1),
    ('agregarEstadoPQRSF', 1),
    ('modificarEstadoPQRSF', 1),
    ('eliminarEstadoPQRSF', 1),
    ('registrarRespuesta', 1),
    ('modificarRespuesta', 1),
    ('eliminarRespuesta', 1),
    ('consultarProducto', 2),
    ('consultarServicio', 2),
    ('crearCotizacion', 2),
    ('modificarCotizacion', 2),
    ('eliminarCotizacion', 2),
    ('consultarCotizacion', 2),
    ('crearCita', 2),
    ('modificarCita', 2),
    ('eliminarCita', 2),
    ('consultarCita', 2),
    ('consultarEnvios', 2),
    ('crearPQRSF', 2),
    ('consultarPQRSF', 2),
    ('consultarRespuesta', 2),
    ('consultarActividades', 3);

-- Inserción de asignación de permisos a roles
INSERT INTO Roles_has_Permisos (idRol, idPermiso)
VALUES 
   (1, 1), 
   (1, 2), 
   (1, 3), 
   (1, 4), 
   (1, 5),
   (1, 6), 
   (1, 7), 
   (1, 8), 
   (1, 9), 
   (1, 10),
   (1, 11), 
   (1, 12), 
   (1, 13), 
   (1, 14), 
   (1, 15),
   (1, 16), 
   (1, 17), 
   (1, 18), 
   (1, 19), 
   (1, 20),
   (1, 21), 
   (1, 22), 
   (1, 23), 
   (1, 24), 
   (1, 25),
   (2, 26), 
   (2, 27), 
   (2, 28), 
   (2, 29), 
   (2, 30),
   (2, 31), 
   (2, 32), 
   (2, 33), 
   (2, 34), 
   (2, 35),
   (2, 36), 
   (2, 37), 
   (2, 38), 
   (2, 39), 
   (3, 40);

-- Inserción de estados de usuarios
INSERT INTO EstadosUsuarios (nombreEstadoUsuario)
VALUES
    ('Activo'),
    ('Inactivo');

-- Inserción de usuarios
INSERT INTO Usuarios (numeroDocumento, nombre, apellido, email, password, numeroContacto, idRol, idEstadosUsuarios) 
VALUES
    (1021826839, 'Joaco', 'Galindo', 'JGalindo1980@jjsystem.com', '57P92rlN', 3208285814, 1, 1),
    (1027385914, 'Valentina', 'Gutiérrez', 'vgutierrez@mail.com', '2sY9rT5q', 3123456789, 2, 1),
    (1094730265, 'Santiago', 'Jiménez', 'sjimenez@mail.com', '6jK7cH3n', 3245678901, 2, 1),
    (1089456723, 'Isabella', 'Silva', 'isilva@mail.com', '4xG1vB8m', 3356789012, 2, 1),
    (1056709238, 'Daniel', 'Castro', 'dcastro@mail.com', '9pF6wE2k', 3478901234, 2, 1),
    (1078964532, 'Emilia', 'Martínez', 'emartinez@mail.com', '3lD5mV7c', 3590123456, 2, 1),
    (1025637498, 'Sebastián', 'Ramírez', 'sramirez@mail.com', '7nS2bR4g', 3612345678, 2, 1),
    (1064829375, 'María', 'Fernández', 'mfernandez@mail.com', '1vQ8tZ6f', 3734567890, 2, 1),
    (1045726398, 'Mateo', 'Vásquez', 'mvasquez@mail.com', '5dX3cN9h', 3856789012, 2, 1),
    (1038475629, 'Valeria', 'Pérez', 'vperez@mail.com', '8kL4rJ2w', 3978901234, 2, 1),
    (1015928364, 'Miguel', 'Álvarez', 'malvarez@mail.com', '0zH7yT1x', 3090123456, 2, 1),
    (1009283754, 'Camila', 'Benítez', 'cbenitez@mail.com', '4tF3kP7s', 3123456780, 2, 1),
    (1093654782, 'Nicolás', 'Hernández', 'nhernandez@mail.com', '6jM7rG2v', 3234567891, 2, 1),
    (1082369745, 'Sofía', 'Muñoz', 'smunoz@mail.com', '2pB9lW3d', 3345678902, 2, 1),
    (1054978632, 'Diego', 'García', 'dgarcia@mail.com', '5xV8gQ1c', 3456789013, 2, 1),
    (1072369854, 'Valentina', 'Rojas', 'vrojas@mail.com', '7rN4vS6j', 3567890124, 2, 1),
    (1023986547, 'Daniela', 'Castro', 'dcastro2@mail.com', '3kD1wH8m', 3678901235, 2, 1),
    (1067582943, 'Andrés', 'Sánchez', 'asanchez@mail.com', '9qT6fJ2b', 3789012346, 2, 1),
    (1049763258, 'Abril', 'Betancourt', 'abetancourt@mail.com', '1yZ8xG7s', 3890123457, 2, 1),
    (1038596472, 'Juan', 'Pérez', 'jperez2@mail.com', '5cN2vB4h', 3901234568, 2, 1),
    (1012375986, 'Samantha', 'González', 'sgonzalez@mail.com', '8wL6mC3q', 3012345679, 2, 1),
    (1007496358, 'Manuel', 'Jaramillo', 'mjaramillo@mail.com', '0hS9pR7d', 3145678902, 2, 1),
    (1098576234, 'Luciana', 'López', 'llopez@mail.com', '6nG2sT4r', 3278901234, 2, 1),
    (1089275463, 'Tomás', 'Moreno', 'tmoreno@mail.com', '2mK9cX5j', 3301234565, 2, 1),
    (1057468239, 'Camilo', 'Castro', 'ccastro@mail.com', '4bV8nQ1f', 3434567896, 2, 1),
    (1079358624, 'Ana', 'Sánchez', 'asanchez@mail.com', '7sW3jH6g', 3567890127, 2, 1),
    (1028374659, 'Luisa', 'Martínez', 'lmartinez@mail.com', '1rD6tZ2k', 3690123458, 2, 1),
    (1062937548, 'José', 'Ramírez', 'jramirez@mail.com', '3gF5wC7v', 3723456789, 2, 1),
    (1045376289, 'María', 'José', 'mariaj@mail.com', '9vM2xR4l', 3856789010, 2, 1),
    (1038279654, 'Daniel', 'Ramirez', 'danira@mail.com', '5wB4dN1p', 3989012341, 2, 1),
    (1012547698, 'Carlos', 'Gonzales', 'cargonz@mail.com', '8cQ7hL3y', 3001234562, 2, 1),
    (1007986453, 'Mar', 'gonzalez', 'maria.gonzalez@jjsystem.com', '6qG2vJ4c', 3001234567, 3, 1),
    (1098465237, 'Juan', 'Perez', 'juan.perez@jjsystem.com', '0jP9sT5r', 3123456789, 3, 1),
    (1085679234, 'David', 'Herrero', 'david.smith@jjsystem.com', '2hK9bX7n', 3789012345, 3, 1),
    (1057623948, 'Sara', 'Johnson', 'sarah.johnson@jjsystem.com', '4fV8mS1g', 3567890123, 3, 1),
    (1079348562, 'Carlos', 'Rodriguez', 'carlos.rodriguez@jjsystem.com', '7nW3sJ6d', 3456789123, 3, 1),
    (1029875463, 'Emily', 'Williams', 'emily.williams@jjsystem.com', '1tZ6rD2k', 3890123456, 3, 1),
    (1068457329, 'Antonio', 'Lopez', 'antonio.lopez@jjsystem.com', '3xH5cF7w', 3456789234, 3, 1),
    (1045376298, 'Laura', 'Diaz', 'laura.diaz@jjsystem.com', '9lQ2vT4n', 3567834521, 3, 1),
    (1036485927, 'José', 'Ramírez', 'jose.ramirez@jjsystem.com', '5bN4pR1m', 3789012165, 3, 1),
    (1019286547, 'Ana', 'castro', 'ana.castro@jjsystem.com', '8gC7sW3j', 3456701234, 3, 1);

-- Inserción de clientes
INSERT INTO Clientes (direccionCliente, numeroDocumento)
VALUES
    ('Calle 123 # 45-67', 1027385914),
    ('Carrera 78A # 12-34', 1094730265),
    ('Avenida 987 Sur # 56-78', 1089456723),
    ('Calle 456B # 90-12', 1056709238),
    ('Transversal 654 Este # 34-56', 1078964532),
    ('Diagonal 321Bis # 78-90', 1025637498),
    ('Calle 789 Norte # 12-34', 1064829375),
    ('Carrera 246Bis # 56-78', 1045726398),
    ('Avenida 753 Sur # 90-12', 1038475629),
    ('Calle 864 Este # 34-56', 1015928364),
    ('Carrera 231Bis # 78-90', 1009283754),
    ('Avenida 875 Norte # 12-34', 1093654782),
    ('Calle 692Bis # 56-78', 1082369745),
    ('Carrera 318Bis # 90-12', 1054978632),
    ('Avenida 947 Sur # 34-56', 1072369854),
    ('Calle 526 Este # 78-90', 1023986547),
    ('Carrera 183Bis # 12-34', 1067582943),
    ('Avenida 796 Norte # 56-78', 1049763258),
    ('Calle 459Bis # 90-12', 1038596472),
    ('Carrera 102Bis # 34-56', 1012375986),
    ('Avenida 735 Sur # 78-90', 1007496358),
    ('Calle 384 Este # 12-34', 1098576234),
    ('Carrera 961Bis # 56-78', 1089275463),
    ('Avenida 578 Norte # 90-12', 1057468239),
    ('Calle 215Bis # 34-56', 1079358624),
    ('Carrera 849 Este # 78-90', 1028374659),
    ('Avenida 476Bis # 12-34', 1062937548),
    ('Calle 103 Sur # 56-78', 1045376289),
    ('Carrera 732Bis # 90-12', 1038279654),
    ('Avenida 369 Este # 34-56', 1012547698);

-- Inserción de administradores
INSERT INTO Administrador (numeroDocumento) 
VALUES (1021826839);

-- Inserción de especialidad de técnicos
INSERT INTO Especialidad_tecnicos(nombre_especialidad)
VALUES
	('Analisis'),
    ('Instalacion'),
    ('Mantenimiento');
-- Inserción de técnicos
INSERT INTO Tecnicos (id_especialidad_fk, numeroDocumento)
VALUES
    (1, 1007986453),
    (2, 1098465237),
    (3, 1085679234),
    (1, 1057623948),
    (2, 1079348562),
    (3, 1029875463),
    (1, 1068457329),
    (2, 1045376298),
    (3, 1036485927),
    (1, 1019286547);

-- Inserción de estados de envío
INSERT INTO EstadosEnvios (nombreEstadoEnvio)
VALUES
    ('En bodega'),
    ('Llegando'),
    ('Entregado');

-- Inserción de envíos
INSERT INTO Envios (direccionEnvio, idTecnico, idEstadoEnvio)
VALUES
    ('Calle 23 # 14-34, Barrio La Candelaria', 6, 2),
    ('Carrera 11 # 22-45, Barrio Chapinero Alto', 3, 1),
    ('Avenida Caracas # 67-89, Barrio Quinta Camacho', 10, 3),
    ('Calle 72 # 5-67, Barrio La Cabrera', 4, 1),
    ('Carrera 9 # 122-21, Barrio Usaquén', 1, 1),
    ('Calle 26 # 68-34, Barrio El Campín', 9, 3),
    ('Avenida Suba # 100-23, Barrio Suba', 7, 2),
    ('Carrera 7 # 32-12, Barrio La Merced', 8, 3),
    ('Calle 63 # 15-34, Barrio San Felipe', 2, 1),
    ('Carrera 13 # 26-45, Barrio La Soledad', 5, 3),
    ('Avenida Calle 100 # 19-34, Barrio Chicó Norte', 6, 2),
    ('Calle 53 # 12-56, Barrio Galerías', 3, 3),
    ('Carrera 15 # 78-34, Barrio Santa Bárbara', 10, 1),
    ('Calle 72 # 11-45, Barrio Rosales', 4, 2),
    ('Avenida Carrera 30 # 62-23, Barrio La Macarena', 1, 1),
    ('Calle 85 # 18-34, Barrio El Nogal', 9, 3),
    ('Carrera 5 # 9-12, Barrio La Catedral', 7, 2),
    ('Avenida 68 # 13-56, Barrio Los Andes', 8, 1),
    ('Calle 19 # 10-34, Barrio La Perseverancia', 2, 1),
    ('Carrera 17 # 21-45, Barrio Teusaquillo', 5, 2),
    ('Avenida Caracas # 47-89, Barrio Santa Isabel', 6, 2),
    ('Calle 100 # 13-67, Barrio El Refugio', 3, 3),
    ('Carrera 30 # 45-21, Barrio El Recuerdo', 10, 1),
    ('Calle 72 # 19-56, Barrio La Castellana', 4, 3),
    ('Carrera 13 # 21-34, Barrio San Luis', 1, 2),
    ('Avenida Suba # 70-12, Barrio La Floresta', 9, 1),
    ('Calle 63 # 12-45, Barrio La Estancia', 7, 2),
    ('Carrera 7 # 28-56, Barrio El Polo', 8, 3),
    ('Avenida Boyacá # 72-23, Barrio Salitre Greco', 2, 3),
    ('Calle 39 # 14-34, Barrio Antonio Nariño', 5, 1); 
    
INSERT INTO categoriasProductos (nombreCategoria) 
VALUES
	("Camara"),
    ("DVR"),
    ("Alarma"),
    ("Sensor");
    
INSERT INTO proveedoresProductos (nombreProveedor)
VALUES
	("TechSecure"),
    ("SecureGuard"),
    ("SecureTech Solutions"),
	("Servicios SafeGuard"),
    ("TechGuard Systems"),
    ("Soluciones SecureNet"),
    ("Servicios de Seguridad Proactiva"),
    ("Sistemas de Seguridad Global"),
    ("Security Solutions"),
    ("Seguridad integrada de Tyco"),
    ("Soluciones de seguridad Stanley"),
    ("Soluciones de construcción de Honeywell"),
    ("Tecnologías de construcción de Siemens"),
    ("Vida digital de AT&T");

INSERT INTO Productos (nombreProducto, descripcionProducto, precioProducto, cantidad, idAdministrador, idCategoriaProducto, idProveedorProducto)
VALUES
	('Cámara de vigilancia HD+','Una cámara de última generación que captura imágenes de alta definición con precisión y nitidez. Su diseño discreto se integra perfectamente en cualquier entorno, ofreciendo una protección encubierta. Fácil de instalar y utilizar, es la elección ideal para mantener tus espacios seguros.', 158000, 12, 1, 1, 3),
	('Cámara de seguridad IP','Cámara de seguridad IP: Permite una conexión a través de la red para acceder a las imágenes desde cualquier lugar.',526000, 14, 1, 1, 6),
	('Cámara domo PTZ','Cámara domo PTZ: Posee movimiento y zoom controlables, ideal para monitorear áreas amplias y seguir objetos en movimiento.', 408000, 15, 1, 1, 14),
	('Cámara bullet infrarroja','Cámara bullet infrarroja: Diseñada para capturar imágenes claras incluso en condiciones de poca luz gracias a su iluminación infrarroja.', 278000, 11, 1, 1, 14),
	('Cámara de videovigilancia 360°','Cámara de videovigilancia 360°: Proporciona una vista panorámica completa para vigilar grandes espacios sin puntos ciegos.', 116000, 18, 1, 1, 5),
	('Cámara de vigilancia exterior resistente al agua','Cámara de vigilancia exterior resistente al agua: Diseñada para soportar las condiciones climáticas adversas y mantener la vigilancia en exteriores.', 419000, 16, 1, 1, 11),
	('Cámara oculta de alta resolución','Cámara oculta de alta resolución: Permite una vigilancia encubierta sin llamar la atención, capturando imágenes detalladas.', 222000, 13, 1, 1, 7),
	('Cámara de vigilancia panorámica de alta definición','Cámara de vigilancia panorámica de alta definición: Proporciona una vista amplia y de alta calidad para una vigilancia efectiva.', 534000, 17, 1, 1, 8),
	('Cámara de videovigilancia WiFi','Cámara de videovigilancia WiFi: Conexión inalámbrica que facilita la instalación y el acceso remoto a las imágenes.', 297000, 19, 1, 1, 4),
	('Cámara de seguridad con visión nocturna','Cámara de seguridad con visión nocturna: Permite la vigilancia continua incluso en condiciones de poca o ninguna luz.', 452000, 12, 1, 1, 6),
	('DVR de 8 canales','DVR de 8 canales: Permite la grabación y almacenamiento de imágenes de hasta 8 cámaras de vigilancia.', 590000, 2, 1, 2, 8),
	('DVR de alta capacidad de almacenamiento','DVR de alta capacidad de almacenamiento: Proporciona un espacio amplio para almacenar un gran volumen de imágenes de vigilancia.', 245000, 14, 1, 2, 13),
	('DVR híbrido analógico/IP','DVR híbrido analógico/IP: Compatible con cámaras analógicas e IP, brindando flexibilidad en la configuración del sistema de vigilancia.', 188000, 18, 1, 2, 14),
	('DVR de 16 canales con conexión remota','DVR de 16 canales con conexión remota: Permite el acceso y monitoreo remoto de las imágenes de hasta 16 cámaras.', 524000, 10, 1, 2, 11),
	('DVR de seguridad de 4K Ultra HD','DVR de seguridad de 4K Ultra HD: Ofrece una resolución de imagen excepcional para una visualización detallada y clara.', 358000, 15, 1, 2, 14),
	('DVR de video vigilancia móvil','DVR de video vigilancia móvil: Diseñado para vehículos, permite la grabación de imágenes en movimiento para una vigilancia en tiempo real.', 143000, 13, 1, 2, 2),
	('DVR de grabación continua 24/7','DVR de grabación continua 24/7: Permite la grabación constante sin interrupciones para una vigilancia ininterrumpida.', 492000, 16, 1, 2, 12),
	('Alarma de intrusión inalámbrica','Alarma de intrusión inalámbrica: Detecta la presencia de intrusos y emite una señal de alarma de forma inalámbrica.', 118000, 17, 1, 3, 14),
	('Alarma de seguridad con detector de movimiento','Alarma de seguridad con detector de movimiento: Activa una alarma cuando se detecta movimiento en el área protegida.', 399000, 20, 1, 3, 13),
	('Alarma de emergencia sonora y luminosa','Alarma de emergencia sonora y luminosa: Emite una señal sonora y activa luces de advertencia en situaciones de emergencia.', 100000, 10, 1, 3, 11),
	('Alarma de incendio con sensor de humo','Alarma de incendio con sensor de humo: Detecta la presencia de humo y activa una alarma para alertar sobre un posible incendio.', 352000, 12, 1, 3, 13),
	('Alarma de detección de gas','Alarma de detección de gas: Detecta la presencia de gases tóxicos o peligrosos y emite una alarma para advertir de una posible fuga.', 474000, 15, 1, 3, 10),
	('Alarma de seguridad para ventanas y puertas','Alarma de seguridad para ventanas y puertas: Detecta la apertura o manipulación de ventanas y puertas y activa una alarma.', 209000, 14, 1, 3, 3),
	('Sensor de movimiento infrarrojo pasivo (PIR)','Sensor de movimiento infrarrojo pasivo (PIR): Detecta el movimiento de personas o animales basándose en cambios de temperatura.', 311000, 16, 1, 4, 11),
	('Sensor de apertura de puertas y ventanas','Sensor de apertura de puertas y ventanas: Detecta la apertura o cierre de puertas y ventanas y envía una señal de alerta.', 191000, 15, 1, 4, 11),
	('Sensor de inundación inalámbrico','Sensor de inundación inalámbrico: Detecta la presencia de agua y activa una alarma para prevenir daños causados por inundaciones.', 505000, 11, 1, 4, 1),
	('Sensor de vibración para detección de impactos','Sensor de vibración para detección de impactos: Detecta vibraciones o golpes bruscos y activa una alarma en caso de intento de intrusión.', 482000, 13, 1, 4, 14),
	('Sensor de temperatura y humedad','Sensor de temperatura y humedad: Monitoriza los cambios de temperatura y humedad en un entorno y envía notificaciones en caso de desviaciones.', 227000, 17, 1, 4, 3),
	('Sensor de movimiento para exteriores','Sensor de movimiento para exteriores: Diseñado para áreas exteriores, detecta el movimiento y activa una respuesta de seguridad.', 408000, 18, 1, 4, 4),
	('Sensor de humo y calor','Sensor de humo y calor: Detecta el humo y los cambios de temperatura causados por un incendio y activa una alarma.', 276000, 20, 1, 4, 7);

INSERT INTO categoriasServicios (nombreCategoria)
VALUES
	('Venta'),
    ('Instalacion'),
    ('Análisis'),
    ('Mantenimiento');
    
INSERT INTO Servicios (nombreServicio, descripcionServicio, idCategoriaServicio)
VALUES
	('Venta', 'Venta de productos', 1),
    ('Instalacion de camaras', 'Proceso de colocar y configurar cámaras de seguridad en un lugar determinado, con el fin de vigilar y grabar imágenes para proteger la propiedad, prevenir el delito y mejorar la seguridad.', 3),
    ('Instalacion de sensores', 'Proceso de colocar y configurar dispositivos electrónicos que detectan cambios en el entorno físico y los predeterminados en señales eléctricas para su uso en diversas aplicaciones.', 4),
    ('Instalacion de cerca electrica', 'Instalación y configuración de un sistema de seguridad que utiliza una barrera electrificada para proteger perímetros y evitar intrusiones no deseadas en propiedades.', 2),
    ('Analisis', 'El servicio de instalación generalmente incluye una evaluación previa del lugar para determinar la mejor ubicación para las cámaras o cercas y la cantidad de cámaras necesarias para cubrir el área de manera efectiva.', 3),
    ('Mantenimiento computadores', 'El mantenimiento de computadoras es el cuidado y la atención que se brinda a los equipos informáticos para mantenerlos en buen estado y funcionando correctamente.', 2),
    ('Mantenimiento camaras', 'El mantenimiento de cámaras implica tareas como limpieza interna y externa, limpieza del sensor, verificación del enfoque, actualización del firmware, revisión de baterías y conexiones, y almacenamiento adecuado. Estas acciones mantienen la calidad de las imágenes, previenen problemas y prolongan la vida útil de las cámaras. Es importante seguir las indicaciones del fabricante y buscar servicios técnicos especializados cuando sea necesario.', 3),
    ('Mantenimiento cerca electrica', 'El mantenimiento de una cerca eléctrica implica inspeccionar, limpiar y probar regularmente el sistema para garantizar su funcionamiento adecuado. Es importante revisar los componentes en busca de daños, limpiar la cerca para eliminar la suciedad y realizar pruebas para asegurar la emisión correcta de pulsos eléctricos. También se deben verificar las conexiones eléctricas y realizar reparaciones o reemplazos según sea necesario. Se recomienda contar con la ayuda de un profesional y cumplir con las regulaciones locales.', 4),
    ('Mantenimiento sensores', 'El mantenimiento de sensores se encarga de cuidar y mantener en buen estado los dispositivos electrónicos que detectan cambios en el entorno. Los sensores son utilizados para diferentes propósitos, como medir temperatura, humedad, movimiento, entre otros.', 2);

INSERT INTO EstadosCotizaciones(nombreEstadoCotizacion)
VALUES
	('Activa'),
    ('Inactiva');


INSERT INTO Cotizaciones (fechaCotizacion, totalCotizacion, descripcionCotizacion, idCliente, idEstadoCotizacion)
VALUES
    ('2023-04-15', 75000, 'Instalación de una cámara de seguridad IP en la entrada principal del edificio', 26, 1),
    ('2023-04-16', 100000, 'Suministro de una alarma de intrusión para el hogar', 18, 1),
    ('2023-04-20', 187000, 'Venta', 9, 1),
    ('2023-04-22', 50000, 'Reparación del sistema de monitoreo en la tienda', 11, 1),
    ('2023-04-23', 85000, 'Instalación de cuatro cámaras de seguridad CCTV en la bodega', 1, 1),
    ('2023-04-24', 120000, 'Suministro de una alarma contra incendios para el restaurante', 19, 1),
    ('2023-04-25', 110000, 'Instalación de un sistema de control de acceso biométrico en la empresa', 27, 1),
    ('2023-04-26', 46000, 'Venta de una cámara de seguridad domo para la residencia', 10, 1),
    ('2023-04-28', 55000, 'Venta de un control remoto adicional para la alarma de la tienda', 14, 1),
    ('2023-04-30', 90000, 'Instalación de dos cámaras de seguridad inalámbricas en la casa', 13, 1),
    ('2023-05-01', 110000, 'Suministro de una alarma contra intrusos para la oficina', 17, 1),
    ('2023-05-02', 78000, 'Mantenimiento preventivo de las cámaras de vigilancia en el estacionamiento', 25, 1),
    ('2023-05-03', 140000, 'Instalación de un sistema de cámaras de seguridad en el edificio de apartamentos', 8, 1),
    ('2023-05-05', 68000, 'Venta de un sensor de movimiento para el patio trasero', 21, 1),
    ('2023-05-07', 125000, 'Instalación de una alarma con sensor de humo en la cocina del restaurante', 20, 1),
    ('2023-05-08', 95000, 'Venta de una cámara de vigilancia panorámica para la tienda de conveniencia', 5, 1),
    ('2023-05-10', 76000, 'Instalación de una alarma perimetral en el jardín de la casa', 2, 1),
    ('2023-05-12', 105000, 'Venta de un sensor de vibración para la alarma de la empresa', 24, 1),
    ('2023-05-14', 92000, 'Instalación de una cámara de seguridad oculta en la sala de reuniones', 4, 1),
    ('2023-05-15', 65000, 'Venta de una alarma de emergencia para el taller mecánico', 16, 1);

INSERT INTO Cotizaciones_Productos (idProducto, idCotizacion, cantidad)
VALUES
    (1, 1, 1),
    (23, 2, 1),
    (22, 3, 1),
    (3, 4, 1),
    (7, 5, 4),
    (9, 6, 1),
    (7, 7, 1),
    (26, 8, 1),
    (12, 9, 1),
    (21, 10, 2),
    (14, 11, 1),
    (4, 12, 1),
    (25, 13, 1),
    (16, 14, 1),
    (25, 15, 1),
    (19, 16, 1),
    (18, 17, 1),
    (15, 18, 1),
    (13, 19, 1),
    (11, 20, 1);


INSERT INTO Cotizaciones_Servicios (idServicio, idCotizacion)
VALUES
    (1, 1),
    (2, 2),
    (3, 3),
    (6, 4),
    (4, 5),
    (1, 6),
    (8, 7),
    (5, 8),
    (5, 9),
    (1, 10),
    (4, 11),
    (7, 12),
    (4, 13),
    (1, 14),
    (4, 15),
    (2, 16),
    (1, 17),
    (4, 18),
    (5, 19),
    (1, 20);
    
INSERT INTO EstadosCitas (nombreEstadoCita)
VALUES
	('Confirmada'),
	('Cancelada'),
	('Modificada'),
    ('Programada');

INSERT INTO Citas (fechaCita, direccionCita, contactoCliente, descripcionCita, idTecnico, idAdministrador, idCotizacion, idEstadoCita)
VALUES
	('2023-06-01', 'Calle 23 # 14-34, Barrio La Candelaria', 3478901234, 'Reunión para discutir instalación de cámaras de seguridad', 4, 1, 8, 1),
	('2023-06-02', 'Carrera 11 # 22-45, Barrio Chapinero Alto', 3734567890, 'Visita técnica para evaluar instalación de sistema de monitoreo', 7, 1, 16, 2),
	('2023-06-03', 'Avenida Caracas # 67-89, Barrio Quinta Camacho', 3856789012, 'Asesoramiento sobre sistemas de control de acceso', 2, 1, 13, 2),
	('2023-06-04', 'Calle 72 # 5-67, Barrio La Cabrera', 3356789012, 'Reunión para cotización de alarmas de intrusión', 6, 1, 5, 3),
	('2023-06-05', 'Carrera 9 # 122-21, Barrio Usaquén', 3789012346, 'Instalación de videoportero en apartamento', 8, 1, 3, 2),
	('2023-06-06', 'Calle 26 # 68-34, Barrio El Campín', 3278901234, 'Revisión de sistema de control de acceso biométrico', 1, 1, 10, 1),
	('2023-06-07', 'Avenida Suba # 100-23, Barrio Suba', 3890123457, 'Visita técnica para evaluación de cámaras de seguridad', 3, 1, 15, 2),
	('2023-06-08', 'Carrera 7 # 32-12, Barrio La Merced', 3856789010, 'Reunión para discutir mantenimiento de sistemas de seguridad', 9, 1, 7, 3),
	('2023-06-09', 'Calle 63 # 15-34, Barrio San Felipe', 3123456780, 'Instalación de cámaras de seguridad inalámbricas', 5, 1, 18, 2),
	('2023-06-10', 'Carrera 13 # 26-45, Barrio La Soledad', 3989012341, 'Reunión para cotización de sistema de detección de intrusos', 2, 1, 11, 1),
	('2023-06-11', 'Avenida Calle 100 # 19-34, Barrio Chicó Norte', 3001234562, 'Asesoramiento sobre sistemas de intercomunicación', 10, 1, 4, 3),
	('2023-06-12', 'Calle 53 # 12-56, Barrio Galerías', 3678901235, 'Visita técnica para evaluar sistema de control de acceso vehicular', 3, 1, 14, 2),
	('2023-06-13', 'Carrera 15 # 78-34, Barrio Santa Bárbara', 3590123456, 'Reunión para cotización de cámaras de seguridad PTZ', 9, 1, 17, 3),
	('2023-06-14', 'Calle 72 # 11-45, Barrio Rosales', 3456789013, 'Instalación de alarma contra incendios en restaurante', 7, 1, 6, 1),
	('2023-06-15', 'Avenida Carrera 30 # 62-23, Barrio La Macarena', 3434567896, 'Revisión de sistema de control de acceso peatonal', 4, 1, 12, 1),
	('2023-06-16', 'Calle 85 # 18-34, Barrio El Nogal', 3590123456, 'Visita técnica para evaluación de cerraduras electrónicas', 2, 1, 19, 1);

INSERT INTO DisponibilidadCronogramas (nombreDisponibilidad)
VALUES
	("Disponible"),
    ("No disponible");

INSERT INTO CronogramaTecnicos (idTecnico, idCita, idDisponibilidadCronograma)
VALUES
	(5, 8, 2),
	(3, 4, 2),
	(2, 15, 2),
	(10, 6, 2),
	(8, 7, 2),
	(7, 11, 2),
	(1, 14, 2),
	(9, 15, 2),
	(6, 10, 2),
	(4, 2, 1);

INSERT INTO ActividadesCronogramaTecnicos (nombreActividad)
VALUES
	("Cita de Análisis"),
    ("Cita de Mantenimiento"),
    ("Cita de Instalación"),
    ("Entrega de Envío");
    
INSERT INTO detallesactividadcronograma (idCronogramaTecnico, idActividadCronogramaTecnico, fechaActividadCronograma)
VALUE
	(1, 1,'2022-07-18 09:30:00'),
	(2, 2, '2023-02-14 17:00:00'),
	(3, 2, '2022-11-30 08:30:00'),
	(4, 3, '2023-01-05 14:30:00'),
	(5, 4, '2022-08-21 13:00:00'),
	(6, 2, '2023-03-10 11:00:00'),
	(7, 3, '2022-09-09 06:15:00'),
	(8, 4, '2023-06-05 19:14:28'),
	(9, 2, '2022-12-12 13:39:50'),
	(10, 4, '2023-04-25 03:58:09');

INSERT INTO Ventas (fechaVenta, idEnvio, idCotizacion)
VALUES
    ('2023-01-01', 27, 1),
    ('2023-02-05', 29, 2),
    ('2023-03-10', 30, 3),
    ('2023-04-15', 16, 4),
    ('2023-05-20', 28, 5),
    ('2023-06-25', 26, 6),
    ('2023-07-30', 17, 7),
    ('2023-08-04', 22, 8),
    ('2023-09-09', 24, 9),
    ('2023-10-14', 23, 10),
    ('2023-01-26', 25, 11),
    ('2023-06-15', 21, 12),
    ('2023-03-03', 20, 13),
    ('2023-03-12', 19, 14),
    ('2023-01-18', 18, 15),
    ('2022-11-24', 15, 16),
    ('2022-08-15', 11, 17),
    ('2022-08-08', 13, 18),
    ('2022-09-01', 12, 19);

INSERT INTO DetallesVentas (detallesVenta, subtotalVenta, totalVenta, idVenta)
VALUES
	('Instalación de una cámara de seguridad IP en la entrada principal del edificio', 75000, 80000, 1),
    ('Suministro de una alarma de intrusión para el hogar', 100000, 100000, 2),
    ('Venta alarma de detección de gas', 187000, 187000, 3),
    ('Reparación del sistema de monitoreo en la tienda', 50000, 50000, 4),
    ('Instalación de cuatro cámaras de seguridad CCTV en la bodega', 80000, 80000, 5),
    ('Suministro de una alarma contra incendios para el restaurante', 100000, 80000, 6),
    ('Instalación de un sistema de control de acceso biométrico en la empresa', 75000, 80000, 7),
    ('Venta de una cámara de seguridad domo para la residencia', 67800, 70000, 8),
    ('Venta de un control remoto adicional para la alarma de la tienda', 48000, 55000, 9),
    ('Instalación de dos cámaras de seguridad inalámbricas en la casa', 90000, 150000, 10);

INSERT INTO tiposPQRSF (nombreTipoPQRSF)
VALUES
	("Peticion"),
    ("Queja"),
    ("Reclamo"),
    ("Sugerencia"),
    ("Felicitacion");
    
INSERT INTO estadosPQRSF (nombreEstadoPQRSF)
VALUES
	("Solicitada"),
    ("En trámite"),
    ("Resuelta");
    
INSERT INTO PQRSF (fechaPQRSF, informacionPQRSF, idCliente, idTipoPQRSF, idEstadoPQRSF)
VALUES
    ('2023-01-01', 'Presenté un reclamo sobre un sistema de cámaras de seguridad que no quedó bloqueado durante un robo en mi negocio. Quiero que se investigue y se resuelva el problema para evitar futuras pérdidas.', 1, 3, 3),
    ('2023-01-01', 'Solicito información sobre los precios y la disponibilidad de cámaras de seguridad inalámbricas para instalar en mi hogar. También me gustaría programar una cita con un representante de ventas para discutir las características técnicas del producto.', 2, 1, 3),
    ('2023-01-01', 'Quería felicitar a la empresa por la excelente atención al cliente que recibió durante la instalación de mi sistema de seguridad. El técnico fue muy profesional y amable, y resolvió todas mis dudas de manera clara y concisa. ¡Gracias por el excelente servicio!', 3, 5, 3),
    ('2023-01-01', 'Quiero felicitar al equipo de soporte técnico de su empresa por su excelente trabajo en solucionar el problema que utiliza con nuestro sistema de seguridad. Su rápida respuesta y profesionalismo fueron impresionantes. ¡Gracias!', 4, 5, 3),
    ('2023-01-01', 'Compré un sistema de seguridad para mi casa hace un mes, y ahora no funciona correctamente. He tratado de contactar al servicio al cliente varias veces sin obtener respuesta.', 5, 2, 3),
    ('2023-01-01', 'Mi sistema de seguridad no limita un robo y perdí objetos de valor. Quiero presentar un reclamo por la pérdida sufrida.', 6, 3, 3),
    ('2023-01-01', 'Sugiero que la empresa considere agregar una función de geolocalización para los sistemas de seguridad, para que los clientes puedan rastrear la ubicación de sus cámaras y otros dispositivos desde su teléfono inteligente.', 7, 4, 3),
    ('2023-01-01', 'Quiero felicitar a la empresa por su excelente servicio al cliente. El representante que me atendió fue muy amable y me ayudó a elegir el sistema de seguridad perfecto para mi hogar. El técnico que realizó la instalación también fue muy profesional y me enseñó cómo usar el sistema de seguridad de manera efectiva. ¡Gracias por hacer que mi hogar sea más seguro!', 8, 5, 3),
    ('2023-01-01', 'He estado teniendo problemas con mi sistema de seguridad durante semanas y el soporte técnico no ha sido capaz de solucionarlo. Ya he llamado varias veces y nadie parece saber cómo arreglar el problema. Esto es inaceptable.', 9, 2, 3),
    ('2023-01-01', 'Mi sistema de seguridad no protegido durante un robo y sufrí una pérdida significativa de propiedad. Quiero presentar un reclamo por el daño causado.', 10, 3, 3),
    ('2023-01-01', 'Sugiero que agreguen la opción de grabación en la nube para las cámaras de seguridad en el hogar. Sería una gran comodidad para los clientes poder acceder a sus grabaciones de seguridad desde cualquier lugar.', 11, 4, 3),
    ('2023-01-01', 'Descripción: Mi sistema de seguridad se activó accidentalmente y llamó a la policía sin motivo. Solicito una solución a este problema para evitar futuros problemas similares.', 12, 3, 3),
    ('2023-01-01', 'Quiero felicitar a su equipo técnico por la excelente instalación del sistema de seguridad en mi hogar. Fueron muy profesionales, amables y respetuosos durante todo el proceso.', 13, 5, 3),
    ('2023-01-01', 'Presento un reclamo porque después de comprar e instalar el sistema de seguridad, este no falló correctamente durante un robo y no recibió la respuesta adecuada del servicio al cliente.', 14, 3, 3),
    ('2023-01-01', 'Sugerencia para agregar una función de programación de luces en el sistema de seguridad para disuadir a los ladrones.', 15, 4, 3),
    ('2023-01-01', 'Compre un sistema de seguridad para mi hogar hace tres meses y ha tenido problemas desde entonces. Las alarmas se activan sin motivo aparente y el servicio técnico no ha sido capaz de solucionar el problema.', 16, 2, 3);

INSERT INTO Respuestas (fecha, informacionRespuesta, idAdministrador, idPQRSF)
VALUES
    ('2023-01-10', 'Gracias por presentar su reclamo sobre el sistema de cámaras de seguridad. Lamentamos mucho lo ocurrido y entendemos la importancia de proteger su negocio. Nos comprometemos a investigar a fondo este incidente y a resolver el problema para evitar futuras pérdidas. Nuestro equipo de soporte técnico se comunicará con usted para recopilar más información y tomar las medidas necesarias. Agradecemos su paciencia y estamos comprometidos en brindarle un servicio de seguridad confiable.', 1, 1),
    ('2023-01-11', 'Agradecemos su interés en nuestras cámaras de seguridad inalámbricas. Con gusto le proporcionaremos la información sobre los precios y disponibilidad de los productos que desea. También le ofrecemos programar una cita con uno de nuestros representantes de ventas, quienes estarán encantados de discutir las características técnicas del producto y responder a todas sus preguntas. Pronto recibirá un correo electrónico con los detalles y opciones para coordinar la cita. Esperamos poder ayudarle a garantizar la seguridad de su hogar.', 1, 2),
    ('2023-01-12', 'Nos alegra mucho recibir su felicitación y saber que está satisfecho con nuestro servicio al cliente. Transmitiremos sus amables palabras a nuestro equipo, incluyendo al técnico que realizó la instalación. Su reconocimiento es muy valioso para nosotros y nos motiva a seguir brindando un servicio de calidad. Si tiene alguna otra consulta o necesita asistencia adicional, no dude en comunicarse con nosotros. ¡Gracias por elegirnos como su proveedor de seguridad!', 1, 3),
    ('2023-01-13', 'Nos alegra mucho recibir su felicitación y saber que está satisfecho con nuestro servicio al cliente. Transmitiremos sus amables palabras a nuestro equipo, incluyendo al técnico que realizó la instalación. Su reconocimiento es muy valioso para nosotros y nos motiva a seguir brindando un servicio de calidad. Si tiene alguna otra consulta o necesita asistencia adicional, no dude en comunicarse con nosotros. ¡Gracias por elegirnos como su proveedor de seguridad!', 1, 4),
    ('2023-01-14', 'Lamentamos mucho los inconvenientes que ha experimentado con su sistema de seguridad y el servicio al cliente. Entendemos su frustración y nos disculpamos por las dificultades para contactarnos. Nos gustaría resolver este problema lo antes posible. Nuestro equipo de soporte técnico se pondrá en contacto con usted para solucionar los problemas con su sistema y brindarle la asistencia necesaria. Valoramos su paciencia y confianza en nuestra empresa, y trabajaremos arduamente para resolver esta situación.', 1, 5),
    ('2023-01-15', 'Gracias por presentar su reclamo sobre el sistema de cámaras de seguridad. Lamentamos mucho lo ocurrido y entendemos la importancia de proteger su negocio. Nos comprometemos a investigar a fondo este incidente y a resolver el problema para evitar futuras pérdidas. Nuestro equipo de soporte técnico se comunicará con usted para recopilar más información y tomar las medidas necesarias. Agradecemos su paciencia y estamos comprometidos en brindarle un servicio de seguridad confiable.', 1, 6),
    ('2023-01-16', 'Agradecemos su sugerencia de agregar una función de geolocalización a nuestros sistemas de seguridad. Es una idea interesante que consideraremos en nuestros desarrollos futuros. Valoramos los comentarios de nuestros clientes, ya que nos ayudan a mejorar nuestros productos y servicios. Si tiene alguna otra sugerencia o consulta, no dude en compartirla con nosotros. ¡Gracias por su aporte!', 1, 7),
    ('2023-01-17', 'Nos alegra mucho recibir su felicitación y saber que está satisfecho con nuestro servicio al cliente. Transmitiremos sus amables palabras a nuestro equipo, incluyendo al técnico que realizó la instalación. Su reconocimiento es muy valioso para nosotros y nos motiva a seguir brindando un servicio de calidad. Si tiene alguna otra consulta o necesita asistencia adicional, no dude en comunicarse con nosotros. ¡Gracias por elegirnos como su proveedor de seguridad!', 1, 8),
    ('2023-01-18', 'Lamentamos mucho los inconvenientes que ha experimentado con su sistema de seguridad y el servicio al cliente. Entendemos su frustración y nos disculpamos por las dificultades para contactarnos. Nos gustaría resolver este problema lo antes posible. Nuestro equipo de soporte técnico se pondrá en contacto con usted para solucionar los problemas con su sistema y brindarle la asistencia necesaria. Valoramos su paciencia y confianza en nuestra empresa, y trabajaremos arduamente para resolver esta situación.', 1, 9),
    ('2023-01-19', 'Gracias por presentar su reclamo sobre el sistema de cámaras de seguridad. Lamentamos mucho lo ocurrido y entendemos la importancia de proteger su negocio. Nos comprometemos a investigar a fondo este incidente y a resolver el problema para evitar futuras pérdidas. Nuestro equipo de soporte técnico se comunicará con usted para recopilar más información y tomar las medidas necesarias. Agradecemos su paciencia y estamos comprometidos en brindarle un servicio de seguridad confiable.', 1, 10),
    ('2023-01-20', 'Agradecemos su sugerencia de agregar una función de geolocalización a nuestros sistemas de seguridad. Es una idea interesante que consideraremos en nuestros desarrollos futuros. Valoramos los comentarios de nuestros clientes, ya que nos ayudan a mejorar nuestros productos y servicios. Si tiene alguna otra sugerencia o consulta, no dude en compartirla con nosotros. ¡Gracias por su aporte!', 1, 11),
    ('2023-01-21', 'Gracias por presentar su reclamo sobre el sistema de cámaras de seguridad. Lamentamos mucho lo ocurrido y entendemos la importancia de proteger su negocio. Nos comprometemos a investigar a fondo este incidente y a resolver el problema para evitar futuras pérdidas. Nuestro equipo de soporte técnico se comunicará con usted para recopilar más información y tomar las medidas necesarias. Agradecemos su paciencia y estamos comprometidos en brindarle un servicio de seguridad confiable.', 1, 12),
    ('2023-01-22', 'Nos alegra mucho recibir su felicitación y saber que está satisfecho con nuestro servicio al cliente. Transmitiremos sus amables palabras a nuestro equipo, incluyendo al técnico que realizó la instalación. Su reconocimiento es muy valioso para nosotros y nos motiva a seguir brindando un servicio de calidad. Si tiene alguna otra consulta o necesita asistencia adicional, no dude en comunicarse con nosotros. ¡Gracias por elegirnos como su proveedor de seguridad!', 1, 13),
    ('2023-01-23', 'Gracias por presentar su reclamo sobre el sistema de cámaras de seguridad. Lamentamos mucho lo ocurrido y entendemos la importancia de proteger su negocio. Nos comprometemos a investigar a fondo este incidente y a resolver el problema para evitar futuras pérdidas. Nuestro equipo de soporte técnico se comunicará con usted para recopilar más información y tomar las medidas necesarias. Agradecemos su paciencia y estamos comprometidos en brindarle un servicio de seguridad confiable.', 1, 14),
    ('2023-01-24', 'Agradecemos su sugerencia de agregar una función de geolocalización a nuestros sistemas de seguridad. Es una idea interesante que consideraremos en nuestros desarrollos futuros. Valoramos los comentarios de nuestros clientes, ya que nos ayudan a mejorar nuestros productos y servicios. Si tiene alguna otra sugerencia o consulta, no dude en compartirla con nosotros. ¡Gracias por su aporte!', 1, 15),
    ('2023-01-25', 'Lamentamos mucho los inconvenientes que ha experimentado con su sistema de seguridad y el servicio al cliente. Entendemos su frustración y nos disculpamos por las dificultades para contactarnos. Nos gustaría resolver este problema lo antes posible. Nuestro equipo de soporte técnico se pondrá en contacto con usted para solucionar los problemas con su sistema y brindarle la asistencia necesaria. Valoramos su paciencia y confianza en nuestra empresa, y trabajaremos arduamente para resolver esta situación.', 1, 16);
    
    /*Vistas*/
    
     DROP VIEW IF EXISTS Producto_Categoria;
    
    CREATE VIEW Producto_Categoria AS 
	SELECT concat(nombreProducto, nombreCategoria) as Producto, nombreCategoria as Categoria
    From productos
    INNER JOIN categoriasproductos on productos.idCategoriaProducto = categoriasproductos.idCategoriaProducto;
    
      DROP VIEW IF EXISTS Servicio_Categoria;
    
    CREATE VIEW Servicio_Categoria AS 
	SELECT concat(nombreServicio, nombreCategoria) as Servicio, nombreCategoria as Categoria
    From servicios
    INNER JOIN categoriasservicios on servicios.idCategoriaServicio = categoriasservicios.idCategoriaServicio;
    
    DROP VIEW IF EXISTS Cotizacion_Cliente;
    
    CREATE VIEW Cotizacion_Cliente AS 
	SELECT concat(nombre, " ", apellido) as Nombre_Usuario, fechaCotizacion as Fecha, totalCotizacion as Total
    From cotizaciones
    INNER JOIN Clientes on Cotizaciones.idCliente = Clientes.idCliente
    INNER JOIN Usuarios on Clientes.numeroDocumento = Usuarios.numeroDocumento;
    
    DROP VIEW IF EXISTS tecnicosActividadCitaAnalisis;
    
    CREATE VIEW tecnicosActividadCitaAnalisis AS
	SELECT t.idTecnico, t.numeroDocumento, u.nombre, u.apellido
	FROM tecnicos t
	JOIN usuarios u ON t.numeroDocumento = u.numeroDocumento
	JOIN cronogramatecnicos c ON t.idTecnico = c.idTecnico
	JOIN detallesactividadcronograma dac ON c.idCronogramaTecnico = dac.idCronogramaTecnico
	JOIN actividadescronogramatecnicos ac ON dac.idActividadCronogramaTecnico = ac.idActividadCronogramaTecnico
	WHERE ac.idActividadCronogramaTecnico = 1;
	
    DROP VIEW IF EXISTS tecnicosActividadCitaMantenimiento;
    
	CREATE VIEW tecnicosActividadCitaMantenimiento AS
	SELECT t.idTecnico, t.numeroDocumento, u.nombre, u.apellido
	FROM tecnicos t
	JOIN usuarios u ON t.numeroDocumento = u.numeroDocumento
	JOIN cronogramatecnicos c ON t.idTecnico = c.idTecnico
	JOIN detallesactividadcronograma dac ON c.idCronogramaTecnico = dac.idCronogramaTecnico
	JOIN actividadescronogramatecnicos ac ON dac.idActividadCronogramaTecnico = ac.idActividadCronogramaTecnico
	WHERE ac.idActividadCronogramaTecnico= 2;

	DROP VIEW IF EXISTS tecnicosActividadCitaInstalacion;

	CREATE VIEW tecnicosActividadCitaInstalacion AS
	SELECT t.idTecnico, t.numeroDocumento, u.nombre, u.apellido
	FROM tecnicos t
	JOIN usuarios u ON t.numeroDocumento = u.numeroDocumento
	JOIN cronogramatecnicos c ON t.idTecnico = c.idTecnico
	JOIN detallesactividadcronograma dac ON c.idCronogramaTecnico = dac.idCronogramaTecnico
	JOIN actividadescronogramatecnicos ac ON dac.idActividadCronogramaTecnico = ac.idActividadCronogramaTecnico
	WHERE ac.idActividadCronogramaTecnico= 3;

	DROP VIEW IF EXISTS tecnicosActividadEntregaEnvio;

	CREATE VIEW tecnicosActividadEntregaEnvio AS
	SELECT t.idTecnico, t.numeroDocumento, u.nombre, u.apellido
	FROM tecnicos t
	JOIN usuarios u ON t.numeroDocumento = u.numeroDocumento
	JOIN cronogramatecnicos c ON t.idTecnico = c.idTecnico
	JOIN detallesactividadcronograma dac ON c.idCronogramaTecnico = dac.idCronogramaTecnico
	JOIN actividadescronogramatecnicos ac ON dac.idActividadCronogramaTecnico = ac.idActividadCronogramaTecnico
	WHERE ac.idActividadCronogramaTecnico = 4;

	DROP VIEW IF EXISTS consultarEnvios;

	CREATE VIEW consultarEnvios
	AS SELECT envios.idEnvio, estadosenvios.nombreEstadoEnvio, envios.direccionEnvio,
	tecnicos.idTecnico
	FROM estadosenvios
	JOIN envios ON envios.idEstadoEnvio = estadosenvios.idEstadoEnvio
	JOIN tecnicos ON tecnicos.idTecnico = envios.idTecnico;
    
	DROP VIEW IF EXISTS consultarQuejas;
    
    	CREATE VIEW consultarQuejas AS
	SELECT idPQRSF, fechaPQRSF, informacionPQRSF, c.idCliente, nombreEstadoPQRSF
	FROM PQRSF
	JOIN Clientes c ON PQRSF.idCliente = c.idCliente
	JOIN EstadosPQRSF e ON PQRSF.idEstadoPQRSF = e.idEstadoPQRSF
	WHERE idTipoPQRSF = 2;

	DROP VIEW IF EXISTS Detalle_Envios;

	CREATE VIEW Detalle_Envios AS 
	SELECT envios.idEnvio, envios.direccionEnvio, tecnicos.numeroDocumento, estadosenvios.nombreEstadoEnvio
	FROM envios
	INNER JOIN tecnicos ON envios.idTecnico = tecnicos.idTecnico
	INNER JOIN estadosenvios ON envios.idEstadoEnvio = estadosenvios.idEstadoEnvio;

    DROP VIEW IF EXISTS detalle_envios_y_ventas;

    CREATE VIEW detalle_envios_y_ventas AS
    SELECT
        e.idEnvio AS idEnvio,
        e.direccionEnvio AS direccionEnvio,
        dv.detallesVenta AS detallesVenta,
        t.idTecnico AS tecnicoAsignado,
        CONCAT(u.nombre, ' ', u.apellido) AS nombreTecnico,
        t.numeroDocumento AS numeroDocumento,
        v.fechaVenta AS fechaVenta,
        v.idVenta AS idVenta
    FROM
        jjsystem_db.envios e
    JOIN jjsystem_db.ventas v ON e.idEnvio = v.idEnvio
    JOIN jjsystem_db.detallesventas dv ON v.idVenta = dv.idVenta
    JOIN jjsystem_db.tecnicos t ON e.idTecnico = t.idTecnico
    JOIN jjsystem_db.usuarios u ON t.numeroDocumento = u.numeroDocumento
    WHERE
        u.idRol = 3;

    DROP VIEW IF EXISTS VistaEnviosClientes;

    CREATE VIEW VistaEnviosClientes AS
    SELECT
        e.idEnvio AS idEnvio,
        e.direccionEnvio AS direccionEnvio,
        e.idTecnico AS idTecnico,
        e.idEstadoEnvio AS idEstadoEnvio,
        c.idCliente AS idCliente,
        c.direccionCliente AS direccionCliente,
        c.numeroDocumento AS documentoCliente
    FROM
        jjsystem_db.envios e
    JOIN jjsystem_db.clientes c ON e.direccionEnvio = c.direccionCliente;


/*Procedimiento*/


DROP PROCEDURE IF EXISTS CrearProducto;
    DELIMITER //
	CREATE PROCEDURE CrearProducto(
		IN p_nombreProducto TEXT(100),
		IN p_descripcionProducto TEXT(200),
		IN p_precioProducto FLOAT,
		IN p_cantidad INT,
        IN p_idAdministrador INT,
        IN p_idCategoriaProducto INT,
        IN p_idProveedorProducto INT
	)
	BEGIN
		INSERT INTO productos (nombreProducto, descripcionProducto, precioProducto, cantidad, idAdministrador , idCategoriaProducto, idProveedorProducto )
		VALUES (p_nombreProducto,p_descripcionProducto, p_precioProducto, p_cantidad, p_idAdministrador, p_idCategoriaProducto, p_idProveedorProducto );
	END //
	DELIMITER ;
    
    DROP PROCEDURE IF EXISTS CrearServicio;
    DELIMITER //
    CREATE PROCEDURE CrearServicio(
		IN p_nombreServicio TEXT(100),
		IN p_descripcionServicio TEXT(200),
		IN p_idCategoriaServicio INT
    )
	BEGIN
		INSERT INTO servicios (nombreServicio, descripcionServicio, idCategoriaServicio)
		VALUES (p_nombreServicio, p_descripcionServicio, p_idCategoriaServicio);
	END //
	DELIMITER ;

    DROP PROCEDURE IF EXISTS AsignarActividad;
	
    DELIMITER //
	CREATE PROCEDURE AsignarActividad(
		IN p_idTecnico INT,
		IN p_idActividadCronogramaTecnico INT,
		IN p_idCita INT,
		IN p_fechaActividadCronograma DATETIME
	)
	BEGIN
		DECLARE idCronogramaTecnico INT;
		SELECT MAX(idCronogramaTecnico) INTO idCronogramaTecnico FROM cronogramatecnicos;
		INSERT INTO detallesactividadcronograma (idCronogramaTecnico, idActividadCronogramaTecnico, fechaActividadCronograma)
		VALUES (idCronogramaTecnico, p_idActividadCronogramaTecnico, p_fechaActividadCronograma);
		UPDATE CronogramaTecnicos
		SET Tecnico_idTecnico = p_idTecnico
		WHERE Cita_idCita = p_idCita;
	END //
	DELIMITER ;

    DROP PROCEDURE IF EXISTS RegistrarEnvio;
    DELIMITER //
	CREATE PROCEDURE RegistrarEnvio(
	    IN p_direccionEnvio VARCHAR(255),
	    IN p_idTecnico INT,
	    IN p_idEstadoEnvio INT
	)
	BEGIN
	    INSERT INTO envios (direccionEnvio, idTecnico, idEstadoEnvio)
	    VALUES (p_direccionEnvio, p_idTecnico, p_idEstadoEnvio);
	END //
	DELIMITER ;

   DROP PROCEDURE IF EXISTS RegistrarPQRSF;
   DELIMITER //
	CREATE PROCEDURE RegistrarPQRSF(
	    IN p_fechaPQRSF DATE,
	    IN p_informacionPQRSF TEXT(200),
	    IN p_idCliente INT,
	    IN p_idEstadoPQRSF INT,
	    IN p_idTipoPQRSF INT
	)
	BEGIN
	    INSERT INTO PQRSF (fechaPQRSF, informacionPQRSF, idCliente, idEstadoPQRSF, idTipoPQRSF)
	    VALUES (p_fechaPQRSF, p_informacionPQRSF, p_idCliente, p_idEstadoPQRSF, p_idTipoPQRSF); 
	END //
	DELIMITER ;


/*Trigger*/

DELIMITER //
    CREATE TRIGGER asignarCategoriaProducto
    BEFORE INSERT ON productos
    FOR EACH ROW 
    BEGIN 
		IF NEW.nombreProducto LIKE 'Camara%' THEN
			SET NEW.idCategoriaProducto = (SELECT idCategoriaProducto FROM categoriasProducto WHERE nombreCategoria = 'Camara');
		ELSEIF NEW.nombreProducto LIKE 'DVR%' THEN
			SET NEW.idCategoriaProducto = (SELECT idCategoriaProducto FROM categoriasProducto WHERE nombreCategoria = 'DVR');
		ELSEIF NEW.nombreProducto LIKE 'Alarma%' THEN
			SET NEW.idCategoriaProducto = (SELECT idCategoriaProducto FROM categoriasProducto WHERE nombreCategoria = 'Alarma');
		ELSEIF NEW.nombreProducto LIKE 'Sensor%' THEN
			SET NEW.idCategoriaProducto = (SELECT idCategoriaProducto FROM categoriasProducto WHERE nombreCategoria = 'Sensor');
		ELSE 
			SET NEW.idCategoriaProducto = NULL;
		END IF;
	END;

    
	DROP TRIGGER IF EXISTS Cotizaciones;
    
    DELIMITER //
	CREATE TRIGGER cotizacionesHistorial
	AFTER UPDATE ON historialCotizaciones
	FOR EACH ROW
	BEGIN
		INSERT INTO cotizacionesHistorial (idCotizacion, fechaCreada, fechaActualizacion)
        VALUES (NEW.idCotizacion, NOW(), NEW.fechaActualizacion);
	END; //
	DELIMITER ;

	DROP TABLE IF EXISTS enviosEntregados;
	CREATE table enviosEntregados (
    idEnvio int primary key,
    fecha datetime, idTecnicoEncargado int, documentoTecnico bigint);
	DROP TRIGGER IF EXISTS enviosEntregados;
    DELIMITER //
CREATE TRIGGER enviosEntregados
AFTER UPDATE ON envios
FOR EACH ROW
BEGIN
	IF NEW.idEstadoEnvio = 3 THEN
		INSERT INTO enviosEntregados (idEnvio, fecha, idTecnicoEncargado, documentoTecnico)
		SELECT NEW.idEnvio, NOW(), tecnicos.idTecnico, tecnicos.numeroDocumento
		FROM tecnicos
		WHERE tecnicos.idTecnico = NEW.idTecnico;
	END IF;
END //
DELIMITER ;

UPDATE envios SET idEstadoEnvio = '3' WHERE envios.idEnvio = 7;

CREATE TABLE IF NOT EXISTS historialPQRSFporTipoEstado (
	idRegistro INT AUTO_INCREMENT PRIMARY KEY,
	idPQRSF INT,
	idTipoPQRSF INT,
	idEstadoPQRSF INT,
	fechaRegistro DATETIME,
    foreign key(idPQRSF) references PQRSF (idPQRSF)
);

DELIMITER //
CREATE TRIGGER registroPQRSFPorTipoEstado
AFTER INSERT ON PQRSF
FOR EACH ROW
BEGIN
	INSERT INTO historialPQRSFporTipoEstado (idPQRSF, idTipoPQRSF, idEstadoPQRSF, fechaRegistro)
	SELECT NEW.idPQRSF, NEW.idTipoPQRSF, NEW.idEstadoPQRSF, NOW();
END; //
DELIMITER ;

use jjsystem_db;

DELIMITER //
CREATE TRIGGER crear_cliente_desde_usuario
AFTER INSERT ON usuarios
FOR EACH ROW
BEGIN
    IF NEW.idrol = 2 THEN
        -- Insertar el cliente con la dirección fija para usuarios con idrol = 2
        INSERT INTO clientes (direccioncliente, numerodocumento) 
        VALUES ('Dirección por defecto', NEW.numerodocumento);
    END IF;
END;
//

DROP trigger IF exists usuario_tecnico;

DELIMITER //
CREATE TRIGGER usuario_tecnico
AFTER INSERT ON usuarios
FOR EACH ROW
BEGIN
    IF NEW.idRol = 3 THEN
        INSERT INTO tecnicos (id_especialidad_fk, numeroDocumento) VALUES ('1', NEW.numeroDocumento);
    END IF;
END;
//
DELIMITER ;
DROP TRIGGER IF EXISTS usuario_administrador;

DELIMITER //
CREATE TRIGGER usuario_administrador
AFTER INSERT ON usuarios
FOR EACH ROW
BEGIN
    IF NEW.idRol = 1 THEN
        INSERT INTO administrador (numeroDocumento) VALUES (NEW.numeroDocumento);
    END IF;
END;
//
DELIMITER ;


DROP PROCEDURE IF EXISTS ObtenerDetallesCotizacion;
DELIMITER //

CREATE PROCEDURE ObtenerDetallesCotizacion(IN id_cotizacion INT)
BEGIN
    SELECT 
        cotizaciones.idCotizacion, 
        cotizaciones.fechaCotizacion, 
        cotizaciones.descripcionCotizacion,
        estadoscotizaciones.nombreEstadoCotizacion AS nombreEstado,
        productos.idProducto, 
        productos.nombreProducto, 
        productos.descripcionProducto, 
        productos.precioProducto,
        servicios.idServicio,
        servicios.nombreServicio,
        servicios.descripcionServicio,
        servicios.precioServicio
    FROM 
        cotizaciones
    LEFT JOIN 
        cotizaciones_productos ON cotizaciones.idCotizacion = cotizaciones_productos.idCotizacion
    LEFT JOIN 
        productos ON cotizaciones_productos.idProducto = productos.idProducto
    LEFT JOIN 
        cotizaciones_servicios ON cotizaciones.idCotizacion = cotizaciones_servicios.idCotizacion
    LEFT JOIN 
        servicios ON cotizaciones_servicios.idServicio = servicios.idServicio
    LEFT JOIN 
        estadoscotizaciones ON cotizaciones.idEstadoCotizacion = estadoscotizaciones.idEstadoCotizacion
    WHERE 
        cotizaciones.idCotizacion = id_cotizacion;
END //

DELIMITER ;

DELIMITER ;