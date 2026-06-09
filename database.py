#SQLite con Python.
#Le pedí a la IA Claude que me de un codigo para una base de datos con SQLite en Python.
#Mi prompt fue: "Quiero saber como conecto mi aplicación para escritorio (desarrollada con python y su libreria wxPython) con SQLite. Ya que quiero "armar" una base de datos con un hisorial de apuntes, guardar fechas que se marcan en el calendario, guardar detalles de las materias que el alumno escribio, archivos subidos desde el escritorio, etc."

#Respuesta: Aquí te explico cómo conectar tu aplicación wxPython con SQLite, con un diseño pensado para lo que describís (apuntes, calendario, materias, archivos).
#La integración se hace con el módulo sqlite3 de Python, que ya viene incluido sin instalar nada extra. La idea central es tener una clase DatabaseManager que centralice todas las operaciones.

import sqlite3
import os
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path="apuntes.db"):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.conectar()
        self.crear_tablas()

    def conectar(self):
        # check_same_thread=False es necesario en wxPython
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  # devuelve filas como diccionarios
        self.cursor = self.conn.cursor()

    def crear_tablas(self):
        self.cursor.executescript("""
            CREATE TABLE IF NOT EXISTS materias (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre      TEXT NOT NULL,
                color       TEXT DEFAULT '#4A90D9',
                descripcion TEXT
            );

            CREATE TABLE IF NOT EXISTS apuntes (
                id             INTEGER PRIMARY KEY AUTOINCREMENT,
                materia_id     INTEGER REFERENCES materias(id) ON DELETE CASCADE,
                titulo         TEXT NOT NULL,
                contenido      TEXT,
                fecha_creacion TEXT DEFAULT (datetime('now','localtime')),
                fecha_mod      TEXT DEFAULT (datetime('now','localtime'))
            );

            CREATE TABLE IF NOT EXISTS calendario (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                materia_id INTEGER REFERENCES materias(id) ON DELETE CASCADE,
                fecha      TEXT NOT NULL,
                titulo     TEXT NOT NULL,
                tipo       TEXT CHECK(tipo IN ('examen','entrega','clase','otro'))
            );

            CREATE TABLE IF NOT EXISTS archivos (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                apunte_id  INTEGER REFERENCES apuntes(id) ON DELETE CASCADE,
                nombre     TEXT NOT NULL,
                ruta       TEXT NOT NULL,
                tamaño     INTEGER,
                fecha_sub  TEXT DEFAULT (datetime('now','localtime'))
            );
        """)
        self.conn.commit()

    # ── MATERIAS ──────────────────────────────────────────
    def agregar_materia(self, nombre, color="#4A90D9", descripcion=""):
        self.cursor.execute(
            "INSERT INTO materias (nombre, color, descripcion) VALUES (?, ?, ?)",
            (nombre, color, descripcion)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def obtener_materias(self):
        self.cursor.execute("SELECT * FROM materias ORDER BY nombre")
        return self.cursor.fetchall()

    # ── APUNTES ───────────────────────────────────────────
    def agregar_apunte(self, materia_id, titulo, contenido=""):
        self.cursor.execute(
            "INSERT INTO apuntes (materia_id, titulo, contenido) VALUES (?, ?, ?)",
            (materia_id, titulo, contenido)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def obtener_apuntes(self, materia_id=None):
        if materia_id:
            self.cursor.execute(
                "SELECT * FROM apuntes WHERE materia_id=? ORDER BY fecha_mod DESC",
                (materia_id,)
            )
        else:
            self.cursor.execute("SELECT * FROM apuntes ORDER BY fecha_mod DESC")
        return self.cursor.fetchall()

    def actualizar_apunte(self, apunte_id, titulo, contenido):
        self.cursor.execute(
            """UPDATE apuntes SET titulo=?, contenido=?,
               fecha_mod=datetime('now','localtime') WHERE id=?""",
            (titulo, contenido, apunte_id)
        )
        self.conn.commit()

    # ── CALENDARIO ────────────────────────────────────────
    def agregar_evento(self, materia_id, fecha, titulo, tipo="otro"):
        self.cursor.execute(
            "INSERT INTO calendario (materia_id, fecha, titulo, tipo) VALUES (?,?,?,?)",
            (materia_id, fecha, titulo, tipo)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def obtener_eventos_por_fecha(self, fecha):
        # fecha en formato 'YYYY-MM-DD'
        self.cursor.execute(
            "SELECT * FROM calendario WHERE fecha=? ORDER BY tipo",
            (fecha,)
        )
        return self.cursor.fetchall()

    # ── ARCHIVOS ──────────────────────────────────────────
    def adjuntar_archivo(self, apunte_id, ruta_archivo):
        nombre = os.path.basename(ruta_archivo)
        tamaño = os.path.getsize(ruta_archivo)
        self.cursor.execute(
            "INSERT INTO archivos (apunte_id, nombre, ruta, tamaño) VALUES (?,?,?,?)",
            (apunte_id, nombre, ruta_archivo, tamaño)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def obtener_archivos(self, apunte_id):
        self.cursor.execute(
            "SELECT * FROM archivos WHERE apunte_id=?",
            (apunte_id,)
        )
        return self.cursor.fetchall()

    def cerrar(self):
        if self.conn:
            self.conn.close()