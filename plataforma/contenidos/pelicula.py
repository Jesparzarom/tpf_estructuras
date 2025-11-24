from .contenido_base import ContenidoBase


class Pelicula(ContenidoBase):
    """TDA para Películas"""

    def __init__(self, director: str, actores: set[str], duracion: int, **kwargs):
        """
        Args:
            nombre (str): Titulo de la película
            director (str): Director de la película
            actores (list): Actores que participan
            anio (int): Año de producción
            produccion (str): Casa productora
            etiquetas (list): Géneros y niveles de géneros
            palabras_clave (list): Lista de palabras clave.
        """
        super().__init__(**kwargs)
        self.director = director
        self.actores = actores
        self.duracion = duracion

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update(
            {
                "director": self.director,
                "actores": list(self.actores),
                "duracion": self.duracion,
            }
        )
        return base_dict

    @classmethod
    def from_dict(cls, data: dict):
        """
        Construye una instancia de Pelicula desde un diccionario de datos.
        """
        
        # 1. 🌟 Manejar y extraer los campos PROPIOS de Pelicula. 
        #    Usamos .pop() para quitar los campos propios del diccionario 'data'.
        #    Esto es clave: al final, 'data' solo contendrá los argumentos BASE.

        # No mutar el diccionario original: trabajamos sobre una copia
        data_copy = dict(data)

        director = data_copy.pop("director", None)
        duracion = data_copy.pop("duracion", None)

        # Convierte la lista (lo que viene del JSON) a set (el TDA lo necesita)
        actores_list = data_copy.pop("actores", [])
        actores = set(actores_list)

        # 2. El resto de la 'data' (lo que queda después de los .pop()) 
        #    SON los argumentos base (id, titulo, anio, etc.).
        
        # 3. 🚀 Llamar a cls() (el constructor de Pelicula)
        #    Pasamos los campos propios de forma explícita.
        #    Pasamos el resto de los argumentos BASE usando **data.

        return cls(
            director=director,
            actores=actores,
            duracion=duracion,
            **data_copy  # Los campos base (id, titulo, etiquetas, etc.) van aquí.
        )
    
    def __str__(self):
        return super().__str__() + f", Director: {self.director}, Actores: {', '.join(self.actores)}, Duración: {self.duracion} min"
    
    def __repr__(self):
        return super().__repr__() + f", Director: {self.director}, Actores: {', '.join(self.actores)}, Duración: {self.duracion} min"

    
    def __str__(self):
        return super().__str__() + f", Director: {self.director}, Actores: {', '.join(self.actores)}, Duración: {self.duracion} min"
    
    def __repr__(self):
        return super().__repr__() + f", Director: {self.director}, Actores: {', '.join(self.actores)}, Duración: {self.duracion} min"





class Peliculas:
    def __init__(self):
        pass