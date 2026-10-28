-- ====================================================================
-- SISTEMA DE GESTION: LA ESCUELITA GERMAN SIMAN
-- SCRIPT DE BASE DE DATOS (POSTGRESQL)
-- ====================================================================

-- 1. TABLA: ALUMNOS
CREATE TABLE IF NOT EXISTS alumnos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    telefono VARCHAR(50),
    fecha_nacimiento DATE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. TABLA: CURSOS
CREATE TABLE IF NOT EXISTS cursos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    costo NUMERIC(10, 2) NOT NULL DEFAULT 0.00,
    periodo_pago VARCHAR(50) DEFAULT 'Mensual', -- Mensual, Quincenal, Bimestral, Semestral, Anual, Pago Unico
    dia_vencimiento INT DEFAULT 10,             -- Dia del mes limite de pago
    fecha_limite_pago DATE NULL,                -- Fecha limite puntual
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. TABLA: INSCRIPCIONES
CREATE TABLE IF NOT EXISTS inscripciones (
    id SERIAL PRIMARY KEY,
    alumno_id INT NOT NULL REFERENCES alumnos(id) ON DELETE CASCADE,
    curso_id INT NOT NULL REFERENCES cursos(id) ON DELETE CASCADE,
    fecha_inscripcion DATE NOT NULL DEFAULT CURRENT_DATE,
    estado VARCHAR(50) DEFAULT 'Activo',
    observaciones TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_alumno_curso UNIQUE (alumno_id, curso_id)
);

-- 4. TABLA: PAGOS
CREATE TABLE IF NOT EXISTS pagos (
    id SERIAL PRIMARY KEY,
    inscripcion_id INT NOT NULL REFERENCES inscripciones(id) ON DELETE CASCADE,
    monto NUMERIC(10, 2) NOT NULL,
    periodo_cubierto VARCHAR(50) NOT NULL,
    fecha_vencimiento DATE,
    fecha_pago DATE NULL,
    estado VARCHAR(50) DEFAULT 'Pendiente',
    metodo_pago VARCHAR(50) NULL,
    observaciones TEXT
);

-- ====================================================================
-- DATOS DE EJEMPLO
-- ====================================================================
INSERT INTO alumnos (nombre, apellido, email, telefono, fecha_nacimiento) VALUES
('Lucas', 'Martinez', 'lucas.martinez@gmail.com', '11-4567-8901', '2005-04-12'),
('Sofia', 'Fernandez', 'sofia.fernandez@hotmail.com', '11-9876-5432', '2008-09-23'),
('Joaquin', 'Gomez', 'joaco.gomez@gmail.com', '11-2345-6789', '2002-11-05')
ON CONFLICT (email) DO NOTHING;

INSERT INTO cursos (nombre, descripcion, costo, periodo_pago, dia_vencimiento, fecha_limite_pago, activo) VALUES
('Batería y Ritmo', 'Clases individuales y práctica rítmica', 35000.00, 'Mensual', 10, NULL, TRUE),
('Guitarra Criolla y Eléctrica', 'Acordes, armonía y técnica', 30000.00, 'Mensual', 10, NULL, TRUE),
('Taller Intensivo de Canto', 'Técnica vocal y respiración - 4 clases', 25000.00, 'Pago Unico', NULL, '2026-11-30', TRUE);

INSERT INTO inscripciones (alumno_id, curso_id, fecha_inscripcion, estado) VALUES
(1, 1, '2026-10-01', 'Activo'),
(2, 2, '2026-10-05', 'Activo'),
(3, 1, '2026-10-10', 'Activo')
ON CONFLICT (alumno_id, curso_id) DO NOTHING;
