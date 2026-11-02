
"""
escaneo_red.py

Práctica Experimental 4 - Seguridad Informática
Grupo 5

Escáner de puertos TCP para comprobar los servicios
disponibles en un equipo o entorno de laboratorio autorizado.

Configuración predeterminada:
    Dirección IP: 127.0.0.1
    Puerto inicial: 4995
    Puerto final: 5005

El rango incluye el puerto 5000 utilizado por Flask.

Ejecución interactiva:
    python escaneo_red.py

Ejecución con argumentos:
    python escaneo_red.py 127.0.0.1 4995 5005

Uso exclusivo en equipos propios o redes autorizadas.
"""

import ipaddress
import socket
import sys
import time

from dataclasses import dataclass, field


IP_POR_DEFECTO = "127.0.0.1"
PUERTO_INICIAL_POR_DEFECTO = 4995
PUERTO_FINAL_POR_DEFECTO = 5005


SERVICIOS = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    135: "RPC",
    139: "NetBIOS",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    3306: "MySQL",
    3389: "RDP",
    5000: "Flask (aplicación de pruebas)",
    5432: "PostgreSQL",
    8000: "HTTP (servidor de prueba)",
    8080: "HTTP alternativo"
}


class ErrorValidacion(ValueError):
    """Representa errores en los datos ingresados."""


@dataclass(frozen=True, slots=True)
class ConfiguracionEscaneo:
    """Contiene los parámetros del escaneo."""

    ip: str
    puerto_inicial: int
    puerto_final: int

    @property
    def total_puertos(self) -> int:
        return self.puerto_final - self.puerto_inicial + 1


@dataclass(slots=True)
class ResultadoEscaneo:
    """Almacena los resultados del escaneo."""

    configuracion: ConfiguracionEscaneo
    puertos_abiertos: list[int] = field(
        default_factory=list
    )
    tiempo_total: float = 0.0

    @property
    def total_analizados(self) -> int:
        return self.configuracion.total_puertos

    @property
    def total_abiertos(self) -> int:
        return len(self.puertos_abiertos)


class ValidadorEntrada:
    """Valida direcciones IPv4 y rangos de puertos."""

    PUERTO_MINIMO = 1
    PUERTO_MAXIMO = 65535

    @staticmethod
    def validar_ip(ip: str) -> str:
        ip = ip.strip()

        if not ip:
            raise ErrorValidacion(
                "La dirección IP no puede estar vacía."
            )

        try:
            return str(ipaddress.IPv4Address(ip))

        except ipaddress.AddressValueError as error:
            raise ErrorValidacion(
                "La dirección IPv4 ingresada no es válida."
            ) from error

    @classmethod
    def validar_puerto(cls, puerto: int) -> int:

        if not cls.PUERTO_MINIMO <= puerto <= cls.PUERTO_MAXIMO:
            raise ErrorValidacion(
                f"El puerto debe estar entre "
                f"{cls.PUERTO_MINIMO} y "
                f"{cls.PUERTO_MAXIMO}."
            )

        return puerto

    @classmethod
    def validar_rango(
        cls,
        puerto_inicial: int,
        puerto_final: int
    ) -> None:

        cls.validar_puerto(puerto_inicial)
        cls.validar_puerto(puerto_final)

        if puerto_inicial > puerto_final:
            raise ErrorValidacion(
                "El puerto inicial no puede ser "
                "mayor que el puerto final."
            )


class EscanerPuertos:
    """Realiza el escaneo TCP utilizando sockets."""

    def __init__(self, timeout: float = 0.3) -> None:

        if timeout <= 0:
            raise ValueError(
                "El tiempo de espera debe ser mayor que cero."
            )

        self._timeout = timeout

    def esta_abierto(self, ip: str, puerto: int) -> bool:
        """Comprueba si un puerto TCP acepta conexiones."""

        try:
            with socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM
            ) as cliente:

                cliente.settimeout(self._timeout)

                return cliente.connect_ex(
                    (ip, puerto)
                ) == 0

        except (socket.timeout, OSError):
            return False

    def escanear(
        self,
        configuracion: ConfiguracionEscaneo
    ) -> ResultadoEscaneo:
        """Analiza todos los puertos del rango indicado."""

        resultado = ResultadoEscaneo(configuracion)

        inicio = time.perf_counter()

        for puerto in range(
            configuracion.puerto_inicial,
            configuracion.puerto_final + 1
        ):

            if self.esta_abierto(
                configuracion.ip,
                puerto
            ):
                resultado.puertos_abiertos.append(
                    puerto
                )

        resultado.tiempo_total = (
            time.perf_counter() - inicio
        )

        return resultado


