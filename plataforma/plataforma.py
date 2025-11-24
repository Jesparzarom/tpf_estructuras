import os
from time import sleep
from typing import Optional, Dict, List
from enum import Enum
from .catalogo import NuevoCatalogo
from .contenidos import Pelicula, Documental
from .grafo_contenido import GrafoContenido
from .clientes import Clientes, Cliente
import traceback


class TipoContenido(Enum):
    """Enum para tipos de contenido disponibles"""

    PELICULAS = "peliculas"
    SERIES = "series"
    DOCUMENTALES = "documentales"


NOMBRE = "FAKEFLIX"
LOGO = """

***************************************************************
*                                                             *
* ███████╗ █████╗ ██╗  ██╗███████╗███████╗██╗    ██╗██╗  ██╗  *
* ██╔════╝██╔══██╗██║ ██╔╝██╔════╝██╔════╝██║    ██║╚██╗██╔╝  *
* █████╗  ███████║█████╔╝ █████╗  █████╗  ██║    ██║ ╚███╔╝   *
* ██╔══╝  ██╔══██║██╔═██╗ ██╔══╝  ██╔══╝  ██║    ██║ ██╔██╗   *
* ██║     ██║  ██║██║  ██╗███████╗██║     ███████╗██║██╔╝ ██╗ *
* ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝     ╚══════╝╚═╝╚═╝  ╚═╝ *
***************************************************************
                                                         
"""


def limpiar_pantalla():
    """Limpia la pantalla y muestra el logo"""
    os.system("cls" if os.name == "nt" else "clear")
    print(LOGO)


def pausa(mensaje: str = "\nPresiona ENTER para continuar..."):
    """Pausa la ejecución esperando input del usuario"""
    input(mensaje)


def animacion_carga(mensaje: str = "Cargando", duracion: float = 1.25):
    """Muestra una barra de carga animada"""
    print(f"\n{mensaje}")
    for _ in range(50):
        print("|", end="", flush=True)
        sleep(duracion / 50)
    print()


class Plataforma:
    """Gestiona el catálogo, clientes y estado de la sesión"""

    def __init__(self, nombre: str = NOMBRE):
        self.nombre = nombre
        self.catalogo = NuevoCatalogo()
        self.clientes = Clientes()

        # Estado de la sesión
        self._sesion_iniciada: bool = False
        self._cliente_actual: Cliente = None
        self._contenido_actual = None
        self._tipo_contenido_actual: TipoContenido | None = None

    @property
    def sesion_iniciada(self) -> bool:
        return self._sesion_iniciada

    @property
    def cliente_actual(self) -> Cliente | None:
        return self._cliente_actual

    @property
    def contenido_actual(self):
        return self._contenido_actual

    def obtener_catalogo(self, tipo: TipoContenido | None = None):
        """Obtiene el catálogo completo o filtrado por tipo"""
        if tipo:
            return self.catalogo.obtener_contenido_tipo(tipo.value)

        return {
            "peliculas": self.catalogo.db_peliculas,
            "series": self.catalogo.db_series,
            "documentales": self.catalogo.db_documentales,
        }

    def buscar_contenido(self, tipo: TipoContenido, id_contenido: str):
        """Busca un contenido específico por ID"""
        try:
            return self.catalogo.buscar_por_id(tipo=tipo.value, contenido_id=id_contenido)
        except Exception as e:
            traceback.print_exc()
            print(f"⚠️ Error al buscar contenido: {e}")
            sleep(10)
            return None

    def registrar_cliente(
        self,
        nombre: str,
        apellido: str,
        nro_cliente: str,
        fecha_alta: str,
        tipo_servicio: str = "básico",
    ) -> Cliente | None:
        """Registra un nuevo cliente en la plataforma"""
        try:
            nuevo_cliente = Cliente(
                nombre=nombre,
                apellido=apellido,
                nro_cliente=nro_cliente,
                fecha_alta=fecha_alta,
                tipo_servicio=tipo_servicio,
            )
            self.clientes.agregar_cliente(nuevo_cliente)
            return nuevo_cliente
        except Exception as e:
            print(f"⚠️ Error al registrar cliente: {e}")
            return None

    def iniciar_sesion(
        self, nro_cliente: str = None, nombre_cliente: str = None
    ) -> bool:
        """Inicia sesión con el numero o nombre del cliente"""
        cliente = (
            self.clientes.obtener_cliente(nro_cliente=nro_cliente)
            if nro_cliente
            else self.clientes.obtener_cliente(nombre_cliente=nombre_cliente)
        )

        if cliente:
            self._sesion_iniciada = True
            self._cliente_actual = cliente
            return True

        return False

    def cerrar_sesion(self):
        """Cierra la sesión actual"""
        self._sesion_iniciada = False
        self._cliente_actual = None
        self._contenido_actual = None
        self._tipo_contenido_actual = None

    def seleccionar_contenido(
        self, tipo: TipoContenido, contenido: Pelicula | Documental
    ):
        """Establece el contenido actual para reproducción"""
        self._tipo_contenido_actual = tipo
        self._contenido_actual = contenido


