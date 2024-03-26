use jjsystem_db;
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