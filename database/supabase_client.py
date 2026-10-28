import os
import requests

def _load_env():
    """Carga variables desde el archivo .env si existe."""
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    k, v = line.split('=', 1)
                    os.environ.setdefault(k.strip(), v.strip())

_load_env()

SUPABASE_PROJECT_ID = os.environ.get("SUPABASE_PROJECT_ID", "ptnbtgnjcaxaucekkfqa")
SUPABASE_URL = os.environ.get("SUPABASE_URL", f"https://{SUPABASE_PROJECT_ID}.supabase.co")
SUPABASE_SERVICE_ROLE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InB0bmJ0Z25qY2F4YXVjZWtrZnFhIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc5MDY5OTUwNywiZXhwIjoyMTA2Mjc1NTA3fQ.P_FrqIyCmpEL-fJs2qv-2ljHs-nySyvInVZAFATCq5g")

HEADERS = {
    "apikey": SUPABASE_SERVICE_ROLE_KEY,
    "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

# ====================================================================
# OPERACIONES DE ALUMNOS (STUDENTS)
# ====================================================================
def get_all_students():
    """Obtiene todos los alumnos ordenados por apellido."""
    url = f"{SUPABASE_URL}/rest/v1/students?select=*,course_students(id,status,courses(name))&order=last_name.asc"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code == 200:
        students = resp.json()
        for s in students:
            cs = s.get('course_students') or []
            active_cs = [c for c in cs if c.get('status') == 'active']
            s['active_courses_count'] = len(active_cs)
            course_names = [c['courses']['name'] for c in active_cs if c.get('courses')]
            s['course_names'] = ", ".join(course_names)
        return students
    return []

def get_student_by_id(student_id):
    url = f"{SUPABASE_URL}/rest/v1/students?id=eq.{student_id}&select=*"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code == 200 and resp.json():
        return resp.json()[0]
    return None

def create_student(first_name, last_name, email, phone, birth_date):
    url = f"{SUPABASE_URL}/rest/v1/students"
    data = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "phone": phone or None,
        "birth_date": birth_date or None
    }
    resp = requests.post(url, headers=HEADERS, json=data)
    if resp.status_code in [200, 201]:
        return resp.json()[0], None
    return None, resp.text

def update_student(student_id, first_name, last_name, email, phone, birth_date):
    url = f"{SUPABASE_URL}/rest/v1/students?id=eq.{student_id}"
    data = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "phone": phone or None,
        "birth_date": birth_date or None
    }
    resp = requests.patch(url, headers=HEADERS, json=data)
    if resp.status_code in [200, 204]:
        return True, None
    return False, resp.text

def delete_student(student_id):
    url = f"{SUPABASE_URL}/rest/v1/students?id=eq.{student_id}"
    resp = requests.delete(url, headers=HEADERS)
    if resp.status_code in [200, 204]:
        return True, None
    return False, resp.text

# ====================================================================
# OPERACIONES DE CURSOS (COURSES)
# ====================================================================
def get_all_courses():
    """Obtiene todos los cursos con la cantidad de alumnos inscriptos."""
    url = f"{SUPABASE_URL}/rest/v1/courses?select=*,course_students(id,status)&order=name.asc"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code == 200:
        courses = resp.json()
        for c in courses:
            cs = c.get('course_students') or []
            active_cs = [x for x in cs if x.get('status') == 'active']
            c['students_count'] = len(active_cs)
            c['active'] = True
        return courses
    return []

def get_course_by_id(course_id):
    url = f"{SUPABASE_URL}/rest/v1/courses?id=eq.{course_id}&select=*"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code == 200 and resp.json():
        c = resp.json()[0]
        c['active'] = True
        return c
    return None

def create_course(name, description, cost, billing_period, payment_due_day):
    url = f"{SUPABASE_URL}/rest/v1/courses"
    data = {
        "name": name,
        "description": description or None,
        "cost": float(cost),
        "billing_period": billing_period or "Mensual",
        "payment_due_day": int(payment_due_day) if payment_due_day else 10
    }
    resp = requests.post(url, headers=HEADERS, json=data)
    if resp.status_code in [200, 201]:
        return resp.json()[0], None
    return None, resp.text

def update_course(course_id, name, description, cost, billing_period, payment_due_day):
    url = f"{SUPABASE_URL}/rest/v1/courses?id=eq.{course_id}"
    data = {
        "name": name,
        "description": description or None,
        "cost": float(cost),
        "billing_period": billing_period or "Mensual",
        "payment_due_day": int(payment_due_day) if payment_due_day else 10
    }
    resp = requests.patch(url, headers=HEADERS, json=data)
    if resp.status_code in [200, 204]:
        return True, None
    return False, resp.text

def delete_course(course_id):
    url = f"{SUPABASE_URL}/rest/v1/courses?id=eq.{course_id}"
    resp = requests.delete(url, headers=HEADERS)
    if resp.status_code in [200, 204]:
        return True, None
    return False, resp.text

# ====================================================================
# OPERACIONES DE ASIGNACIONES (COURSE_STUDENTS)
# ====================================================================
def get_all_enrollments():
    """Obtiene todas las asignaciones de alumnos a cursos con detalles cruzados."""
    url = f"{SUPABASE_URL}/rest/v1/course_students?select=*,students(*),courses(*)&order=assigned_at.desc"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code == 200:
        return resp.json()
    return []

def get_enrollments_by_course(course_id):
    """Obtiene todos los alumnos inscriptos en un curso específico."""
    url = f"{SUPABASE_URL}/rest/v1/course_students?course_id=eq.{course_id}&select=*,students(*)&order=assigned_at.desc"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code == 200:
        return resp.json()
    return []

def enroll_student(course_id, student_id, status='active'):
    """Asigna un alumno a un curso."""
    url = f"{SUPABASE_URL}/rest/v1/course_students"
    data = {
        "course_id": course_id,
        "student_id": student_id,
        "status": status
    }
    resp = requests.post(url, headers=HEADERS, json=data)
    if resp.status_code in [200, 201]:
        return resp.json()[0], None
    return None, resp.text

def update_enrollment_status(enrollment_id, new_status):
    url = f"{SUPABASE_URL}/rest/v1/course_students?id=eq.{enrollment_id}"
    data = {"status": new_status}
    resp = requests.patch(url, headers=HEADERS, json=data)
    if resp.status_code in [200, 204]:
        return True, None
    return False, resp.text

def delete_enrollment(enrollment_id):
    url = f"{SUPABASE_URL}/rest/v1/course_students?id=eq.{enrollment_id}"
    resp = requests.delete(url, headers=HEADERS)
    if resp.status_code in [200, 204]:
        return True, None
    return False, resp.text
