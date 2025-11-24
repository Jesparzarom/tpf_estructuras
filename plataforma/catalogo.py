from .contenidos.contenido_base import ContenidoBase
from .contenidos.db_contenidos import DBContenidos 

class NuevoCatalogo:
    """
    Fachada que centraliza el acceso y la gestión de todos los tipos de contenido 
    utilizando las clases DBContenidos como capa de persistencia.
    """
    def __init__(self):
        # 💡 Inicializamos las instancias de los gestores DB (Controladores)
        self.db_peliculas = DBContenidos("peliculas")
        self.db_series = DBContenidos("series")
        self.db_documentales = DBContenidos("documentales")
        
        # 💡 Mantenemos un mapa para acceso rápido
        self._gestores = {
            "peliculas": self.db_peliculas,
            "series": self.db_series,
            "documentales": self.db_documentales,
        }

    # --- Métodos de Acceso al Gestor (Encapsulación) ---

    def _obtener_gestor(self, tipo: str) -> DBContenidos:
        """Función interna para obtener el gestor de DB adecuado."""
        gestor = self._gestores.get(tipo.lower())
        if gestor is None:
            raise ValueError(f"Tipo de contenido no válido: {tipo}")
        return gestor


    def obtener_contenido_tipo(self, tipo: str):
        """Devuelve una lista de objetos TDA (no diccionarios) para un tipo."""
        # 💡 Pedimos al gestor que cargue y convierta la data.
        return self._obtener_gestor(tipo).obtener_todos()


    def agregar_contenido_tipo(self, tipo: str, contenido: ContenidoBase):
        """Añade/Actualiza contenido, delegando la persistencia al gestor."""
        # 💡 Delegamos la serialización y guardado al gestor.
        self._obtener_gestor(tipo).agregar_contenido(contenido)


    def elminar_contenido_tipo(self, tipo: str, contenido_id: str):
        """Delega la eliminación al gestor."""
        # 💡 Delegamos la eliminación al gestor.
        return self._obtener_gestor(tipo).eliminar_contenido(contenido_id)
        
    # --- Métodos de Búsqueda ---

    def buscar_por_id(self, tipo: str, contenido_id: str):
        """Busca un solo contenido por ID, usando la eficiencia del diccionario."""
        # 💡 Usamos el método eficiente de DBContenidos (acceso O(1)).
        return self._obtener_gestor(tipo).obtener_por_id(contenido_id)

    # El método buscar_y_ver de antes iteraba ineficientemente:
    # return self.buscar_por_id(tipo, contenido_id) # Usaría este en su lugar


    def buscar(self, titulo=None, etiquetas=None, palabras_claves=None, id_contenido=None) -> list[ContenidoBase]:
        """
        Busca en todos los contenidos cargados aplicando los filtros.
        """
        resultados = []
        
        # 💡 Ahora iteramos sobre todos los gestores y les pedimos la data (si es necesario)
        # NOTA: Para no sobrecargar la memoria, es mejor pedir la data solo cuando se busca.
        
        # 1. Obtenemos todos los TDA de todos los tipos:
        todos_los_contenidos = []
        for gestor in self._gestores.values():
            todos_los_contenidos.extend(gestor.obtener_todos())
        
        # 2. Aplicamos la lógica de filtrado sobre los TDA:
        for c in todos_los_contenidos:
            match = True
            
            # Busqueda por ID (si se proporciona)
            if id_contenido and id_contenido.lower() not in c.id.lower():
                match = False
                
            # Busqueda por título
            if titulo and titulo.lower() not in c.titulo.lower():
                match = False
                
            # Busqueda por etiquetas
            # Usamos any() para buscar una intersección de claves.
            if etiquetas and not any(e in c.etiquetas for e in etiquetas):
                match = False
                
            # Busqueda por palabras clave
            # Usamos isdisjoint() para ver si NO tienen elementos comunes
            if palabras_claves and set(palabras_claves).isdisjoint(c.palabras_claves):
                match = False
                
            if match:
                resultados.append(c)
                
        return resultados