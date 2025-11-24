from .cliente import Cliente
from .db_clientes import DBClientes

db = DBClientes() 

class Clientes:
    def __init__(self):
        # 💡 Ya no se carga todo en memoria en el init (es ineficiente). 
        # Ahora se usa el Repository para obtener los objetos SOLO cuando se necesitan.
        pass # self.clientes = db.obtener_todos() <-- ¡Mal!
    
    def obtener_clientes(self) -> list[Cliente]:
        """Obtiene TODOS los clientes (TDA) del Repository (DB)."""
        return db.obtener_todos() # Llama al método del Repository que devuelve TDA Cliente

    def agregar_cliente(self, cliente: Cliente):
        """Recibe el TDA Cliente y se lo pasa al Repository para que lo guarde."""
        db.agregar_cliente(cliente) # El Repository sabe cómo convertir Cliente a Dict y guardar

    def obtener_cliente(self, nro_cliente: str=None, nombre_cliente:str=None) -> Cliente | None:
        """Pide al Repository el TDA Cliente por ID."""
        if nro_cliente:
            return db.obtener_por_id(nro_cliente) # Llama al método del Repository que devuelve TDA Cliente
        if nombre_cliente:
            return db.obtener_por_nombre(nombre_cliente)

    def __str__(self):
        return f"Clientes: {self.clientes}"
    
    def __repr__(self):
        return self.__str__()
    
    def __iter__(self):
        return iter(self.clientes)
