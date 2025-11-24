from ._preferencia import Preferencias
from datetime import datetime


def perfil_cliente(cliente: Cliente) -> str:
    """
    Genera una representación bonita y legible de los datos de un cliente.
    """

    # Manejo si el cliente es None o no tiene datos (por si acaso)
    if not cliente:
        return "❌ Cliente no encontrado."

    # Extraemos las preferencias para un formato más limpio
    preferencias = cliente.obtener_preferencias().to_dict()

    genero = "\n".join(f" -- {gen} | {int(peso * 100)}%" for gen, peso in preferencias["genero"].items())
    actores = "\n".join(f" -- {gen} | {int(peso * 100)}%" for gen, peso in preferencias["actor"].items())
    directores = "\n".join(f" -- {gen} | {int(peso * 100)}%" for gen, peso in preferencias["director"].items())


    # Formateamos las preferencias en una lista de strings para unirlas después


    # --- Creación de la Plantilla de Salida (f-string multilínea) ---
    return f"""
        ________________________
                        
        |    #############     |
        |    ##         ##     |   
        |    #  ~~   ~~  #     |   
        |    #  ()   ()  #     |   
        |    (     ^     )     |   
        |     |         |      | 
        |     |  (===)  |      |
        |      \       /       |
        |      / -----  \      |
        |  ---  |%\ /%|  ---   | 
        | /     |%%%%%|     \  | 
        |       |%/ \%|        |
        ________________________   
                                                                                                                                      
======================================
         FICHA DEL CLIENTE
======================================
ID Cliente:       {cliente.id} ({cliente.nro_cliente})
Nombre Completo:  {cliente.nombre} {cliente.apellido}
-------------------------------------
Servicio:         {cliente.tipo_servicio}
Fecha de Alta:    {cliente.fecha_alta}
---------------------------------------
PREFERENCIAS:

- GENERO:
{genero}

- ACTORES:
{actores}

- DIRECTORES:
{directores or ' -- Sin preferencias'}
======================================
"""


class Cliente:
    """
    Clase TDA

    Args:
        nombre (str, optional): fsfsfssfs
        NRO cliente:
        preferencias:
            género,
            actor,
            director
            porcentaje que permite determinar el nivel de preferencia,
        tipo de servicio que consume
        fecha de alta
        fecha de baja.
    """

    def __init__(
        self,
        nro_cliente,
        nombre,
        apellido,
        fecha_alta,
        preferencias: Preferencias, # 💡 INYECCIÓN
        tipo_servicio="básico",
        fecha_baja=None,
        id=None,
    ):
        self.id = id if id is not None else nro_cliente 
        self.nro_cliente = nro_cliente
        self.nombre = nombre
        self.apellido = apellido
        self.tipo_servicio = tipo_servicio
        self.fecha_alta = datetime.strptime(fecha_alta, "%Y-%m-%d")
        self.fecha_baja = (
            datetime.strptime(fecha_baja, "%Y-%m-%d") if fecha_baja else None
        )
        self.preferencias = preferencias # 💡 ¡Asignación directa!

    def ver_perfil(self):
        return perfil_cliente(self)

    def es_activo(self):
        """Verifica si el cliente está activo (sin fecha de baja)."""
        return self.fecha_baja is None

    def actualizar_tipo_servicio(self, nuevo_tipo: str):
        """Actualiza el tipo de servicio del cliente."""
        self.tipo_servicio = nuevo_tipo

    def actualizar_perfil(self, nombre: str = None, apellido: str = None):
        """Actualiza el nombre y/o apellido del cliente."""
        if nombre:
            self.nombre = nombre
        if apellido:
            self.apellido = apellido

    def obtener_preferencias(self):
        """Retorna las preferencias del cliente."""
        return self.preferencias

    def obtener_preferencia_tipo(self, tipo: str):
        """Retorna las preferencias del cliente por tipo (genero, actor, director)."""
        return self.preferencias.obtener_preferencia_tipo(tipo)

    def agregar_preferencia(self, tipo: str, nombre: str, nivel: float):
        """Agrega una preferencia específica dentro de genero, actor o director"""
        self.preferencias.agregar_preferencia(tipo, nombre, nivel)

    def eliminar_preferencia(self, tipo: str, nombre: str):
        """Elimina una preferencia específica dentro de genero, actor o director"""
        if (
            tipo in self.preferencias.preferencias[self.nro_cliente]
            and nombre in self.preferencias.preferencias[self.nro_cliente][tipo]
        ):
            del self.preferencias.preferencias[self.nro_cliente][tipo][nombre]

    def __str__(self):
        return (
            f"{self.nro_cliente}, {self.nombre}, {self.apellido}, {self.tipo_servicio}"
        )

    def __repr__(self):
        return self.__str__()

    def __iter__(self):
        return iter(self)
    
