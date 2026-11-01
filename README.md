# Práctica Experimental 4 – Seguridad Informática

## Demostración de SQL Injection y escaneo de puertos TCP

### 1. Descripción del proyecto

Este proyecto desarrolla una aplicación web de inicio de sesión utilizando Python, Flask y SQLite, con el propósito de demostrar una vulnerabilidad de SQL Injection y su mitigación mediante consultas parametrizadas.

Se implementan dos versiones independientes de la aplicación:

- **Aplicación vulnerable:** construye una consulta SQL incorporando directamente los datos ingresados por el usuario.
- **Aplicación segura:** utiliza consultas parametrizadas para evitar que las entradas modifiquen la estructura de la consulta SQL.

Adicionalmente, el proyecto incluye un programa para ejecutar tres pruebas automatizadas de SQL Injection y un escáner de puertos TCP.

Todas las pruebas se realizan exclusivamente en un entorno local y autorizado.

### 2. Integrantes – Grupo 5

- Iza Verdesoto Maribel Del Rocío
- Lojan Malla Ana Elizabeth
- Macías Moya Jessica Jessenia
- Quishpe Herrera Jefferson Camilo
- Suárez Cevallos Juana Paola
- Toaquiza Sillo Joselyn Aracely
- Zambrano Rodríguez José Antonio

### 3. Estructura del repositorio

```text
TPE_4-Grupo-5/
│
├── app_vulnerable.py
├── app_segura.py
├── ataque_sql_i.py
├── escaneo_red.py
├── usuarios.db
├── requirements.txt
├── README.md
├── MANUAL_USO.md
│
└── templates/
    └── login.html
```

**Descripción de los archivos:**

| Archivo | Función |
|---|---|
| `app_vulnerable.py` | Servidor Flask con autenticación intencionalmente vulnerable a SQL Injection |
| `app_segura.py` | Servidor Flask con autenticación mediante consultas parametrizadas |
| `ataque_sql_i.py` | Ejecuta tres pruebas automatizadas y presenta los resultados |
| `escaneo_red.py` | Analiza puertos TCP de una dirección IPv4 autorizada |
| `usuarios.db` | Base de datos SQLite con usuarios de prueba |
| `templates/login.html` | Formulario de autenticación compartido por ambas aplicaciones |
| `requirements.txt` | Dependencias necesarias para ejecutar el proyecto |
| `MANUAL_USO.md` | Instrucciones detalladas de instalación, ejecución y pruebas |

### 4. Requisitos

- Python 3.11 o superior compatible con las dependencias.
- pip.
- Flask.
- Requests.
- Navegador web.
- Visual Studio Code, PyCharm u otro editor de código (opcional).

SQLite y la biblioteca `socket` forman parte de Python, por lo que no requieren instalación independiente.

### 5. Instalación

Clonar el repositorio:

```bash
git clone https://github.com/jtoaquizas4-source/TPE_4-Grupo-5.git
cd TPE_4-Grupo-5
```

Instalar las dependencias:

```bash
python -m pip install -r requirements.txt
```

### 6. Ejecución de la aplicación vulnerable

En una terminal, ejecutar:

```bash
python app_vulnerable.py
```

Abrir en el navegador:

http://127.0.0.1:5000

La aplicación utiliza una consulta SQL vulnerable de manera intencional para demostrar cómo una entrada puede alterar el proceso de autenticación.

### 7. Usuarios de prueba

La aplicación crea los siguientes usuarios si la tabla `usuarios` está vacía:

| Usuario | Contraseña | Rol |
|---|---|---|
| `admin` | `admin123` | administrador |
| `joss` | `clave2026` | usuario |
| `jeff` | `seguridad1` | usuario |

Si la base de datos ya contiene registros, estos usuarios no se insertan nuevamente.

### 8. Pruebas automatizadas de SQL Injection

Con la aplicación vulnerable en ejecución, abrir una segunda terminal y ejecutar:

```bash
python ataque_sql_i.py --modo vulnerable
```

El programa prueba tres entradas:

1. `admin' --`
2. `' OR '1'='1`
3. `x' OR '1'='1' --`

Los resultados indican si la aplicación concede o rechaza el acceso, además de presentar un resumen.

**Resultado esperado:** al menos una entrada debe permitir eludir la comprobación de contraseña en la aplicación vulnerable, siempre que los datos y la consulta correspondan a la configuración indicada.

### 9. Ejecución de la aplicación segura

Detener primero la aplicación vulnerable mediante `Ctrl + C`.

Iniciar la aplicación segura:

```bash
python app_segura.py
```

En otra terminal, ejecutar:

```bash
python ataque_sql_i.py --modo segura
```

**Resultado esperado:** las tres entradas de SQL Injection deben ser rechazadas, mientras que las credenciales legítimas deben continuar funcionando.

Ambas aplicaciones utilizan el puerto `5000`, por lo que no deben ejecutarse simultáneamente con esa configuración.

**Nota:** el argumento `--modo` identifica la prueba en el informe de consola, pero no inicia ni selecciona automáticamente el servidor.

### 10. Escaneo de puertos TCP

Con uno de los servidores Flask en ejecución, ejecutar:

```bash
python escaneo_red.py 127.0.0.1 4995 5005
```

El programa examina el rango indicado y presenta los puertos TCP abiertos.

**Resultado esperado:** el puerto `5000` debe aparecer abierto cuando Flask está funcionando.

También se puede ejecutar de manera interactiva:

```bash
python escaneo_red.py
```

### 11. Evidencias de la práctica

Se deben documentar los siguientes procedimientos:

- Inicio del servidor Flask y funcionamiento del formulario.
- Autenticación con credenciales válidas e inválidas.
- Ejecución de las pruebas SQL Injection en la aplicación vulnerable.
- Ejecución de las mismas pruebas en la aplicación segura.
- Comparación de los resultados.
- Escaneo TCP y detección del puerto `5000`.

Los resultados obtenidos deben respaldarse con capturas de pantalla e incorporarse al informe técnico grupal.

### 12. Advertencia de uso responsable

Este proyecto contiene una vulnerabilidad intencional con fines exclusivamente académicos.

La aplicación vulnerable no debe utilizarse en producción ni exponerse a Internet. Las pruebas de SQL Injection y el escaneo de puertos deben realizarse únicamente sobre equipos y servicios propios o expresamente autorizados.

Para conocer los procedimientos detallados, consultar `MANUAL_USO.md`.