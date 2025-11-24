import json
import os
from .pelicula import Pelicula      # Asume que estos son tus TDA
from .documental import Documental  # Asume que tienen from_dict/to_dict
from .serie import Serie            # Asume que tienen from_dict/to_dict


# Rutas estáticas de la base de datos (DB)
DB_PELIS_FILE = "db/peliculas.json"
DB_DOCUS_FILE = "db/documentales.json"
DB_SERIES_FILE = "db/series.json"


class DBContenidos:
    """
    Clase para gestionar la persistencia de Contenidos (Peliculas,
    Documentales o Series) en archivos JSON.
    """
    def __init__(self, tipo: str):
        """Inicializa la DB para un tipo específico y carga los datos."""
        self.tipo = tipo.lower() # 'peliculas', 'documentales', o 'series'
        self.contenido = self._cargar_archivo(self.tipo)

    # --- 1. Métodos de Utilería y Persistencia ---

    def _obtener_file_path(self, tipo: str) -> str:
        """Devuelve la ruta del archivo JSON según el tipo de contenido."""
        if tipo == "peliculas":
            return DB_PELIS_FILE
        elif tipo == "documentales":
            return DB_DOCUS_FILE
        elif tipo == "series":
            return DB_SERIES_FILE
        else:
            raise ValueError(f"Tipo de contenido no soportado: {tipo}")


    def _cargar_archivo(self, tipo: str) -> dict:
        """Carga el diccionario de contenidos desde el archivo JSON."""
        DB_FILE = self._obtener_file_path(tipo)

        if not os.path.exists(DB_FILE) or os.path.getsize(DB_FILE) == 0:
            return {}
            
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                # La clave es el tipo (e.g., 'peliculas')
                return data.get(tipo, {})

        except json.JSONDecodeError as e:
            # Si el JSON está mal, hay que avisar de forma brutal.
            print(f"Error fatal: El archivo '{DB_FILE}' no tiene un formato JSON válido: {e}")
            return {}
        except Exception as e:
            print(f"Error desconocido al cargar el archivo '{DB_FILE}': {e}")
            return {}


    def _guardar_archivo(self, tipo: str):
        """Guarda el diccionario actual de contenidos en el archivo JSON."""
        DB_FILE = self._obtener_file_path(tipo)
        
        # Se guarda el diccionario completo con la clave que es el tipo (e.g., 'peliculas')
        data = {tipo: self.contenido}

        try:
            with open(DB_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error al escribir en el archivo '{DB_FILE}': {e}")


    # --- 2. Métodos de Conversión (Serialización/Deserialización) ---
    
    def _diccionario_a_objeto(self, data: dict):
        """Construye el TDA apropiado (Pelicula, Documental, Serie) desde un diccionario."""
        # Usa el tipo de la instancia para decidir qué clase invocar.
        if self.tipo == "peliculas":
            return Pelicula.from_dict(data)
        elif self.tipo == "documentales":
            return Documental.from_dict(data)
        elif self.tipo == "series":
            return Serie.from_dict(data)
        # El caso 'else' ya se maneja en __init__ o _obtener_file_path, 
        # pero por seguridad, mejor dejarlo robusto:
        raise ValueError(f"No puedo convertir diccionario a objeto para el tipo: {self.tipo}")
        
    
    def _objeto_a_diccionario(self, objeto) -> dict:
        """Convierte un objeto TDA (Pelicula, etc.) de vuelta a diccionario para guardar."""
        # Esto es simple: si el objeto es un TDA, DEBE tener un método to_dict().
        if hasattr(objeto, 'to_dict') and callable(getattr(objeto, 'to_dict')):
            return objeto.to_dict()
        else:
            raise TypeError(f"El objeto de tipo {type(objeto)} no tiene un método 'to_dict()' para serializarlo.")


    # --- 3. Operaciones CRUD Básicas ---

    def obtener_todos(self) -> list[Pelicula | Documental | Serie]:
        """Devuelve una lista de todos los objetos TDA (Pelicula, Documental, Serie)."""
        # Comprensión de lista simple y eficiente.
        return [self._diccionario_a_objeto(data) for data in self.contenido]

    
    def obtener_por_id(self, contenido_id: str) -> Pelicula | Documental | Serie:
        """Busca y devuelve el objeto TDA por su ID, o None si no se encuentra."""
        lista_contenidos = self.obtener_todos()
        # Buscamos el objeto ya convertido en la lista de objetos
        for contenido in lista_contenidos:
            if getattr(contenido, 'id', None) == contenido_id:
                return contenido

        # No se encontró
        return None


    def agregar_contenido(self, contenido):
        """Añade o actualiza un objeto TDA y lo guarda en el archivo JSON."""
        # 💡 Convertimos el objeto TDA A DICCIONARIO para persistir.
        contenido_data = self._objeto_a_diccionario(contenido)

        # Asumo que el campo clave es 'id' para todos tus contenidos.
        contenido_id = contenido_data.get("id")
        if not contenido_id:
            raise ValueError("El objeto de contenido debe tener un 'id' válido.")

        # Si self.contenido es una lista (estructura actual del JSON), inserta o reemplaza
        if isinstance(self.contenido, list):
            for i, item in enumerate(self.contenido):
                if item.get("id") == contenido_id:
                    self.contenido[i] = contenido_data
                    break
            else:
                # No existía, lo agregamos
                self.contenido.append(contenido_data)

        # Si por alguna razón es un dict (versiones anteriores), mantener compatibilidad
        elif isinstance(self.contenido, dict):
            self.contenido[contenido_id] = contenido_data

        else:
            raise TypeError("Estructura de 'self.contenido' inesperada. Debe ser lista o dict.")

        # Guarda todo el diccionario persistente.
        self._guardar_archivo(self.tipo)

    def eliminar_contenido(self, contenido_id: str) -> bool:
            """
            Elimina un contenido por su ID, si existe, y guarda los cambios.
            Devuelve True si se eliminó, False si no se encontró.
            """
            # Si la estructura es lista, buscamos por id y removemos
            if isinstance(self.contenido, list):
                for i, item in enumerate(self.contenido):
                    if item.get("id") == contenido_id:
                        self.contenido.pop(i)
                        self._guardar_archivo(self.tipo)
                        return True
                return False

            # Si es dict, eliminar por clave
            if isinstance(self.contenido, dict):
                if contenido_id in self.contenido:
                    del self.contenido[contenido_id]
                    self._guardar_archivo(self.tipo)
                    return True
                return False

            # Estructura inesperada
            raise TypeError("Estructura de 'self.contenido' inesperada. Debe ser lista o dict.")