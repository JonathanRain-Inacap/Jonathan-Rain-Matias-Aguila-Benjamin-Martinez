CREATE TABLE usuario (
    id        NUMBER GENERATED ALWAYS AS IDENTITY,
    nombre    VARCHAR2(100) NOT NULL,
    correo    VARCHAR2(150) NOT NULL,
    password  VARCHAR2(255) NOT NULL,   
    CONSTRAINT pk_usuario PRIMARY KEY (id),
    CONSTRAINT uq_usuario_correo UNIQUE (correo)
);

CREATE TABLE departamento (
    id_departamento  NUMBER GENERATED ALWAYS AS IDENTITY,
    nombre           VARCHAR2(100) NOT NULL,
    CONSTRAINT pk_departamento PRIMARY KEY (id_departamento),
    CONSTRAINT uq_departamento_nombre UNIQUE (nombre)
);

CREATE TABLE empleado (
    id_usuario       NUMBER,
    direccion        VARCHAR2(200),
    telefono         VARCHAR2(20),
    fecha_inicio     DATE NOT NULL,
    salario          NUMBER(12,2),
    id_departamento  NUMBER NOT NULL,
    CONSTRAINT pk_empleado PRIMARY KEY (id_usuario),
    CONSTRAINT fk_empleado_usuario
        FOREIGN KEY (id_usuario) REFERENCES usuario (id),
    CONSTRAINT fk_empleado_departamento
        FOREIGN KEY (id_departamento) REFERENCES departamento (id_departamento),
    CONSTRAINT ck_empleado_salario CHECK (salario >= 0)
);


CREATE TABLE administrador_rrhh (
    id_usuario    NUMBER,
    nivel_acceso  NUMBER(2) NOT NULL,
    CONSTRAINT pk_admin_rrhh PRIMARY KEY (id_usuario),
    CONSTRAINT fk_admin_rrhh_usuario
        FOREIGN KEY (id_usuario) REFERENCES usuario (id)
);

CREATE TABLE proyecto (
    id_proyecto   NUMBER GENERATED ALWAYS AS IDENTITY,
    nombre        VARCHAR2(100) NOT NULL,
    descripcion   VARCHAR2(500),
    fecha_inicio  DATE NOT NULL,
    CONSTRAINT pk_proyecto PRIMARY KEY (id_proyecto)
);

CREATE TABLE empleado_proyecto (
    id_usuario   NUMBER,
    id_proyecto  NUMBER,
    CONSTRAINT pk_empleado_proyecto PRIMARY KEY (id_usuario, id_proyecto),
    CONSTRAINT fk_ep_empleado
        FOREIGN KEY (id_usuario) REFERENCES empleado (id_usuario),
    CONSTRAINT fk_ep_proyecto
        FOREIGN KEY (id_proyecto) REFERENCES proyecto (id_proyecto)
);

CREATE TABLE registro_tiempo (
    id_registro       NUMBER GENERATED ALWAYS AS IDENTITY,
    fecha             DATE NOT NULL,
    horas_trabajadas  NUMBER(5,2) NOT NULL,
    descripcion       VARCHAR2(300),
    id_usuario        NUMBER NOT NULL,
    id_proyecto       NUMBER NOT NULL,
    CONSTRAINT pk_registro_tiempo PRIMARY KEY (id_registro),
    CONSTRAINT fk_rt_empleado
        FOREIGN KEY (id_usuario) REFERENCES empleado (id_usuario),
    CONSTRAINT fk_rt_proyecto
        FOREIGN KEY (id_proyecto) REFERENCES proyecto (id_proyecto),
    CONSTRAINT ck_rt_horas CHECK (horas_trabajadas > 0 AND horas_trabajadas <= 24)
);

CREATE INDEX idx_empleado_depto ON empleado (id_departamento);
CREATE INDEX idx_rt_empleado    ON registro_tiempo (id_usuario);
CREATE INDEX idx_rt_proyecto    ON registro_tiempo (id_proyecto);
CREATE INDEX idx_ep_proyecto    ON empleado_proyecto (id_proyecto);
