from flask import Flask, render_template, request, redirect, url_for, flash
import os
import database.supabase_client as sb

app = Flask(__name__)
app.secret_key = 'escuelita-musica-german-siman-secret-key-2026'

@app.route('/')
def index():
    try:
        students = sb.get_all_students()
        courses = sb.get_all_courses()
        enrollments = sb.get_all_enrollments()
    except Exception as e:
        flash(f'Error al conectar con Supabase: {str(e)}', 'danger')
        students, courses, enrollments = [], [], []

    total_alumnos = len(students)
    total_cursos = len([c for c in courses if c.get('active', True)])
    active_enrollments = [e for e in enrollments if e.get('status') == 'active']
    total_inscripciones = len(active_enrollments)

    # Estimación de recaudación mensual sumando el costo de las asignaciones activas
    recaudacion_estimada = sum(
        float(e.get('courses', {}).get('cost', 0) or 0)
        for e in active_enrollments
        if e.get('courses')
    )

    # Cursos más concurridos
    cursos_populares = sorted(courses, key=lambda c: c.get('students_count', 0), reverse=True)[:5]

    # Últimas inscripciones realizadas
    ultimas_inscripciones = enrollments[:6]

    return render_template('index.html',
                           total_alumnos=total_alumnos,
                           total_cursos=total_cursos,
                           total_inscripciones=total_inscripciones,
                           recaudacion_estimada=recaudacion_estimada,
                           cursos_populares=cursos_populares,
                           ultimas_inscripciones=ultimas_inscripciones,
                           modo_nube=True)

# ====================================================================
# MODULO: ALUMNOS
# ====================================================================
@app.route('/alumnos')
def alumnos_lista():
    students = sb.get_all_students()
    return render_template('alumnos.html', alumnos=students)

@app.route('/alumnos/crear', methods=['POST'])
def alumno_crear():
    nombre = request.form.get('nombre', '').strip()
    apellido = request.form.get('apellido', '').strip()
    email = request.form.get('email', '').strip()
    telefono = request.form.get('telefono', '').strip()
    fecha_nacimiento = request.form.get('fecha_nacimiento', '').strip() or None

    if not nombre or not apellido or not email:
        flash('El nombre, apellido y correo electrónico son obligatorios.', 'danger')
        return redirect(url_for('alumnos_lista'))

    res, err = sb.create_student(nombre, apellido, email, telefono, fecha_nacimiento)
    if err:
        if 'duplicate' in err.lower() or 'unique' in err.lower():
            flash('Ya existe un alumno con ese correo electrónico en la base de datos.', 'danger')
        else:
            flash(f'Error al registrar en Supabase: {err}', 'danger')
    else:
        flash(f'Alumno {nombre} {apellido} registrado con éxito en Supabase.', 'success')

    return redirect(url_for('alumnos_lista'))

@app.route('/alumnos/<student_id>/editar', methods=['POST'])
def alumno_editar(student_id):
    nombre = request.form.get('nombre', '').strip()
    apellido = request.form.get('apellido', '').strip()
    email = request.form.get('email', '').strip()
    telefono = request.form.get('telefono', '').strip()
    fecha_nacimiento = request.form.get('fecha_nacimiento', '').strip() or None

    if not nombre or not apellido or not email:
        flash('Nombre, apellido y correo son obligatorios.', 'danger')
        return redirect(url_for('alumnos_lista'))

    ok, err = sb.update_student(student_id, nombre, apellido, email, telefono, fecha_nacimiento)
    if ok:
        flash('Datos del alumno actualizados en Supabase.', 'success')
    else:
        flash(f'Error al actualizar alumno: {err}', 'danger')

    return redirect(url_for('alumnos_lista'))

@app.route('/alumnos/<student_id>/eliminar', methods=['POST'])
def alumno_eliminar(student_id):
    ok, err = sb.delete_student(student_id)
    if ok:
        flash('Alumno eliminado de Supabase correctamente.', 'success')
    else:
        flash(f'Error al eliminar alumno: {err}', 'danger')
    return redirect(url_for('alumnos_lista'))

# ====================================================================
# MODULO: CURSOS
# ====================================================================
@app.route('/cursos')
def cursos_lista():
    cursos = sb.get_all_courses()
    return render_template('cursos.html', cursos=cursos)

@app.route('/cursos/crear', methods=['POST'])
def curso_crear():
    nombre = request.form.get('nombre', '').strip()
    descripcion = request.form.get('descripcion', '').strip()
    costo = request.form.get('costo', '0').strip()
    periodo_pago = request.form.get('periodo_pago', 'Mensual').strip()
    dia_vencimiento = request.form.get('dia_vencimiento', '10').strip()

    if not nombre:
        flash('El nombre del curso es obligatorio.', 'danger')
        return redirect(url_for('cursos_lista'))

    res, err = sb.create_course(nombre, descripcion, costo, periodo_pago, dia_vencimiento)
    if err:
        flash(f'Error al crear el curso en Supabase: {err}', 'danger')
    else:
        flash(f'Curso "{nombre}" guardado con éxito en Supabase.', 'success')

    return redirect(url_for('cursos_lista'))

