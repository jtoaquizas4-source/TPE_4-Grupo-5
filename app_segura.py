
"""
Práctica Experimental 4 - Seguridad Informática
Aplicación segura contra SQL Injection.

Objetivo:
Demostrar cómo las consultas parametrizadas permiten
evitar la inyección SQL en un formulario de inicio de sesión.

Esta aplicación se compara con app_vulnerable.py.

Uso académico en un entorno local autorizado.
"""

import os
import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

DB_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "usuarios.db"
)


def get_connection():
    """Establece conexión con la base de datos SQLite."""
    return sqlite3.connect(DB_PATH)


def init_db():
    """Crea la tabla e inserta usuarios de prueba si está vacía."""

    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                rol TEXT NOT NULL
            )
        """)

        cursor.execute("SELECT COUNT(*) FROM usuarios")

        if cursor.fetchone()[0] == 0:
            cursor.executemany(
                """
                INSERT INTO usuarios (username, password, rol)
                VALUES (?, ?, ?)
                """,
                [
                    ("admin", "admin123", "administrador"),
                    ("joss", "clave2026", "usuario"),
                    ("jeff", "seguridad1", "usuario")
                ]
            )

        conn.commit()


@app.route("/", methods=["GET"])
def home():
    """Muestra el formulario de inicio de sesión."""

    return render_template(
        "login.html",
        mensaje=None
    )


@app.route("/login", methods=["POST"])
def login():
    """Valida las credenciales mediante una consulta segura."""

    username = request.form.get("username", "")
    password = request.form.get("password", "")

    # MITIGACIÓN DE SQL INJECTION:
    # Los valores ingresados se envían por separado.
    # No se concatenan con la consulta SQL.

    query = (
        "SELECT * FROM usuarios "
        "WHERE username = ? AND password = ?"
    )

    print("\n--- PRUEBA DE AUTENTICACIÓN ---")
    print("Aplicación: SEGURA")
    print("Consulta parametrizada:", query)

    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute(
            query,
            (username, password)
        )

        resultado = cursor.fetchone()

    except sqlite3.Error as error:
        print("Resultado: ERROR SQL")
        print("Detalle:", error)

        return render_template(
            "login.html",
            mensaje="Error al procesar la consulta."
        )

    finally:
        conn.close()

    if resultado:
        print("Resultado: ACCESO CONCEDIDO")

        return render_template(
            "login.html",
            mensaje=(
                f"Acceso concedido. Bienvenido, "
                f"{resultado[1]} (rol: {resultado[3]})."
            )
        )

    print("Resultado: ACCESO RECHAZADO")

    return render_template(
        "login.html",
        mensaje="Usuario o contraseña incorrectos."
    )


if __name__ == "__main__":
    init_db()

    print("Iniciando aplicación segura...")
    print("Dirección: http://127.0.0.1:5000")
    print("Entorno de pruebas local y autorizado.")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )
