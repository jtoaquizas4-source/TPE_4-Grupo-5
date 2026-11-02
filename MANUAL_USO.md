# MANUAL DE USO Y PRUEBAS

## Práctica Experimental 4 – Seguridad Informática
**Grupo 5**

### 1. Objetivo

Describir los procedimientos para instalar, ejecutar y comprobar el funcionamiento de una aplicación web desarrollada con Python, Flask y SQLite, demostrando una vulnerabilidad de SQL Injection y su mitigación mediante consultas parametrizadas.

Adicionalmente, se incluye un escáner de puertos TCP para verificar la disponibilidad del servidor de pruebas.

Todas las actividades deben realizarse exclusivamente en un entorno local y autorizado.

### 2. Requisitos previos

Para ejecutar el proyecto se requiere:

- Python 3.11 o una versión compatible con el código.
- Visual Studio Code, PyCharm u otro editor de código.
- Git.
- Flask.
- Requests.
- SQLite, incluido en la biblioteca estándar de Python.
- Navegador web.

**Repositorio del proyecto:**

https://github.com/jtoaquizas4-source/TPE_4-Grupo-5

### 3. Estructura del proyecto

El proyecto contiene los siguientes archivos:

| Archivo | Descripción |
|---|---|
| `app_vulnerable.py` | Aplicación con vulnerabilidad SQL Injection intencional |
| `app_segura.py` | Aplicación protegida mediante consultas parametrizadas |
| `ataque_sql_i.py` | Ejecución automatizada de tres pruebas SQL Injection |
| `escaneo_red.py` | Escáner de puertos TCP |
| `templates/login.html` | Formulario web de autenticación |
| `usuarios.db` | Base de datos SQLite |
| `requirements.txt` | Dependencias del proyecto |
| `README.md` | Información general del proyecto |
| `MANUAL_USO.md` | Instrucciones de instalación, ejecución y pruebas |

### 4. Instalación y configuración

**Paso 1. Clonar el repositorio**

Abrir una terminal y ejecutar:

```bash
git clone https://github.com/jtoaquizas4-source/TPE_4-Grupo-5.git
cd TPE_4-Grupo-5
```

Abrir la carpeta del proyecto en Visual Studio Code o PyCharm.

**Paso 2. Crear un entorno virtual (recomendado)**

```bash
python -m venv .venv
```

En PowerShell, activar el entorno mediante:

```powershell
.\.venv\Scripts\Activate.ps1
```

**Paso 3. Instalar las dependencias**

```bash
python -m pip install -r requirements.txt
```

El archivo `requirements.txt` debe incluir las bibliotecas Flask y Requests.

### 5. Ejecución de la aplicación vulnerable

Abrir una terminal dentro de la carpeta del proyecto y ejecutar:

```bash
python app_vulnerable.py
```

El servidor debe iniciarse en:

http://127.0.0.1:5000

Abrir esa dirección en el navegador para visualizar el formulario de inicio de sesión.

**Importante:** mantener abierta la terminal del servidor mientras se realizan las pruebas.

### 6. Verificación de la autenticación

**Prueba 1. Credenciales válidas**

Ingresar:

- Usuario: `admin`
- Contraseña: `admin123`

**Resultado esperado:** acceso concedido y mensaje de bienvenida al administrador, siempre que la base de datos contenga esas credenciales.

**Prueba 2. Credenciales inválidas**

Ingresar:

- Usuario: `admin`
- Contraseña: `incorrecta123`

**Resultado esperado:** mensaje «Usuario o contraseña incorrectos».

### 7. Demostración de SQL Injection

La aplicación `app_vulnerable.py` construye la consulta SQL incorporando directamente los valores del formulario:

```python
query = (
    f"SELECT * FROM usuarios "
    f"WHERE username = '{username}' "
    f"AND password = '{password}'"
)

cursor.execute(query)
```

Esta implementación permite que una entrada especialmente construida modifique la condición de autenticación.

**Paso 1. Mantener iniciada la aplicación vulnerable.**