@app.route('/cursos/<course_id>/editar', methods=['POST'])
def curso_editar(course_id):
    nombre = request.form.get('nombre', '').strip()
    descripcion = request.form.get('descripcion', '').strip()
    costo = request.form.get('costo', '0').strip()
    periodo_pago = request.form.get('periodo_pago', 'Mensual').strip()
    dia_vencimiento = request.form.get('dia_vencimiento', '10').strip()

    if not nombre:
        flash('El nombre del curso es obligatorio.', 'danger')
        return redirect(url_for('cursos_lista'))

    ok, err = sb.update_course(course_id, nombre, descripcion, costo, periodo_pago, dia_vencimiento)
    if ok:
        flash('Curso actualizado con éxito en Supabase.', 'success')
    else:
        flash(f'Error al actualizar el curso: {err}', 'danger')

    return redirect(url_for('cursos_lista'))

@app.route('/cursos/<course_id>/eliminar', methods=['POST'])
def curso_eliminar(course_id):
    ok, err = sb.delete_course(course_id)
    if ok:
        flash('Curso eliminado correctamente de Supabase.', 'success')
    else:
        flash(f'Error al eliminar el curso: {err}', 'danger')
    return redirect(url_for('cursos_lista'))

@app.route('/cursos/<course_id>')
def curso_detalle(course_id):
    curso = sb.get_course_by_id(course_id)
    if not curso:
        flash('El curso solicitado no existe en Supabase.', 'warning')
        return redirect(url_for('cursos_lista'))

    enrollments = sb.get_enrollments_by_course(course_id)
    all_students = sb.get_all_students()

    # Identificar qué alumnos aún no están inscriptos en este curso
    enrolled_student_ids = {e.get('student_id') for e in enrollments}
    no_inscriptos = [s for s in all_students if s.get('id') not in enrolled_student_ids]

    return render_template('curso_detalle.html', 
                           curso=curso, 
                           inscriptos=enrollments, 
                           no_inscriptos=no_inscriptos)

# ====================================================================
# MODULO: INSCRIPCIONES (Asignar Alumnos a Cursos)
# ====================================================================
@app.route('/inscripciones')
def inscripciones_lista():
    inscripciones = sb.get_all_enrollments()
    alumnos = sb.get_all_students()
    cursos = sb.get_all_courses()
    return render_template('inscripciones.html', 
                           inscripciones=inscripciones, 
                           alumnos=alumnos, 
                           cursos=cursos)

@app.route('/inscripciones/crear', methods=['POST'])
def inscripcion_crear():
    alumno_id = request.form.get('alumno_id')
    curso_id = request.form.get('curso_id')
    redirect_to = request.form.get('redirect_to')

    if not alumno_id or not curso_id:
        flash('Debe seleccionar un alumno y un curso.', 'danger')
        return redirect(url_for('inscripciones_lista'))

    res, err = sb.enroll_student(curso_id, alumno_id, status='active')
    if err:
        if 'duplicate' in err.lower() or 'unique' in err.lower():
            flash('El alumno ya está inscripto en este curso.', 'warning')
        else:
            flash(f'Error al asignar alumno: {err}', 'danger')
    else:
        flash('Alumno asignado al curso exitosamente en Supabase.', 'success')

    if redirect_to == 'curso_detalle':
        return redirect(url_for('curso_detalle', course_id=curso_id))
    return redirect(url_for('inscripciones_lista'))

@app.route('/inscripciones/<enrollment_id>/estado', methods=['POST'])
def inscripcion_cambiar_estado(enrollment_id):
    nuevo_estado = request.form.get('estado', 'active')
    redirect_curso = request.form.get('curso_id')

    ok, err = sb.update_enrollment_status(enrollment_id, nuevo_estado)
    if ok:
        flash('Estado de inscripción actualizado en Supabase.', 'success')
    else:
        flash(f'Error al actualizar estado: {err}', 'danger')

    if redirect_curso:
        return redirect(url_for('curso_detalle', course_id=redirect_curso))
    return redirect(url_for('inscripciones_lista'))

@app.route('/inscripciones/<enrollment_id>/eliminar', methods=['POST'])
def inscripcion_eliminar(enrollment_id):
    redirect_curso = request.form.get('curso_id')
    ok, err = sb.delete_enrollment(enrollment_id)
    if ok:
        flash('Asignación eliminada de Supabase correctamente.', 'success')
    else:
        flash(f'Error al eliminar asignación: {err}', 'danger')

    if redirect_curso:
        return redirect(url_for('curso_detalle', course_id=redirect_curso))
    return redirect(url_for('inscripciones_lista'))

# ====================================================================
# MODULO: SCRIPTS SQL
# ====================================================================
@app.route('/scripts-sql')
def scripts_sql():
    base_dir = os.path.dirname(__file__)
    def leer_archivo(nombre):
        try:
            with open(os.path.join(base_dir, 'database', nombre), 'r', encoding='utf-8') as f:
                return f.read()
        except:
            return ""

    script_mysql = leer_archivo('schema_mysql.sql')
    script_postgres = leer_archivo('schema_postgres.sql')
    script_sqlite = leer_archivo('schema_sqlite.sql')
    script_supabase = leer_archivo('schema_supabase.sql')

    return render_template('scripts_sql.html', 
                           script_mysql=script_mysql,
                           script_postgres=script_postgres,
                           script_sqlite=script_sqlite,
                           script_supabase=script_supabase)

if __name__ == '__main__':
    print("==================================================================")
    print(" 🎵 La Escuelita German Siman - Sistema de Gestion")
    print(" ☁️  Conectado en vivo a: Supabase Cloud (ptnbtgnjcaxaucekkfqa)")
    print(" 🚀 Servidor disponible en: http://localhost:5000")
    print("==================================================================")
    app.run(host='0.0.0.0', port=5000, debug=True)
