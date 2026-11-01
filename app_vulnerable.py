
"""
Práctica Experimental 4 - Seguridad Informática
Aplicación web vulnerable a SQL Injection.

Objetivo:
Demostrar cómo una consulta SQL construida con datos
del usuario puede permitir eludir la autenticación.

Uso exclusivo en un entorno local y autorizado.
No utilizar este código en producción.
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
    """Abre una conexión con la base de datos SQLite."""
    return sqlite3.connect(DB_PATH)


def init_db():
    """Prepara la base de datos y los usuarios de prueba."""

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
    """Presenta el formulario de inicio de sesión."""

    return render_template(
        "login.html",
        mensaje=None
    )


@app.route("/login", methods=["POST"])
def login():
    """Procesa el inicio de sesión vulnerable."""

    username = request.form.get("username", "")
    password = request.form.get("password", "")

    # VULNERABILIDAD INTENCIONAL:
    # Se insertan los valores recibidos directamente
    # en el texto SQL, sin consultas parametrizadas.
    #
    # Esto permite alterar la condición WHERE mediante
    # entradas especialmente construidas.

    query = (
        f"SELECT * FROM usuarios "
        f"WHERE username = '{username}' "
        f"AND password = '{password}'"
    )

    print("\n--- PRUEBA SQL INJECTION ---")
    print("Aplicación: VULNERABLE")
    print("Usuario recibido:", username)
    print("Consulta SQL generada:", query)

    conn = get_connection()

    try:
        cursor = conn.cursor()
        cursor.execute(query)
        resultado = cursor.fetchone()

    except sqlite3.Error as error:
        print("Resultado: ERROR SQL")
        print("Detalle:", error)

        return render_template(
            "login.html",
            mensaje=f"Error en la consulta SQL: {error}"
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

    print("Iniciando aplicación vulnerable...")
    print("Dirección: http://127.0.0.1:5000")
    print("Entorno de pruebas local y autorizado.")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )
