
# MANUAL DE USO Y PRUEBAS

## Aplicación web vulnerable a SQL Injection — Práctica 4

### 1. Objetivo del manual

Describir los procedimientos necesarios para configurar, ejecutar y verificar el funcionamiento de la aplicación web desarrollada con Python, Flask y SQLite, incluyendo la simulación controlada de SQL Injection y la validación de su mitigación mediante consultas parametrizadas.

Las pruebas deben realizarse exclusivamente en un entorno académico local y controlado.

### 2. Requisitos previos

Para ejecutar la aplicación se utilizaron las siguientes herramientas:

- Python 3.11.9.
- PyCharm como entorno de desarrollo.
- Git para clonar el repositorio.
- Flask 3.1.3 y sus dependencias.
- SQLite como sistema de base de datos.
- Navegador web.

**Repositorio del proyecto:**

https://github.com/jtoaquizas4-source/TPE_4-Grupo-5

### 3. Instalación y configuración

**Paso 1. Clonar el repositorio**

Desde PyCharm, seleccionar la opción **Clone Repository** e introducir la URL del repositorio.

Alternativamente, ejecutar el siguiente comando:


git clone https://github.com/jtoaquizas4-source/TPE_4-Grupo-5.git


Abrir el proyecto `TPE_4-Grupo-5` en PyCharm.

**Paso 2. Configurar el intérprete de Python**

Configurar Python 3.11.9 y crear un entorno virtual `.venv` para administrar las dependencias del proyecto de manera independiente.

**Paso 3. Instalar las dependencias**

En la terminal de PyCharm, con el entorno virtual activado, ejecutar:


python -m pip install -r requirements.txt


Verificar que la instalación finalice sin errores. Durante la práctica se instaló correctamente Flask 3.1.3 junto con sus dependencias.

### 4. Ejecución de la aplicación web

**Paso 1. Iniciar el servidor**

En la terminal de PyCharm, ejecutar:


python app_vulnerable.py


**Paso 2. Comprobar el servidor**

Verificar que la terminal muestre la dirección local:


Running on http://127.0.0.1:5000


**Paso 3. Acceder a la aplicación**

Abrir el navegador e ingresar la siguiente dirección:

http://127.0.0.1:5000

Se visualizará el formulario de autenticación con los campos Usuario y Contraseña.

### 5. Verificación del inicio de sesión

**Prueba 1. Credenciales válidas**

Ingresar los siguientes datos de prueba:

- Usuario: `admin`
- Contraseña: `admin123`

**Resultado obtenido:** el sistema permitió el acceso y mostró el mensaje de bienvenida al administrador.

**Prueba 2. Credenciales inválidas**

Ingresar los siguientes datos:

- Usuario: `admin`
- Contraseña: `incorrecta123`

**Resultado esperado:** el sistema debe rechazar el inicio de sesión y mostrar el mensaje «Usuario o contraseña incorrectos».

### 6. Demostración de SQL Injection

**Paso 1. Utilizar la versión vulnerable**

Ejecutar la versión original de `app_vulnerable.py`, antes de aplicar la corrección.

La consulta de autenticación se construía incorporando directamente los valores ingresados en el formulario:


query = f"SELECT * FROM usuarios WHERE username = '{username}' AND password = '{password}'"
cursor.execute(query)


**Paso 2. Introducir la entrada de prueba**

En el formulario web, ingresar los siguientes valores:

- Usuario: `' OR 1=1 -- `
- Contraseña: `Jota25`

Seleccionar **Iniciar sesión**.

**Paso 3. Verificar el resultado**

**Resultado obtenido:** la aplicación concedió acceso como administrador sin utilizar la contraseña legítima.

La terminal de PyCharm mostró la consulta SQL manipulada:


SELECT * FROM usuarios
WHERE username = '' OR 1=1 -- ' AND password = 'Jota25'


La condición `OR 1=1` introdujo una expresión siempre verdadera, mientras que `--` convirtió el resto de la instrucción en un comentario SQL, evitando la comprobación de la contraseña.

Esta prueba confirmó la existencia de una vulnerabilidad de SQL Injection en el proceso de autenticación.

### 7. Implementación de la mitigación

**Paso 1. Modificar la consulta vulnerable**

En la función `login()` del archivo `app_vulnerable.py`, reemplazar la consulta insegura por una consulta parametrizada:


query = "SELECT * FROM usuarios WHERE username = ? AND password = ?"
cursor.execute(query, (username, password))


Los parámetros permiten que SQLite procese los valores ingresados como datos y no como instrucciones SQL, evitando la manipulación de la estructura de la consulta.

**Paso 2. Guardar los cambios**

Guardar el archivo y reiniciar el servidor Flask para aplicar la modificación.

La corrección se desarrolló en la rama `jose-mitigacion-sqli`, manteniendo separada la versión original del proyecto.

### 8. Validación de la mitigación

**Prueba 1. Repetir el intento de SQL Injection**

Ingresar nuevamente:

- Usuario: `' OR 1=1 -- `
- Contraseña: `Jota25`

**Resultado obtenido:** la aplicación rechazó el acceso y mostró el mensaje «Usuario o contraseña incorrectos».

**Prueba 2. Verificar la autenticación legítima**

Ingresar:

- Usuario: `admin`
- Contraseña: `admin123`

**Resultado obtenido:** la aplicación concedió acceso correctamente al administrador.

La consola de PyCharm confirmó que la aplicación utilizaba una consulta parametrizada:


SELECT * FROM usuarios
WHERE username = ? AND password = ?


Las pruebas demostraron que la contramedida impidió el bypass de autenticación previamente identificado, manteniendo el funcionamiento normal del inicio de sesión legítimo.

### 9. Evidencias de ejecución

Las principales evidencias obtenidas durante la práctica corresponden a:

1. Ejecución del servidor Flask y acceso a la aplicación web.
2. Consulta SQL vulnerable y acceso indebido mediante SQL Injection.
3. Rechazo del intento de inyección SQL después de aplicar la mitigación.
4. Consulta parametrizada y funcionamiento de la autenticación legítima.

Las capturas seleccionadas se incorporarán al informe técnico grupal, acompañadas de la explicación de los procedimientos y los resultados comprobados.
