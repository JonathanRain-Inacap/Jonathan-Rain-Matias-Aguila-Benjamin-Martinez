INSERT INTO usuario (nombre, correo, password)
VALUES ('Juan Perez', 'juan@ecotech.cl', '1234');

INSERT INTO usuario (nombre, correo, password)
VALUES ('Maria Gonzalez', 'maria@ecotech.cl', '1234');

INSERT INTO usuario (nombre, correo, password)
VALUES ('Pedro Soto', 'pedro@ecotech.cl', '1234');

INSERT INTO usuario (nombre, correo, password)
VALUES ('Ana Martinez', 'ana@ecotech.cl', '1234');

INSERT INTO usuario (nombre, correo, password)
VALUES ('Carlos Rojas', 'carlos@ecotech.cl', '1234');


INSERT INTO departamento (nombre)
VALUES ('Desarrollo');

INSERT INTO departamento (nombre)
VALUES ('Recursos Humanos');

INSERT INTO departamento (nombre)
VALUES ('Soporte');


INSERT INTO empleado
(id_usuario, direccion, telefono, fecha_inicio, salario, id_departamento)
VALUES (
    (SELECT id FROM usuario WHERE correo = 'juan@ecotech.cl'),
    'Los Carrera 120',
    '912345678',
    DATE '2026-01-10',
    850000,
    (SELECT id_departamento FROM departamento WHERE nombre = 'Desarrollo')
);

INSERT INTO empleado
(id_usuario, direccion, telefono, fecha_inicio, salario, id_departamento)
VALUES (
    (SELECT id FROM usuario WHERE correo = 'maria@ecotech.cl'),
    'Freire 450',
    '923456789',
    DATE '2026-02-15',
    900000,
    (SELECT id_departamento FROM departamento WHERE nombre = 'Recursos Humanos')
);

INSERT INTO empleado
(id_usuario, direccion, telefono, fecha_inicio, salario, id_departamento)
VALUES (
    (SELECT id FROM usuario WHERE correo = 'pedro@ecotech.cl'),
    'Colon 330',
    '934567890',
    DATE '2026-03-01',
    780000,
    (SELECT id_departamento FROM departamento WHERE nombre = 'Desarrollo')
);

INSERT INTO empleado
(id_usuario, direccion, telefono, fecha_inicio, salario, id_departamento)
VALUES (
    (SELECT id FROM usuario WHERE correo = 'ana@ecotech.cl'), 
    'Av. Siempre Viva 123',                                   
    '+56912345678',                                           
    DATE '2026-10-21',                     
    1500000,                                                  
    1                                                        
);                                                       


-- Administrador RRHH Ecotech
INSERT INTO usuario (nombre, correo, password)
VALUES ('Administrador EcoTech', 'admin@ecotech.cl', '1234');

INSERT INTO administrador_rrhh (id_usuario, nivel_acceso)
VALUES (
    (SELECT id
     FROM usuario
     WHERE correo = 'admin@ecotech.cl'),
    1
);

COMMIT;