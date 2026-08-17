USE Clinica_Dental;
GO

-- 0) Vaciar la tabla de prueba (ajusta si tienes datos que conservar)
DELETE FROM ServiciosBrindados;

-- 1) Quitar la FK vieja de id_servicio (si existe) y la columna misma
DECLARE @fkServicio nvarchar(200);
SELECT @fkServicio = fk.name FROM sys.foreign_keys fk
JOIN sys.foreign_key_columns fkc ON fkc.constraint_object_id = fk.object_id
JOIN sys.columns c ON c.object_id = fkc.parent_object_id AND c.column_id = fkc.parent_column_id
WHERE fk.parent_object_id = OBJECT_ID('ServiciosBrindados') AND c.name = 'id_servicio';
IF @fkServicio IS NOT NULL EXEC('ALTER TABLE ServiciosBrindados DROP CONSTRAINT ' + @fkServicio);

ALTER TABLE ServiciosBrindados DROP COLUMN id_servicio;

-- 2) Confirmar que id_cita sea IDENTITY (autogenerado), igual que hicimos con Encargados/MenoresEdad
DECLARE @pkCita nvarchar(200);
SELECT @pkCita = kc.name FROM sys.key_constraints kc
WHERE kc.parent_object_id = OBJECT_ID('ServiciosBrindados') AND kc.type = 'PK';
IF @pkCita IS NOT NULL EXEC('ALTER TABLE ServiciosBrindados DROP CONSTRAINT ' + @pkCita);
ALTER TABLE ServiciosBrindados DROP COLUMN id_cita;
ALTER TABLE ServiciosBrindados ADD id_cita INT IDENTITY(1,1) PRIMARY KEY;

-- 3) Confirmar/crear las FKs que sí se quedan en ServiciosBrindados
ALTER TABLE ServiciosBrindados ADD CONSTRAINT FK_ServiciosBrindados_MenoresEdad
    FOREIGN KEY (id_menor_edad) REFERENCES MenoresEdad(id_menor_edad);

ALTER TABLE ServiciosBrindados ADD CONSTRAINT FK_ServiciosBrindados_Funcionario
    FOREIGN KEY (id_funcionario) REFERENCES Funcionario(id_funcionario);

-- 4) Crear la tabla de detalle (relación muchos-a-muchos entre citas y servicios)
CREATE TABLE DetalleServiciosBrindados (
    id_cita INT NOT NULL,
    id_servicio VARCHAR(20) NOT NULL,
    CONSTRAINT PK_DetalleServiciosBrindados PRIMARY KEY (id_cita, id_servicio),
    CONSTRAINT FK_Detalle_Cita FOREIGN KEY (id_cita) REFERENCES ServiciosBrindados(id_cita),
    CONSTRAINT FK_Detalle_Servicio FOREIGN KEY (id_servicio) REFERENCES ServiciosDisponibles(id_servicio)
);