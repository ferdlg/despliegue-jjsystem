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
    idproducto INT NOT NULL AUTO_INCREMENT,
    nombreProducto TEXT(100) NOT NULL,
    descripcionProducto TEXT(200) NOT NULL,
    precioProducto FLOAT NOT NULL,
    cantidad INT NOT NULL,
    imagen VARCHAR(200) NULL,
    idAdministrador INT,
    idCategoriaProducto INT,
    idProveedorProducto INT,
    PRIMARY KEY(idproducto),
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
    idproducto INT,
    cantidad INT,
    FOREIGN KEY (idCotizacion) REFERENCES Cotizaciones (idCotizacion),
    FOREIGN KEY (idproducto) REFERENCES Productos (idproducto)
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
    horaCita TIME NOT NULL,
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

-- DROP VIEW IF EXISTS consultarEnvios;

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

    DROP VIEW IF EXISTS EnviosUsuarios;

    CREATE VIEW EnviosUsuarios AS
    SELECT 
        usuarios.email AS emailCliente,
        usuarios.nombre AS nombreCliente,
        usuarios.apellido AS apellidoCliente,
        usuarios.numeroDocumento AS numeroDocumentoCliente,
        envios.idEnvio,
        envios.direccionEnvio
    FROM 
        Ventas AS ventas
    JOIN 
        Cotizaciones AS cotizaciones ON ventas.idCotizacion = cotizaciones.idCotizacion
    JOIN 
        Clientes AS clientes ON cotizaciones.idCliente = clientes.idCliente
    JOIN 
        Envios AS envios ON ventas.idEnvio = envios.idEnvio
    JOIN 
        Usuarios AS usuarios ON clientes.numeroDocumento = usuarios.numeroDocumento;


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


USE jjsystem_db;
DROP PROCEDURE IF EXISTS ObtenerDetallesCotizacion;
DELIMITER //

CREATE PROCEDURE ObtenerDetallesCotizacion(IN id_cotizacion INT)
BEGIN
    SELECT 
        cotizaciones.idCotizacion, 
        cotizaciones.fechaCotizacion, 
        cotizaciones.descripcionCotizacion,
        estadoscotizaciones.nombreEstadoCotizacion AS nombreEstado,
        productos.idproducto, 
        productos.nombreProducto, 
        productos.descripcionProducto, 
        productos.precioProducto,
        cotizaciones_productos.cantidad AS cantidadProducto,
        servicios.idServicio,
        servicios.nombreServicio,
        servicios.descripcionServicio,
        servicios.precioServicio
    FROM 
        cotizaciones
    LEFT JOIN 
        cotizaciones_productos ON cotizaciones.idCotizacion = cotizaciones_productos.idCotizacion
    LEFT JOIN 
        productos ON cotizaciones_productos.idproducto = productos.idproducto
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
DELIMITER ;

DELIMITER ;

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
    (1021826839, 'Admin', 'Admin', 'adminadmin@gmail.com', 'argon2$argon2id$v=19$m=102400,t=2,p=8$NGtaaTVCTVgzbG9tblppRmpwbzc3Vw$90sl4TC+9JodIk1WsTfNLucfaC7vFCQItXbi7hxLbNw', 3208285814, 1, 1);

-- Inserción de clientes
-- Inserción de administradores
-- Inserción de especialidad de técnicos
INSERT INTO Especialidad_tecnicos(nombre_especialidad)
VALUES
	('Analisis'),
    ('Instalacion'),
    ('Mantenimiento');
-- Inserción de técnicos
-- Inserción de estados de envío
INSERT INTO EstadosEnvios (nombreEstadoEnvio)
VALUES
    ('En bodega'),
    ('Llegando'),
    ('Entregado');

-- Inserción de envíos
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

INSERT INTO EstadosCitas (nombreEstadoCita)
VALUES
	('Confirmada'),
	('Cancelada'),
	('Modificada'),
    ('Programada'),
    ('Finalizada');

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