class Consola:
    """Gestiona la entrada y salida por consola."""

    ANCHO = 62

    @classmethod
    def linea(cls, caracter: str = "=") -> None:
        print(caracter * cls.ANCHO)

    @classmethod
    def titulo(cls, texto: str) -> None:
        print(texto.center(cls.ANCHO))

    @staticmethod
    def campo(nombre: str, valor: object) -> None:
        print(f"{nombre:<22}: {valor}")

    @classmethod
    def mostrar_encabezado(cls) -> None:

        print()

        cls.linea()
        cls.titulo("ESCÁNER DE PUERTOS TCP")
        cls.linea()

        cls.titulo(
            "Uso exclusivo en equipos y redes autorizadas"
        )

        cls.linea()

    @staticmethod
    def solicitar_ip() -> str:
        """Solicita y valida una dirección IPv4."""

        while True:

            entrada = input(
                f"\nDirección IPv4 [{IP_POR_DEFECTO}]: "
            ).strip()

            try:
                return ValidadorEntrada.validar_ip(
                    entrada or IP_POR_DEFECTO
                )

            except ErrorValidacion as error:
                print(f"[ERROR] {error}")

    @staticmethod
    def solicitar_puerto(
        mensaje: str,
        por_defecto: int
    ) -> int:
        """Solicita y valida un número de puerto."""

        while True:

            entrada = input(mensaje).strip()

            if not entrada:
                entrada = str(por_defecto)

            try:
                puerto = int(entrada)

            except ValueError:
                print(
                    "[ERROR] El puerto debe ser un número entero."
                )
                continue

            try:
                return ValidadorEntrada.validar_puerto(
                    puerto
                )

            except ErrorValidacion as error:
                print(f"[ERROR] {error}")

    @classmethod
    def solicitar_configuracion(
        cls
    ) -> ConfiguracionEscaneo:
        """Solicita la configuración interactiva."""

        ip = cls.solicitar_ip()

        while True:

            puerto_inicial = cls.solicitar_puerto(
                f"Puerto inicial "
                f"[{PUERTO_INICIAL_POR_DEFECTO}]: ",
                PUERTO_INICIAL_POR_DEFECTO
            )

            puerto_final = cls.solicitar_puerto(
                f"Puerto final "
                f"[{PUERTO_FINAL_POR_DEFECTO}]: ",
                PUERTO_FINAL_POR_DEFECTO
            )

            try:
                ValidadorEntrada.validar_rango(
                    puerto_inicial,
                    puerto_final
                )

                return ConfiguracionEscaneo(
                    ip=ip,
                    puerto_inicial=puerto_inicial,
                    puerto_final=puerto_final
                )

            except ErrorValidacion as error:
                print(f"[ERROR] {error}")
                print("Ingrese nuevamente el rango.\n")

    @staticmethod
    def configuracion_desde_argumentos(
        argumentos: list[str]
    ) -> ConfiguracionEscaneo:
        """Recibe IP, puerto inicial y puerto final."""

        if len(argumentos) != 3:
            raise ErrorValidacion(
                "Uso: python escaneo_red.py "
                "<ip> <puerto_inicial> <puerto_final>"
            )

        try:
            ip = ValidadorEntrada.validar_ip(
                argumentos[0]
            )

            inicio = int(argumentos[1])
            fin = int(argumentos[2])

        except ValueError as error:
            raise ErrorValidacion(
                "La dirección IP o los puertos "
                "ingresados no son válidos."
            ) from error

        ValidadorEntrada.validar_rango(
            inicio,
            fin
        )

        return ConfiguracionEscaneo(
            ip=ip,
            puerto_inicial=inicio,
            puerto_final=fin
        )

    @classmethod
    def mostrar_configuracion(
        cls,
        configuracion: ConfiguracionEscaneo
    ) -> None:

        print()

        cls.linea("-")
        cls.titulo("CONFIGURACIÓN DEL ESCANEO")
        cls.linea("-")

        cls.campo(
            "Dirección IPv4",
            configuracion.ip
        )

        cls.campo(
            "Puerto inicial",
            configuracion.puerto_inicial
        )

        cls.campo(
            "Puerto final",
            configuracion.puerto_final
        )

        cls.campo(
            "Puertos a analizar",
            configuracion.total_puertos
        )

        cls.linea("-")

        print("\nEstado: ESCANEANDO...\n")

    @classmethod
    def mostrar_resultado(
        cls,
        resultado: ResultadoEscaneo
    ) -> None:
        """Muestra los puertos abiertos y el resumen."""

        configuracion = resultado.configuracion

        if resultado.puertos_abiertos:

            cls.linea("-")
            cls.titulo("PUERTOS ABIERTOS")
            cls.linea("-")

            print(
                f"{'PUERTO':<10}"
                f"{'PROTOCOLO':<12}"
                f"{'ESTADO':<10}"
                f"SERVICIO"
            )

            cls.linea("-")

            for puerto in resultado.puertos_abiertos:

                servicio = SERVICIOS.get(
                    puerto,
                    "Desconocido"
                )

                print(
                    f"{puerto:<10}"
                    f"{'TCP':<12}"
                    f"{'ABIERTO':<10}"
                    f"{servicio}"
                )

        else:

            cls.linea("-")
            cls.titulo("RESULTADO")
            cls.linea("-")

            print(
                "No se encontraron puertos abiertos "
                "en el rango analizado."
            )

        print()

        cls.linea()
        cls.titulo("RESUMEN DEL ESCANEO")
        cls.linea()

        cls.campo(
            "Dirección IPv4",
            configuracion.ip
        )

        cls.campo(
            "Rango analizado",
            f"{configuracion.puerto_inicial} - "
            f"{configuracion.puerto_final}"
        )

        cls.campo(
            "Puertos analizados",
            resultado.total_analizados
        )

        cls.campo(
            "Puertos abiertos",
            resultado.total_abiertos
        )

        cls.campo(
            "Tiempo empleado",
            f"{resultado.tiempo_total:.2f} segundos"
        )

        cls.linea()
        cls.titulo("ESCANEO COMPLETADO")
        cls.linea()

        if 5000 in resultado.puertos_abiertos:
            print(
                "\nConfirmado: el puerto 5000 "
                "(servidor de pruebas Flask) está abierto."
            )


class AplicacionScanner:
    """Coordina la ejecución del escáner."""

    def __init__(
        self,
        escaner: EscanerPuertos | None = None
    ) -> None:

        self._escaner = (
            escaner or EscanerPuertos()
        )

    def ejecutar(self) -> None:

        Consola.mostrar_encabezado()

        if len(sys.argv) > 1:

            try:
                configuracion = (
                    Consola.configuracion_desde_argumentos(
                        sys.argv[1:]
                    )
                )

            except ErrorValidacion as error:
                print(f"[ERROR] {error}")
                return

        else:
            configuracion = (
                Consola.solicitar_configuracion()
            )

        Consola.mostrar_configuracion(
            configuracion
        )

        resultado = self._escaner.escanear(
            configuracion
        )

        Consola.mostrar_resultado(
            resultado
        )


def main() -> None:
    """Punto de entrada del programa."""

    try:
        AplicacionScanner().ejecutar()

    except KeyboardInterrupt:
        print(
            "\n\n[AVISO] Operación cancelada por el usuario."
        )

    except OSError as error:
        print(
            f"\n[ERROR] Se produjo un problema de red: {error}"
        )


if __name__ == "__main__":
    main()
