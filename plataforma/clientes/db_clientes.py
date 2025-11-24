# DBCLIENTES.PY
import json
import os
from .cliente import Cliente  # Importa el TDA
from ._preferencia import Preferencias  # Importa el TDA

DB_FILE = "db/clientes.json"


class DBClientes:
    # ... (Métodos internos _cargar_archivo y _guardar_archivo permanecen iguales,
    # pero ahora manejan diccionarios de datos crudos)
    def __init__(self):
        self.clientes = self._cargar_archivo()

    def _cargar_archivo(self) -> dict:
        """Carga el diccionario de clientes desde el archivo JSON."""

        # Si el archivo no existe o está vacío, devuelve un diccionario vacío
        if not os.path.exists(DB_FILE) or os.path.getsize(DB_FILE) == 0:
            return {}
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:

                data = json.load(f)
                # Devuelve el valor de la clave 'clientes', que ahora es un diccionario
                return data.get("clientes", {})

        except json.JSONDecodeError as e:
            # Si el JSON está mal formado, el problema no es mío
            print(
                f"Error fatal: El archivo '{DB_FILE}' no tiene un formato JSON válido: {e}"
            )

            return {}

    def _guardar_archivo(self):
        """Guarda el diccionario actual de clientes en el archivo JSON."""
        # Se guarda el diccionario completo con la clave 'clientes'
        data = {"clientes": self.clientes}
        try:
            with open(DB_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error al escribir en el archivo '{DB_FILE}': {e}")

    def obtener_todos(self) -> list:
        """Devuelve la lista de clientes (los valores del diccionario)."""
        # Aunque internamente es un dict, devolver los VALUES es útil para iterar
        return list(self.clientes.values())

    def obtener_por_id(self, cliente_id: str) -> Cliente | None:
        """Busca el diccionario de datos y LO CONVIERTE en un objeto Cliente."""
        cliente_data = self.clientes.get(cliente_id)
        if cliente_data is None:
            return None

        # 💡 Aquí es donde CONVERTIMOS el diccionario crudo a un TDA.
        # Ahora el TDA Cliente necesita una nueva forma de inicializarse.
        return self._diccionario_a_cliente(cliente_data)
    
    def obtener_por_nombre(self, nombre_cliente: str) -> Cliente | None:
        """Busca el diccionario de datos y LO CONVIERTE en un objeto Cliente."""
        cliente_data: dict[str, dict] = self.clientes
        cliente = {}

        if cliente_data is None:
            return None

        for datos_cliente in cliente_data.values():
            if datos_cliente["nombre"].lower() == nombre_cliente.lower():
                cliente.update(datos_cliente)

        # 💡 Aquí es donde CONVERTIMOS el diccionario crudo a un TDA.
        # Ahora el TDA Cliente necesita una nueva forma de inicializarse.
        return self._diccionario_a_cliente(cliente)

    def obtener_todos(self) -> list[Cliente]:
        """Devuelve una lista de objetos Cliente (TDA)."""
        return [self._diccionario_a_cliente(data) for data in self.clientes.values()]

    # Nuevo método para construir el objeto Cliente desde los datos crudos
    def _diccionario_a_cliente(self, data: dict) -> Cliente:
        """Función interna para construir un Cliente y sus Preferencias."""

        # 1. Crear el TDA Preferencias usando SOLO la data cruda, no la DB.
        preferencias_tda = Preferencias.from_dict(data.get("preferencias", {}))

        # 2. Crear el TDA Cliente inyectándole las Preferencias.
        # Quitamos la dependencia de Preferencias en el init del Cliente
        return Cliente(
            id=data.get("id"),
            nro_cliente=data.get("nro_cliente"),
            nombre=data.get("nombre"),
            apellido=data.get("apellido"),
            tipo_servicio=data.get("tipo_servicio"),
            fecha_alta=data.get("fecha_alta"),  # Pasa la string
            fecha_baja=data.get("fecha_baja"),  # Pasa la string
            preferencias=preferencias_tda,  # 💡 Inyección
        )

    def agregar_cliente(self, cliente: Cliente):
        """Añade un objeto Cliente (TDA) CONVIRTIÉNDOLO a diccionario y guarda."""
        # 💡 Convertimos el objeto Cliente A DICCIONARIO para guardar.
        cliente_data = self._cliente_a_diccionario(cliente)

        cliente_id = cliente_data.get("id")
        if not cliente_id:
            raise ValueError("El objeto Cliente debe tener un 'id' válido.")

        self.clientes[cliente_id] = cliente_data
        self._guardar_archivo()

    def _cliente_a_diccionario(self, cliente: Cliente) -> dict:
        """Convierte un objeto Cliente (TDA) de vuelta a diccionario para guardar."""
        # Esto te faltaba para que Preferencias guarde sus datos también.
        return {
            "id": cliente.id,
            "nro_cliente": cliente.nro_cliente,
            "nombre": cliente.nombre,
            "apellido": cliente.apellido,
            "tipo_servicio": cliente.tipo_servicio,
            "fecha_alta": cliente.fecha_alta.strftime("%Y-%m-%d"),  # Guarda como string
            "fecha_baja": (
                cliente.fecha_baja.strftime("%Y-%m-%d") if cliente.fecha_baja else None
            ),
            "preferencias": cliente.preferencias.to_dict(),  # Nuevo método
        }
