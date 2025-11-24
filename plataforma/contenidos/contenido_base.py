class ContenidoBase:
    """TDA Contenido Base que representa el contenido común a películas, documentales y series.
    Puede ser heredado por otros tipos de contenido más específicos.

    Args:
        nombre: Nombre del contenido
        etiquetas: Dict con género como clave y nivel como valor
                Ej: {"comedia": "alto", "accion": "bajo"}
        palabras_clave: Set de palabras que describen el contenido
                Ej: {"aventura", "emocionante", "familiar"}
    """

    def __init__(
        self,
        id: str,
        titulo: str,
        etiquetas: dict[str, int],
        palabras_claves: set[str],
        anio: int,
        produccion: str,
        ids_secuelas: list[str] = [],
    ):
        self.id = id
        self.titulo = titulo
        self.etiquetas = etiquetas
        self.palabras_claves = palabras_claves
        self.anio = anio
        self.produccion = produccion
        self.ids_secuelas = ids_secuelas

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "etiquetas": self.etiquetas,
            "palabras_claves": list(self.palabras_claves),
            "anio": self.anio,
            "produccion": self.produccion,
            "ids_secuelas": self.ids_secuelas,
        }

    # 1. Método de Clase para Deserialización
    @classmethod
    def from_dict(cls, data: dict):
        """
        Método de clase que construye una instancia del TDA (Pelicula, Documental, etc.)
        a partir de un diccionario crudo (desde el JSON).
        """
        # Aquí defines la lógica genérica. Si solo hay datos comunes,
        # puedes intentar instanciar directamente:


        # Retorna una nueva instancia usando el método __init__
        return cls(
            id=data.get("id"),
            titulo=data.get("titulo"),
            etiquetas=data.get("etiquetas"),
            palabras_claves=set(data.get("palabras_claves")),
            anio=data.get("anio"),
            produccion=data.get("produccion"),
            ids_secuelas= data.get("ids_secuelas"),
        )
