# 🎵 Sistema de Gestión - La Escuelita Germán Simán (Conectado a Supabase Cloud)

Sistema web integral conectado en vivo a la base de datos PostgreSQL en la nube de **Supabase** (`ptnbtgnjcaxaucekkfqa`).

---

## ⚡ Conexión en Vivo con Supabase
El sistema se encuentra sincronizado con tu base en la nube:
* **Host Cloud:** `https://ptnbtgnjcaxaucekkfqa.supabase.co`
* **Tablas en la nube utilizadas:**
  * `students`: Alumnos (nombre, apellido, email, teléfono, fecha de nacimiento).
  * `courses`: Cursos (nombre, costo, período de pago, día de vencimiento, descripción).
  * `course_students`: Asignaciones / Matriculaciones de alumnos a cursos con estado.
  * `payments`: Registro y control de cobros.

---

## 🚀 Cómo Iniciar el Sistema en tu Computadora

1. Haz doble clic en el archivo **`iniciar.bat`** (o ejecuta en la terminal: `python app.py`).
2. Abre tu navegador web en:
   👉 **[http://localhost:5000](http://localhost:5000)**

---

## 📋 Funcionalidades Principales

1. **Panel de Control (Dashboard):**
   * Indicador de estado en vivo **Supabase Cloud**.
   * Métricas en tiempo real de alumnos registrados, cursos activos y total de matriculaciones.
   * Proyección y cálculo de recaudación mensual acumulada.
   * Ranking de cursos con mayor cantidad de inscriptos.

2. **Gestión de Alumnos (`/alumnos`):**
   * Alta con validación directa en Supabase: Nombre, Apellido, Email único, Teléfono y Fecha de Nacimiento.
   * Búsqueda instantánea en tiempo real.
   * Edición y baja con confirmación de seguridad.
   * Vista de cantidad y nombres de cursos a los que asiste cada estudiante.

3. **Cursos y Aranceles (`/cursos`):**
   * Nombre del curso, arancel / costo y descripción.
   * Período de pago: *Mensual*, *Quincenal*, *Bimestral*, *Semestral*, *Anual*, *Pago Único*.
   * Día límite de pago mensual (ej: día 10 de cada mes).
   * Vista de detalle del curso (`/cursos/<id>`) para consultar todos los alumnos matriculados e inscribir nuevos alumnos rápidamente.

4. **Inscripciones (`/inscripciones`):**
   * Asignar alumnos a cursos sin duplicar registros.
   * Modificar el estado de la cursada (*Activo*, *Pausado*, *Finalizado*).
   * Desasignar o dar de baja asignaciones.

5. **Visualizador de Scripts SQL (`/scripts-sql`):**
   * Vista y botón de copiado de los scripts para Supabase, MySQL, PostgreSQL y SQLite.
