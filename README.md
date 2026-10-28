# Práctica 4 — Seguridad Informática

Proyecto académico sobre **SQL Injection**: una aplicación web vulnerable en Flask/SQLite, su explotación, su mitigación, y módulos de escaneo de red y seguridad en bases de datos.

⚠️ Este código contiene vulnerabilidades **intencionales** con fines educativos. No usar en producción.

## Integrantes

- (nombre 1)
- (nombre 2)
- (nombre 3)
- (nombre 4)
- (nombre 5)
- (nombre 6)
- (nombre 7)

## Estructura del repositorio

```
app_vulnerable.py      # Servidor Flask con login vulnerable a SQL Injection
templates/login.html   # Formulario de inicio de sesión
ataque_sql_i.py        # Script que explota la vulnerabilidad (pendiente)
escaneo_red.py         # Módulo de escaneo de red (pendiente)
MANUAL_USO.md          # Manual de uso paso a paso (pendiente)
requirements.txt       # Dependencias del proyecto
```

## Requisitos

- Python 3.11 o superior
- pip

## Instalación

```bash
git clone <URL-del-repositorio>
cd <carpeta-del-repositorio>
pip install -r requirements.txt
```

## Ejecución

```bash
python app_vulnerable.py
```

Luego abrir en el navegador: http://127.0.0.1:5000

## Advertencia de uso responsable

Este proyecto se ejecuta únicamente sobre el propio equipo o en un entorno de laboratorio autorizado, con fines estrictamente académicos.
