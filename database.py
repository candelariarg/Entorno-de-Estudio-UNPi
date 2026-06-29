import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_path="entorno_estudio.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.crear_tablas()

    def crear_tablas(self):
        self.cursor.executescript("""
            CREATE TABLE IF NOT EXISTS apuntes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                metodo TEXT NOT NULL,
                contenido_xml TEXT,
                fecha_creacion TEXT DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS materias (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre      TEXT NOT NULL,
                profesor    TEXT DEFAULT 'No asignado',
                link_clases TEXT DEFAULT '-',
                horario     TEXT DEFAULT '-',
                estado      TEXT DEFAULT 'Cursando'
            );

            CREATE TABLE IF NOT EXISTS materiales_clase (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                materia_id INTEGER REFERENCES materias(id) ON DELETE CASCADE,
                nombre     TEXT NOT NULL,
                ruta       TEXT NOT NULL,
                tipo       TEXT,
                fecha_sub  TEXT DEFAULT (date('now','localtime'))
            );

            CREATE TABLE IF NOT EXISTS planificacion (
                id     INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                columna INTEGER,
                fila    INTEGER,
                color  TEXT
            );
        """)
        self.conn.commit()

        try:
            self.cursor.execute("ALTER TABLE apuntes ADD COLUMN materia_id INTEGER REFERENCES materias(id)")
            self.conn.commit()
        except sqlite3.OperationalError:
            #Si la columna ya existe, ignoramos el error
            pass

    #CRUD Apuntes: Create, Read, Update, Delete (crear, leer, actualizar, eliminar)
    def guardar_apunte(self, nombre, metodo, xml, materia_id=None):
        self.cursor.execute(
            "INSERT INTO apuntes (nombre, metodo, contenido_xml, materia_id) VALUES (?, ?, ?, ?)", 
            (nombre, metodo, xml, materia_id)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def obtener_apuntes(self):
        self.cursor.execute("SELECT * FROM apuntes ORDER BY fecha_creacion DESC")
        return self.cursor.fetchall()

    def actualizar_apunte(self, apunte_id, nombre, contenido_xml):
        self.cursor.execute(
            "UPDATE apuntes SET nombre=?, contenido_xml=? WHERE id=?",
            (nombre, contenido_xml, apunte_id)
        )
        self.conn.commit()

    def eliminar_apunte(self, apunte_id):
        self.cursor.execute("DELETE FROM apuntes WHERE id=?", (apunte_id,))
        self.conn.commit()

    def renombrar_apunte(self, apunte_id, nuevo_nombre):
        self.cursor.execute("UPDATE apuntes SET nombre=? WHERE id=?", (nuevo_nombre, apunte_id))
        self.conn.commit()

    #CRUD Materias y Materiales de Clase
    def agregar_materia(self, nombre, profesor, link, horario, estado="Cursando"):
        self.cursor.execute(
            "INSERT INTO materias (nombre, profesor, link_clases, horario, estado) VALUES (?, ?, ?, ?, ?)",
            (nombre, profesor, link, horario, estado)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def obtener_materias(self):
        self.cursor.execute("SELECT * FROM materias ORDER BY nombre")
        return self.cursor.fetchall()
        
    def agregar_material(self, materia_id, ruta_archivo):
        nombre = os.path.basename(ruta_archivo)
        ext = os.path.splitext(nombre)[1].replace('.', '').upper()
        self.cursor.execute("INSERT INTO materiales_clase (materia_id, nombre, ruta, tipo) VALUES (?, ?, ?, ?)",
                            (materia_id, nombre, ruta_archivo, ext if ext else "DOC"))
        self.conn.commit()

    def obtener_materiales(self, materia_id):
        self.cursor.execute("SELECT * FROM materiales_clase WHERE materia_id=? ORDER BY id DESC", (materia_id,))
        return self.cursor.fetchall()

    def actualizar_materia(self, materia_id, nombre, profesor, link, horario):
        self.cursor.execute(
            "UPDATE materias SET nombre=?, profesor=?, link_clases=?, horario=? WHERE id=?",
            (nombre, profesor, link, horario, materia_id)
        )
        self.conn.commit()

    def eliminar_materia(self, materia_id):
        self.cursor.execute("DELETE FROM materias WHERE id=?", (materia_id,))
        self.conn.commit()

    def eliminar_material(self, material_id):
        self.cursor.execute("DELETE FROM materiales_clase WHERE id=?", (material_id,))
        self.conn.commit()

    #CRUD Planner
    def guardar_bloque_planner(self, titulo, columna, fila, color):
        self.cursor.execute("INSERT INTO planificacion (titulo, columna, fila, color) VALUES (?, ?, ?, ?)", 
                            (titulo, columna, fila, color))
        self.conn.commit()
        return self.cursor.lastrowid

    def actualizar_bloque_planner(self, id, columna, fila):
        self.cursor.execute("UPDATE planificacion SET columna=?, fila=? WHERE id=?", (columna, fila, id))
        self.conn.commit()

    def borrar_bloque_planner(self, bloque_id):
        self.cursor.execute("DELETE FROM planificacion WHERE id=?", (bloque_id,))
        self.conn.commit()

    def obtener_bloques_planner(self):
        self.cursor.execute("SELECT * FROM planificacion")
        return self.cursor.fetchall()