class Streaming:
    """Interfaz de usuario para la plataforma de streaming"""

    OPCIONES_INVITADO = {
        "1": "Iniciar Sesión",
        "2": "Películas",
        "3": "Series",
        "4": "Documentales",
        "0": "Salir",
    }

    OPCIONES_USUARIO = {
        "1": "Ver Perfil",
        "2": "Actualizar Perfil",
        "3": "Ver Preferencias",
        "4": "Ver Contenido Disponible",
        "5": "Seleccionar Contenido",
        "0": "Cerrar Sesión",
        "9": "Salir",
    }

    def __init__(self, plataforma: Plataforma):
        self.plataforma = plataforma

    def _mostrar_menu_base(self, opciones: dict[str, str], titulo: str):
        """Muestra un menú genérico"""
        limpiar_pantalla()
        print(f"========= {titulo} =========")
        for key, value in opciones.items():
            print(f"{key}. {value}")
        print("=" * (len(titulo) + 20))

    def mostrar_menu(self):
        """Muestra el menú según el estado de sesión"""
        if self.plataforma.sesion_iniciada:
            self._mostrar_menu_base(self.OPCIONES_USUARIO, "✅ MENÚ DE USUARIO")
        else:
            self._mostrar_menu_base(self.OPCIONES_INVITADO, "🚫 MENÚ INVITADO")

    def proceso_login(self):
        """Gestiona el proceso de inicio de sesión"""
        limpiar_pantalla()
        print("* [Usuarios prueba: priscila, leandro, juan, wenddy]")
        nombre_cliente = input("Ingresa tu nombre de cliente: ").strip()

        if not nombre_cliente:
            print("❌ ID de cliente vacío")
            sleep(1)
            return

        animacion_carga("Iniciando sesión")

        if self.plataforma.iniciar_sesion(nombre_cliente=nombre_cliente):
            print(f"👋 ¡Bienvenido/a, {self.plataforma.cliente_actual.nombre}!")
            sleep(1)
        else:
            print(f"❌ Cliente {nombre_cliente} no encontrado")
            sleep(2)

    def proceso_logout(self):
        """Cierra la sesión del usuario"""
        limpiar_pantalla()
        self.plataforma.cerrar_sesion()
        animacion_carga("Cerrando sesión")
        print("🔒 Sesión cerrada. ¡Hasta pronto!")
        sleep(1)

    def mostrar_perfil(self):
        """Muestra el perfil del usuario"""
        limpiar_pantalla()
        if self.plataforma.cliente_actual:
            print(self.plataforma.cliente_actual.ver_perfil())
        else:
            print("⚠️ No hay sesión iniciada")
        pausa()

    def mostrar_catalogo(self, tipo: TipoContenido):
        """Muestra el catálogo de un tipo específico"""
        limpiar_pantalla()
        print(f"\n📺 Catálogo: {tipo.value.title()}")
        print("=" * 50)

        contenidos = self.plataforma.obtener_catalogo(tipo)

        if not contenidos:
            print(f"El catálogo de {tipo.value} está vacío :(")
        else:
            for contenido in contenidos:
                print(f"[{contenido.id}] {contenido.titulo.title()} | {contenido.director.title()}")

        pausa()

    def seleccionar_tipo_contenido(self):
        """Permite al usuario seleccionar un tipo de contenido"""
        print("\nSelecciona tipo de contenido:")
        print("[1] Películas  |  [2] Documentales  |  [3] Series")

        seleccion = input(">>> ").strip()

        mapeo = {
            "1": TipoContenido.PELICULAS,
            "2": TipoContenido.DOCUMENTALES,
            "3": TipoContenido.SERIES,
        }

        return mapeo.get(seleccion)

    def reproducir_contenido(self):
        """Simula la reproducción de contenido"""
        limpiar_pantalla()

        tipo = self.seleccionar_tipo_contenido()
        if not tipo:
            print("⚠️ Opción no válida")
            sleep(1)
            return

        # Mostrar catálogo
        print(f"\n📺 Catálogo: {tipo.value.title()}")
        print("=" * 50)

        contenidos = self.plataforma.obtener_catalogo(tipo)
        if not contenidos:
            print(f"El catálogo de {tipo.value} está vacío")
            pausa()
            return

        for contenido in contenidos:
            print(f"[{contenido.id}] {contenido.titulo}")

        # Seleccionar contenido
        id_contenido = input("\nIngresa el ID del contenido: ").strip()
        if not id_contenido:
            print("Selección cancelada")
            sleep(1)
            return

        contenido = self.plataforma.buscar_contenido(tipo, id_contenido)
        if not contenido:
            print(f"❌ Contenido con ID '{id_contenido}' no encontrado")
            sleep(5)
            return

        self.plataforma.seleccionar_contenido(tipo, contenido)
        self._simular_reproduccion(tipo)

    def _simular_reproduccion(self, tipo: TipoContenido):
        """Simula la interfaz de reproducción"""
        limpiar_pantalla()
        contenido = self.plataforma.contenido_actual

        print(f"\n▶️ REPRODUCIENDO: {contenido.titulo.title()}\n")
        print("___________________________")
        print("|      \\(o__o)/            |")
        print("___________________________")
        print("[=============o------------]")
        print("◀◀  ❚❚  ▶  ▶▶")
        print()
        print("DETALLES")
        if tipo == "peliculas":
            print(f"Director: {contenido.director} | Actores: {",".join([actor for actor in contenido.actores])}")
            print(f"Duracion: {contenido.duracion} | Año: {contenido.anio}")
        elif tipo == "documentales":
            print(f"Director: {contenido.director} | Producción: {contenido.produccion}")
            print(f"Duracion: {contenido.duracion} | Año: {contenido.anio}")

        # Generar recomendaciones
        try:
            self._generar_recomendaciones(tipo, contenido)
        except Exception as e:
            print(f"⚠️ Error al generar recomendaciones: {e}")

        pausa("\nPresiona ENTER para terminar la reproducción")

    def _generar_recomendaciones(self, tipo: TipoContenido, contenido_actual: Dict):
        """Genera recomendaciones basadas en el contenido actual"""
        gc = GrafoContenido()

        # Agregar todos los contenidos al grafo
        contenidos = self.plataforma.obtener_catalogo(tipo)
        # `contenidos` habitualmente es una lista de objetos TDA; si fuera
        # una lista de dicts, `construir_desde_contenidos` los convertirá.
        gc.construir_desde_contenidos(contenidos, tipo=tipo.value)

        gc.generar_similitud(tipo=tipo.value)
        gc.generar_orden()

        print("\n🎬 RECOMENDACIONES BASADAS EN LO QUE ESTÁS VIENDO:")
        print("-" * 50)

        # `contenido_actual` es un objeto TDA; usar su atributo `id`.
        autoplay = gc.bfs_ver_similar(contenido_actual.id)
        for item_id in autoplay:
            item = gc.vertices_contenido.get(item_id)
            if item:
                print(f"[{item.id}] {item.titulo}")
        
        gc.ver_adyacencia_similitud()

    def ejecutar_opcion_invitado(self, opcion: str) -> bool:
        """Ejecuta una opción del menú de invitado"""
        if opcion == "1":
            self.proceso_login()
        elif opcion == "2":
            self.mostrar_catalogo(TipoContenido.PELICULAS)
        elif opcion == "3":
            self.mostrar_catalogo(TipoContenido.SERIES)
        elif opcion == "4":
            self.mostrar_catalogo(TipoContenido.DOCUMENTALES)
        elif opcion == "0":
            return False
        else:
            limpiar_pantalla()
            print("⛔ Opción no válida")
            sleep(1)

        return True

    def ejecutar_opcion_usuario(self, opcion: str) -> bool:
        """Ejecuta una opción del menú de usuario"""
        if opcion == "1":
            self.mostrar_perfil()
        elif opcion == "2":
            limpiar_pantalla()
            print("🛠️ Función de actualización de perfil no implementada")
            pausa()
        elif opcion == "3":
            limpiar_pantalla()
            print("⭐ Función de preferencias no implementada")
            pausa()
        elif opcion == "4":
            tipo = self.seleccionar_tipo_contenido()
            if tipo:
                self.mostrar_catalogo(tipo)
            else:
                print("⚠️ Opción no válida")
                sleep(1)
        elif opcion == "5":
            self.reproducir_contenido()
        elif opcion == "0":
            self.proceso_logout()
        elif opcion == "9":
            return False
        else:
            limpiar_pantalla()
            print("⛔ Opción no válida")
            sleep(1)

        return True

    def iniciar(self):
        """Bucle principal de la aplicación"""
        limpiar_pantalla()
        ejecutando = True

        while ejecutando:
            self.mostrar_menu()
            opcion = input("\nElige una opción: ").strip()

            if self.plataforma.sesion_iniciada:
                ejecutando = self.ejecutar_opcion_usuario(opcion)
            else:
                ejecutando = self.ejecutar_opcion_invitado(opcion)

        limpiar_pantalla()
        print("\n👋 Programa finalizado. ¡Adiós!")
        sleep(1)