**Paso 2. Abrir una segunda terminal y ejecutar:**

```bash
python ataque_sql_i.py --modo vulnerable
```

El programa realiza tres pruebas con las siguientes entradas:

1. `admin' --`
2. `' OR '1'='1`
3. `x' OR '1'='1' --`

**Paso 3. Revisar los resultados.**

El programa muestra el código HTTP, si el acceso fue concedido o rechazado y un resumen de las tres pruebas.

**Resultado esperado:** al menos una entrada debe permitir eludir la comprobación de contraseña en la aplicación vulnerable, si la consulta y los datos corresponden a la configuración descrita.

El resultado real debe comprobarse en la terminal y documentarse mediante capturas de pantalla.

### 8. Mitigación de SQL Injection

La aplicación `app_segura.py` implementa consultas parametrizadas:

```python
query = (
    "SELECT * FROM usuarios "
    "WHERE username = ? AND password = ?"
)

cursor.execute(query, (username, password))
```

Los parámetros permiten que SQLite trate los valores ingresados como datos y no como instrucciones SQL.

**No se debe modificar `app_vulnerable.py` para aplicar la mitigación**, porque ambas versiones se mantienen separadas con fines comparativos.

### 9. Validación de la mitigación

**Paso 1. Detener la aplicación vulnerable.**

En la terminal donde está ejecutándose Flask, presionar `Ctrl + C`.

**Paso 2. Iniciar la aplicación segura.**

```bash
python app_segura.py
```

**Paso 3. Ejecutar las mismas pruebas en otra terminal.**

```bash
python ataque_sql_i.py --modo segura
```

**Resultado esperado:** los tres intentos de SQL Injection deben ser rechazados.

**Paso 4. Comprobar la autenticación legítima.**

En el navegador, ingresar:

- Usuario: `admin`
- Contraseña: `admin123`

**Resultado esperado:** acceso concedido al administrador, si las credenciales coinciden con las registradas en la base de datos.

Las aplicaciones vulnerable y segura utilizan el puerto `5000`; por lo tanto, deben ejecutarse por separado.

### 10. Escaneo de puertos TCP

El archivo `escaneo_red.py` permite verificar qué puertos TCP están abiertos en un equipo autorizado.

**Paso 1. Mantener iniciado uno de los servidores Flask.**

**Paso 2. Ejecutar el escáner.**

```bash
python escaneo_red.py
```

El programa solicita una dirección IPv4 y un rango de puertos.

Para utilizar los valores predeterminados, presionar Enter en cada campo:

- Dirección IPv4: `127.0.0.1`
- Puerto inicial: `4995`
- Puerto final: `5005`

También puede ejecutarse directamente:

```bash
python escaneo_red.py 127.0.0.1 4995 5005
```

**Resultado esperado:** el puerto TCP `5000` debe aparecer abierto cuando el servidor Flask está funcionando.

El escáner permite comprobar la disponibilidad del puerto, pero no determina si la aplicación activa es la vulnerable o la segura.

### 11. Evidencias de ejecución

Para documentar la práctica se deben obtener capturas de:

1. Inicio del servidor Flask y visualización del formulario.
2. Autenticación con credenciales válidas e inválidas.
3. Ejecución de las tres pruebas SQL Injection contra la aplicación vulnerable.
4. Consulta SQL vulnerable y resultado obtenido.
5. Ejecución de las mismas pruebas contra la aplicación segura.
6. Consulta SQL parametrizada y resultado obtenido.
7. Escaneo TCP que muestre el estado del puerto `5000`.

Las capturas deben incorporarse al informe técnico grupal, explicando los resultados efectivamente observados.

### 12. Consideraciones finales

La práctica permite comparar una consulta SQL vulnerable con una consulta parametrizada, identificar los efectos de la manipulación de entradas y comprobar la mitigación mediante pruebas controladas.

El proyecto es exclusivamente académico. No debe desplegarse la aplicación vulnerable en servidores públicos ni utilizarse para evaluar sistemas sin autorización.