from .contenido_base import ContenidoBase
from datetime import datetime, date


class Documental(ContenidoBase):
    """TDA para Documentales"""

    def __init__(self, director: str, fecha: str, duracion: int, **kwargs):
        """
        Args:
            titulo (str): Titulo de la película
            director (str): Director de la película
            duracion (int): Duracion en minutos
            fecha (int): fecha de producción
            anio (int): año
            produccion (str): Casa productora
            palabras_clave (list): Lista de palabras clave.
            etiquetas (list): Géneros y niveles de géneros
        """
       # 💡 Los campos base se pasan a ContenidoBase
        super().__init__(**kwargs) 
        
        # Campos propios de Documental
        self.director = director

        # `fecha` puede venir como `str` (desde JSON) o como `datetime/date`.
        # - Si es datetime/date: formateamos a 'DD-MM-YYYY'.
        # - Si es str: intentamos parsearlo como ISO; si falla, lo dejamos como string.
        if isinstance(fecha, (datetime, date)):
            self.fecha = fecha.strftime("%d-%m-%Y")
        else:
            # Intentar parsear formatos ISO o comunes
            try:
                parsed = datetime.fromisoformat(str(fecha))
                self.fecha = parsed.strftime("%d-%m-%Y")
            except Exception:
                # Conservamos la representación tal cual (string)
                self.fecha = str(fecha)

        self.duracion = duracion


    def to_dict(self) -> dict:
        """Serializa el Documental a diccionario, incluyendo campos propios."""
        base_dict = super().to_dict()
        base_dict.update(
            {
                "director": self.director,
                "fecha": self.fecha,
                "duracion": self.duracion,
            }
        )
        return base_dict


    @classmethod
    def from_dict(cls, data: dict):
        """
        Construye una instancia de Documental desde un diccionario de datos.
        """
        
        # 1. 🌟 Manejar y extraer los campos PROPIOS de Documental. 
        #    Usamos .pop() para quitar los campos propios del diccionario 'data'.

        data_copy = data.copy()

        director = data_copy.pop("director")
        fecha = data_copy.pop("fecha")
        # Aseguramos que la duración sea un entero, si es que no lo era.
        duracion = data_copy.pop("duracion") 

        # 2. El resto de la 'data' (lo que queda después de los .pop()) 
        #    SON los argumentos base (id, titulo, anio, etc.).
        
        # 3. 🚀 Llamar a cls() (el constructor de Documental)
        #    Pasamos los campos propios de forma explícita.
        #    Pasamos el resto de los argumentos BASE usando **data.

        return cls(
            director=director,
            fecha=fecha,
            duracion=duracion,
            **data_copy  # 💡 **kwargs: Los campos base van al super()
        )
    
    # Opcionales, pero útiles para depuración
    def __str__(self):
        return super().__str__() + f", Director: {self.director}, Fecha: {self.fecha}, Duración: {self.duracion} min"
    
    def __repr__(self):
        return f"Documental({self.id}, {self.titulo}, {self.director}, {self.duracion})"