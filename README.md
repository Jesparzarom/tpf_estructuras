# 1. INTRODUCCION

En la actualidad, la industria del entretenimiento digital ha experimentado un crecimiento exponencial, consolidando a las plataformas de streaming como el medio principal de consumo de contenidos audiovisuales. La gestión de estos sistemas implica el manejo de grandes volúmenes de información heterogénea, que incluye desde catálogos extensos de películas, series y documentales, hasta bases de datos de usuarios con perfiles y preferencias complejas.

El objetivo de este Trabajo Final es el diseño y desarrollo de las estructuras de datos necesarias para soportar el funcionamiento de una Plataforma de Streaming. El sistema debe gestionar eficientemente un catálogo de contenidos multimedia diverso (series, películas y documentales) y la administración de usuarios (clientes), garantizando eficiencia y escalabilidad.

El desafío principal reside en modelar las relaciones entre los distintos tipos de contenidos, sus metadatos (etiquetas, actores, directores) y las preferencias personalizadas de los clientes para permitir funcionalidades futuras de búsqueda y recomendación.

<br>
<br>

# 2. SOBRE EL PROYECTO

## 2.1 OBJETIVOS DEL PROYECTO

### Objetivo General

Diseñar e implementar un sistema de gestión de contenidos multimedia y usuarios para una plataforma de streaming, utilizando el paradigma de Programación Orientada a Objetos (POO) y las estructuras de datos adecuadas para garantizar la eficiencia y escalabilidad del software.

### Objetivos Específicos

1. Modelar la heterogeneidad del catálogo (Herencia):
Implementar una jerarquía de clases que permita gestionar Películas, Series y Documentales bajo una estructura común (ContenidoBase), respetando sus atributos particulares (como directores, actores o duración).

