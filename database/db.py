import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'escuelita.db')
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), 'schema_sqlite.sql')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    """Inicializa la base de datos con el esquema de SQLite si no existe o se requiere."""
    db = get_db()
    with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
        script = f.read()
    db.executescript(script)
    db.commit()
    db.close()
