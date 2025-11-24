class Preferencias:
    """
    Clase TDA que representa  de las preferencias de un cliente.

    Args:
        cliente_id (str, opcional): El id del cliente para identificar la asociación.
        tipo_preferencia (str, opcional): El tipo de preferencia: "genero", "actor" o "director".
        nivel_preferencia (float, opcional): Nivel de preferencia entre 0 (bajo) y 1 (alto).
    """

    # 💡 Se inicializa directamente con los datos Puros.
    def __init__(self, preferencias_data: dict):
        self.preferencias = preferencias_data
    
    # 💡 Constructor alternativo para usar en el Repository
    @classmethod
    def from_dict(cls, data: dict):
        """Crea una instancia desde un diccionario crudo."""
        # Aseguramos la estructura base si viene vacío
        data = {
            "genero": data.get("genero", {}),
            "actor": data.get("actor", {}),
            "director": data.get("director", {})
        }
        return cls(data)

    # 💡 Método para convertir el TDA de vuelta a diccionario para guardar
    def to_dict(self):
        return self.preferencias

    def __str__(self):
        return str(self.preferencias)

    def __repr__(self):
        return self.__str__()

    def obtener_preferencias(self):
        """Retorna las preferencias del cliente."""
        return self.preferencias

    def obtener_preferencia_tipo(self, tipo: str):
        """Retorna las preferencias del cliente por tipo (genero, actor, director)."""
        return self.preferencias.get(tipo, {})
    
    def agregar_preferencia(self, tipo: str, nombre: str, nivel: float):
        """Agrega una preferencia específica dentro de genero, actor o director"""
        if tipo not in self.preferencias:
            # Ahora la validación es más estricta si from_dict asegura las claves.
            raise ValueError(
                f"Tipo inválido: {tipo}, debe ser 'genero', 'actor' o 'director'."
            )
        # Si el tipo existe, agregamos/actualizamos
        self.preferencias[tipo][nombre] = nivel