-- ====================================================================
-- SISTEMA DE GESTION: LA ESCUELITA GERMAN SIMAN
-- SCRIPT DE BASE DE DATOS (MYSQL / MARIADB)
-- ====================================================================

CREATE DATABASE IF NOT EXISTS escuelita_musica 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE escuelita_musica;

-- 1. TABLA: ALUMNOS
CREATE TABLE IF NOT EXISTS alumnos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    telefono VARCHAR(50),
    fecha_nacimiento DATE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- 2. TABLA: CURSOS
CREATE TABLE IF NOT EXISTS cursos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    costo DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    periodo_pago ENUM('Mensual', 'Quincenal', 'Bimestral', 'Semestral', 'Anual', 'Pago Unico') DEFAULT 'Mensual',
    dia_vencimiento INT DEFAULT 10, -- Día del mes límite de pago (1 al 31)
    fecha_limite_pago DATE NULL,     -- Fecha límite puntual para cursos especiales o intensivos
    activo TINYINT(1) DEFAULT 1,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- 3. TABLA: INSCRIPCIONES (Asignación de Alumnos a Cursos)
CREATE TABLE IF NOT EXISTS inscripciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    alumno_id INT NOT NULL,
    curso_id INT NOT NULL,
    fecha_inscripcion DATE NOT NULL,
    estado ENUM('Activo', 'Pausado', 'Finalizado') DEFAULT 'Activo',
    observaciones TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_inscripcion_alumno FOREIGN KEY (alumno_id) REFERENCES alumnos(id) ON DELETE CASCADE,
    CONSTRAINT fk_inscripcion_curso FOREIGN KEY (curso_id) REFERENCES cursos(id) ON DELETE CASCADE,
    CONSTRAINT uq_alumno_curso UNIQUE (alumno_id, curso_id)
) ENGINE=InnoDB;

-- 4. TABLA: PAGOS / CUOTAS (Opcional para control de cobros del periodo)
CREATE TABLE IF NOT EXISTS pagos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    inscripcion_id INT NOT NULL,
    monto DECIMAL(10, 2) NOT NULL,
    periodo_cubierto VARCHAR(50) NOT NULL, -- Ej: "Noviembre 2026"
    fecha_vencimiento DATE,
    fecha_pago DATE NULL,
    estado ENUM('Pendiente', 'Pagado', 'Vencido') DEFAULT 'Pendiente',
    metodo_pago VARCHAR(50) NULL,           -- Efectivo, Transferencia, Tarjeta
    observaciones TEXT,
    CONSTRAINT fk_pago_inscripcion FOREIGN KEY (inscripcion_id) REFERENCES inscripciones(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ====================================================================
-- DATOS DE EJEMPLO INICIALES (DEMO)
-- ====================================================================
INSERT INTO alumnos (nombre, apellido, email, telefono, fecha_nacimiento) VALUES
('Lucas', 'Martinez', 'lucas.martinez@gmail.com', '11-4567-8901', '2005-04-12'),
('Sofia', 'Fernandez', 'sofia.fernandez@hotmail.com', '11-9876-5432', '2008-09-23'),
('Joaquin', 'Gomez', 'joaco.gomez@gmail.com', '11-2345-6789', '2002-11-05');

INSERT INTO cursos (nombre, descripcion, costo, periodo_pago, dia_vencimiento, fecha_limite_pago, activo) VALUES
('Batería y Ritmo', 'Clases individuales y práctica rítmica', 35000.00, 'Mensual', 10, NULL, 1),
('Guitarra Criolla y Eléctrica', 'Acordes, armonía y técnica', 30000.00, 'Mensual', 10, NULL, 1),
('Taller Intensivo de Canto', 'Técnica vocal y respiración - 4 clases', 25000.00, 'Pago Unico', NULL, '2026-11-30', 1);

INSERT INTO inscripciones (alumno_id, curso_id, fecha_inscripcion, estado) VALUES
(1, 1, '2026-10-01', 'Activo'),
(2, 2, '2026-10-05', 'Activo'),
(3, 1, '2026-10-10', 'Activo');