2. Gestionar estructuras dinámicas complejas (Estructuras Anidadas):
Desarrollar una solución algorítmica para las Series que soporte una cantidad variable de temporadas y capítulos, adaptándose a la realidad de producciones de larga duración (ej. Grey's Anatomy).

3. Optimizar el acceso a datos de usuarios (Tablas Hash):
Implementar estructuras de acceso directo (Diccionarios/Tablas Hash) para la gestión de clientes, permitiendo búsquedas instantáneas por número de cliente sin comprometer el rendimiento del sistema.

4. Implementar un sistema de clasificación:
Integrar un sistema de etiquetas y preferencias robusto, utilizando TDAs auxiliares para categorizar el contenido de manera precisa y modelar los gustos del usuario.

<br>
<br>

# 3. PLATAFORMA

## 3.1. CLIENTES

### Objetivo del módulo `clientes`

- Modelar la entidad `Cliente` como TDA.
- Representar y manipular preferencias mediante el TDA `Preferencias`.
- Proveer una capa de servicio/manager `Clientes` que delega persistencia al Repository (`DBClientes`).

### Diseño y decisiones clave

- Separación de responsabilidades: TDAs para dominio, Repository para persistencia, Facade/Manager para orquestación.
- Inyección de dependencias: `Preferencias` se pasa al `Cliente` (mejor testabilidad y desacoplamiento).
- Lazy-loading: `Clientes.__init__` no carga todos los registros en memoria.
- Serialización: `from_dict` / `to_dict` para reconstruir y guardar TDAs.
- Uso de `datetime` para normalizar fechas (`fecha_alta`, `fecha_baja`).

**Componentes principales (cliente)**

- `Cliente` (TDA)
  - Campos y tipos principales:
    - `nro_cliente`: `str` (identificador del cliente)
    - `id`: `str` (opcional, por defecto igual a `nro_cliente`)
    - `nombre`, `apellido`: `str`
    - `fecha_alta`, `fecha_baja`: `datetime`
    - `tipo_servicio`: `str` (p. ej. "básico")
    - `preferencias`: `Preferencias` (TDA)
  
  - Operaciones clave (Descriptivas):
    - `.ver_perfil()`,
    - `.es_activo()`,
    - `.actualizar_tipo_servicio()`,
    - `.actualizar_perfil()`,
    - `.obtener_preferencias()`,
    - `.agregar_preferencia()`,
    - `.eliminar_preferencia()`.

<br>

- `Preferencias` (TDA)
  - Representa un `dict` con claves: `genero`, `actor`, `director`.
  - Métodos:
    - `.from_dict(data: dict) -> Preferencias`,
    - `.to_dict() -> dict`,
    - `.obtener_preferencia_tipo(tipo: str)`,
    - `.agregar_preferencia(tipo, nombre, nivel)`.

<br>

- `Clientes` (manejador / facade)
  - Interactúa con `DBClientes` (Repository). Ya que los TDA's no tienen
  porque saber de donde vienen los datos, ésta clase se encarga de ser un puente DB <=> Cliente y manejar TDA Cliente.

  - Operaciones:
    - `.obtener_clientes()`,
    - `.agregar_cliente(cliente)`,
    - `.obtener_cliente(nro_cliente)`.
    > No mantiene en memoria la colección completa por defecto.

<br>

### Fragmentos de código relevantes

#### TDA Cliente

`plataforma/clientes/cliente.py` (firma y métodos principales):

```python
class Cliente:
    def __init__(
        self,
        nro_cliente,
        nombre,
        apellido,
        fecha_alta,
        preferencias: Preferencias,
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
        self.preferencias = preferencias

    def es_activo(self):
        return self.fecha_baja is None

    def actualizar_tipo_servicio(self, nuevo_tipo: str):
        self.tipo_servicio = nuevo_tipo

    def obtener_preferencias(self):
        return self.preferencias
```

#### TDA Preferencias (de apoyo)

`plataforma/clientes/_preferencia.py` (construcción y serialización):

```python
class Preferencias:
    def __init__(self, preferencias_data: dict):
        self.preferencias = preferencias_data

    @classmethod
    def from_dict(cls, data: dict):
        data = {
            "genero": data.get("genero", {}),
            "actor": data.get("actor", {}),
            "director": data.get("director", {})
        }
        return cls(data)

    def to_dict(self):
        return self.preferencias

    def agregar_preferencia(self, tipo: str, nombre: str, nivel: float):
        if tipo not in self.preferencias:
            raise ValueError("Tipo inválido: debe ser 'genero', 'actor' o 'director'.")
        self.preferencias[tipo][nombre] = nivel
```

#### TDA Clientes (puente db - TDA)

`plataforma/clientes/clientes.py` (uso del Repository):

```python
from .cliente import Cliente
from .db_clientes import DBClientes

db = DBClientes()

class Clientes:
    def __init__(self):
        pass

    def obtener_clientes(self) -> list[Cliente]:
        return db.obtener_todos()

    def agregar_cliente(self, cliente: Cliente):
        db.agregar_cliente(cliente)

    def obtener_cliente(self, nro_cliente: str) -> Cliente | None:
        return db.obtener_por_id(nro_cliente)
```

### Ejemplo de JSON esperado (ejemplo mínimo)

```json
{
    "id": "C003",
    "nro_cliente": "C003",
    "nombre": "Juan",
    "apellido": "Esparza",
    "tipo_servicio": "Estándar",
    "fecha_alta": "2024-06-01",
    "fecha_baja": null,
    "preferencias": {
    "genero": {
        "Acción": 0.8,
        "Documental": 0.4
    },
    "actor": {
        "Denzel Washington": 0.9
    },
    "director": {}
    }
},

```

<br>
<br>

---

## 3.2. CONTENIDOS

### Justificación

- Reutilizar `ContenidoBase` evita duplicación de campos y centraliza la serialización.
- Representar `palabras_claves` como `set` facilita operaciones de búsqueda y deduplicado; al serializar se convierte a lista.
- Mantener estructuras de `temporadas` como `dict` permite acceso rápido por número de temporada y facilita recorridos y búsquedas.
- `to_dict()` en cada TDA asegura que la capa de persistencia reciba datos ya normalizados.


#### Se documentan los TDAs base para los contenidos (`ContenidoBase`) y las subclases `Pelicula`, `Documental` y `Serie`.

- `ContenidoBase` (TDA)
  - Campos y tipos principales:
    - `id`: `str` (identificador único del contenido)
    - `titulo`: `str`
    - `etiquetas`: `dict[str, int]` (género => nivel/score)
    - `palabras_claves`: `set[str]`
    - `anio`: `int`
    - `produccion`: `str`
    - `ids_secuelas`: `list[str]` (opcional)
  - Método útil: `to_dict()` que serializa el TDA para persistencia.

    Fragmento (resumen):

    ```python
    class ContenidoBase:
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
    ```

- `Pelicula` (TDA)
  - Extiende `ContenidoBase` y añade:
    - `director`: `str`
    - `actores`: `set[str]`
    - `duracion`: `int` (minutos)
  - `to_dict()` extiende la serialización base añadiendo campos propios.

    Fragmento:

    ```python
    class Pelicula(ContenidoBase):
            def __init__(self, director: str, actores: set[str], duracion: int, **kwargs):
                    super().__init__(**kwargs)
                    self.director = director
                    self.actores = actores
                    self.duracion = duracion

            def to_dict(self):
                    base = super().to_dict()
                    base.update({
                            "director": self.director,
                            "actores": list(self.actores),
                            "duracion": self.duracion,
                    })
                    return base
    ```

- `Documental` (TDA)
  - Extiende `ContenidoBase` y añade:
    - `director`: `str`
    - `fecha`: `str` (o `date` según preferencia)
    - `duracion`: `int`

    Fragmento:

    ```python
    class Documental(ContenidoBase):
            def __init__(self, director: str, fecha: str, duracion: int, **kwargs):
                    super().__init__(**kwargs)
                    self.director = director
                    self.fecha = fecha
                    self.duracion = duracion
    ```

- `Serie` (TDA)
  - Extiende `ContenidoBase` y añade:
    - `genero_principal`: `str`
    - `temporadas`: `dict[int, dict]` (estructura por temporada y capítulos)

    Fragmento:

    ```python
    class Serie(ContenidoBase):
            def __init__(self, genero: str, temporadas: dict[int, dict], **kwargs):
                    super().__init__(**kwargs)
                    self.genero_principal = genero
                    self.temporadas = temporadas
    ```

### Ejemplo de JSON para `Pelicula`

```json
{
    "id": "MTX1",
    "titulo": "The Matrix",
    "director": "Lana Wachowski, Lilly Wachowski",
    "actores": ["Keanu Reeves", "Laurence Fishburne", "Carrie-Anne Moss"],
    "duracion": 136,
    "produccion": "Warner Bros",
    "etiquetas": {"Ciencia Ficción": 1, "Acción": 0.9, "Cyberpunk": 1, "Distopía": 1, "Tecnología": 0.9},
    "palabras_claves": ["matrix", "realidad virtual", "neo", "revolución", "píldora"],
    "anio": 1999,
    "ids_secuelas": ["MTX2"]
}
```
