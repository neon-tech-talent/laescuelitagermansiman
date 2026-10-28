-- ====================================================================
-- SISTEMA DE GESTION: LA ESCUELITA GERMAN SIMAN
-- SCRIPT DE BASE DE DATOS (SQLITE)
-- ====================================================================

PRAGMA foreign_keys = ON;

-- 1. TABLA: ALUMNOS
CREATE TABLE IF NOT EXISTS alumnos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    telefono TEXT,
    fecha_nacimiento TEXT,
    fecha_creacion TEXT DEFAULT (datetime('now', 'localtime'))
);

-- 2. TABLA: CURSOS
CREATE TABLE IF NOT EXISTS cursos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    costo REAL NOT NULL DEFAULT 0.0,
    periodo_pago TEXT NOT NULL DEFAULT 'Mensual', -- Mensual, Quincenal, Bimestral, Semestral, Anual, Pago Único
    dia_vencimiento INTEGER DEFAULT 10,           -- Día del mes para vencimiento (ej: 1 al 31)
    fecha_limite_pago TEXT NULL,                  -- Para cursos puntuales/intensivos con fecha fija
    activo INTEGER DEFAULT 1,
    fecha_creacion TEXT DEFAULT (datetime('now', 'localtime'))
);

-- 3. TABLA: INSCRIPCIONES
CREATE TABLE IF NOT EXISTS inscripciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    alumno_id INTEGER NOT NULL,
    curso_id INTEGER NOT NULL,
    fecha_inscripcion TEXT NOT NULL DEFAULT (date('now', 'localtime')),
    estado TEXT DEFAULT 'Activo', -- Activo, Pausado, Finalizado
    observaciones TEXT,
    fecha_creacion TEXT DEFAULT (datetime('now', 'localtime')),
    FOREIGN KEY (alumno_id) REFERENCES alumnos(id) ON DELETE CASCADE,
    FOREIGN KEY (curso_id) REFERENCES cursos(id) ON DELETE CASCADE,
    UNIQUE(alumno_id, curso_id)
);

-- 4. TABLA: PAGOS
CREATE TABLE IF NOT EXISTS pagos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    inscripcion_id INTEGER NOT NULL,
    monto REAL NOT NULL,
    periodo_cubierto TEXT NOT NULL,
    fecha_vencimiento TEXT,
    fecha_pago TEXT NULL,
    estado TEXT DEFAULT 'Pendiente', -- Pendiente, Pagado, Vencido
    metodo_pago TEXT NULL,
    observaciones TEXT,
    FOREIGN KEY (inscripcion_id) REFERENCES inscripciones(id) ON DELETE CASCADE
);

-- DATOS DE EJEMPLO
INSERT OR IGNORE INTO alumnos (id, nombre, apellido, email, telefono, fecha_nacimiento) VALUES
(1, 'Lucas', 'Martinez', 'lucas.martinez@gmail.com', '11-4567-8901', '2005-04-12'),
(2, 'Sofia', 'Fernandez', 'sofia.fernandez@hotmail.com', '11-9876-5432', '2008-09-23'),
(3, 'Joaquin', 'Gomez', 'joaco.gomez@gmail.com', '11-2345-6789', '2002-11-05');

INSERT OR IGNORE INTO cursos (id, nombre, descripcion, costo, periodo_pago, dia_vencimiento, fecha_limite_pago, activo) VALUES
(1, 'Batería y Ritmo', 'Clases individuales y técnica rítmica con práctica en batería acústica', 35000.0, 'Mensual', 10, NULL, 1),
(2, 'Guitarra Criolla y Eléctrica', 'Acordes, armonía moderna, escalas y repertorio a elección', 30000.0, 'Mensual', 10, NULL, 1),
(3, 'Taller Intensivo de Canto', 'Técnica vocal, respiración y proyección - Taller especial', 25000.0, 'Pago Único', NULL, '2026-11-30', 1);

INSERT OR IGNORE INTO inscripciones (id, alumno_id, curso_id, fecha_inscripcion, estado) VALUES
(1, 1, 1, '2026-10-01', 'Activo'),
(2, 2, 2, '2026-10-05', 'Activo'),
(3, 3, 1, '2026-10-10', 'Activo');
