# Práctica de SQL Injection — Seguridad Informática

PEn este proyecto armamos una aplicación web con Flask y SQLite que es vulnerable a propósito, para ver cómo funciona un ataque de SQL Injection desde adentro: primero lo explotamos y después lo corregimos. También incluimos dos módulos extra, uno para escanear la red y otro para revisar la seguridad de la base de datos.

El código contiene vulnerabilidades **intencionales** con fines de aprendizaje y práctica. 

## Integrantes

- Iza Verdesoto Maribel Del Rocio
- Lojan Malla Ana Elizabeth
- Macias Moya Jessica Jessenia
- Quishpe Herrera Jefefrson Camilo
- Suarez Cevallos Juana Paola
- Toaquiza Sillo Joselyn Aracely
- Zambrano Rodriguez Jose Antonio

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

## Usuarios de prueba

Para probar el login normal, la base de datos ya viene con estos usuarios cargados:

| Usuario | Contraseña | Rol           |
|---------|------------|---------------|
| admin   | admin123   | administrador |
| joss    | clave2026  | usuario       |
| jeff    | seguridad1 | usuario       |

## Cómo probar la vulnerabilidad

En el campo de usuario, ingresar:

admin’ --

Y en contraseña, cualquier texto. El sistema concede el acceso sin validar la contraseña real, porque el `--` convierte el resto de la consulta SQL en un comentario.

## Advertencia de uso responsable

Este proyecto se ejecuta únicamente sobre el propio equipo o en un entorno de laboratorio autorizado, con fines estrictamente académicos.