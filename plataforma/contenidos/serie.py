from .contenido_base import ContenidoBase


class Serie(ContenidoBase):
    def __init__(self, genero: str, temporadas: dict[int: dict], **kwargs):
        super().__init__(**kwargs)
        self.genero_principal = genero
        self.temporadas = temporadas


temporadas = {
    # Temporada n
    1: {
        # Datos de la temporada
        "año": 2020,
        "produccion": "Productora X",
        "capitulos": {
            # Capítulo n
            1: {
                # Datos del capítulo
                "id": "s1e1",
                "nombre": "Piloto | The Beginning",
                "duracion": 45,  # en minutos
            },
            2: {
                # Datos del capítulo
                "id": "s1e2",
                "nombre": "Capítulo 2 | The Continuation",
                "duracion": 45,  # en minutos
            },
        },
    },
}