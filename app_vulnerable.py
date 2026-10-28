"""
app_vulnerable.py

Aplicación web de demostración académica (Práctica 4 - Seguridad Informática).
Contiene una vulnerabilidad INTENCIONAL de SQL Injection en el formulario
de inicio de sesión, con el fin de estudiar cómo se explota y cómo se
corrige. NO usar este código en un proyecto real.

Cómo es vulnerable:
En la función login(), el usuario y la contraseña que llegan desde el
formulario se insertan directamente dentro del texto de la consulta SQL
usando f-strings (concatenación). Si alguien escribe caracteres especiales
de SQL (como comillas simples y la palabra OR), puede alterar el
significado de la consulta y entrar sin conocer una contraseña real.
"""

from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), "usuarios.db")


def get_connection():
    """Abre una conexión a la base de datos SQLite."""
    return sqlite3.connect(DB_PATH)


def init_db():
    """Crea la base de datos y algunos usuarios de ejemplo, solo si no existe."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            rol TEXT NOT NULL
        )
        """
    )
    # Solo insertamos datos de ejemplo si la tabla está vacía
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO usuarios (username, password, rol) VALUES (?, ?, ?)",
            [
                ("admin", "admin123", "administrador"),
                ("joss", "clave2026", "usuario"),
                ("jeff", "seguridad1", "usuario"),
            ],
        )
        conn.commit()
    conn.close()


@app.route("/", methods=["GET"])
def home():
    """Página principal: solo muestra el formulario de login."""
    return render_template("login.html", mensaje=None)


@app.route("/login", methods=["POST"])
def login():
    """
    Procesa el formulario de login.

    *** ESTA CONSULTA ES VULNERABLE A PROPÓSITO ***
    El usuario y la contraseña se insertan directamente en el texto SQL.
    """
    username = request.form.get("username", "")
    password = request.form.get("password", "")

    conn = get_connection()
    cursor = conn.cursor()

    # --- LÍNEA VULNERABLE ---
    # Concatenamos el texto del usuario directo en la consulta.
    query = f"SELECT * FROM usuarios WHERE username = '{username}' AND password = '{password}'"
    print("Consulta ejecutada:", query)  # Ayuda a ver en consola qué SQL se arma

    try:
        cursor.execute(query)
        resultado = cursor.fetchone()
    except sqlite3.OperationalError as error:
        conn.close()
        return render_template(
            "login.html", mensaje=f"Error en la consulta SQL: {error}"
        )

    conn.close()

    if resultado:
        return render_template(
            "login.html",
            mensaje=f"✅ Acceso concedido. Bienvenido, {resultado[1]} (rol: {resultado[3]}).",
        )
    else:
        return render_template("login.html", mensaje="❌ Usuario o contraseña incorrectos.")


if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="127.0.0.1", port=5000)
