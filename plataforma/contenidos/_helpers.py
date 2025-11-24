import json


class Pila:
    def __init__(self):
        self._items = []

    def esta_vacia(self):
        return not self._items

    def apilar(self, item):
        self._items.append(item)

    def desapilar(self):
        if not self.esta_vacia():
            return self._items.pop()
        raise IndexError("pop from empty stack")

    def __iter__(self):
        return iter(self.items)

    # Implementación necesaria para verificar si un elemento ya está en la pila
    def __contains__(self, item):
        return item in self._items


class Cola:
    def __init__(self):
        # Usamos una lista para simplicidad, pero para grandes volúmenes
        # (que no es tu caso), se debería usar collections.deque
        self._items = []

    def esta_vacia(self):
        return not self._items

    def encolar(self, item):
        self._items.append(item)

    def desencolar(self):
        if not self.esta_vacia():
            # Desencolar es el primer elemento (índice 0)
            return self._items.pop(0)
        raise IndexError("dequeue from empty queue")

    # Implementación necesaria para verificar si un elemento ya está en la cola
    def __contains__(self, item):
        return item in self._items

    def __iter__(self):
        return iter(self.items)


def _obtener_etiquetas_predefinidas(tipo):
    """
    Devuelve conjuntos predefinidos de etiquetas temáticas con pesos alto, medio y bajo,
    dependiendo del tipo de contenido solicitado ('peliculas', 'documentales', 'series').

    Args:
        tipo (str): El tipo de contenido para el cual se requieren las etiquetas.
                    Debe ser 'peliculas', 'documentales', o 'series'.

    Returns:
        tuple[set[str], set[str], set[str]]: Una tupla conteniendo tres conjuntos:
            - etiquetas_peso_alto (set): Etiquetas con máxima relevancia (peso implícito 5-4).
            - etiquetas_peso_medio (set): Etiquetas de relevancia secundaria (peso implícito 3-2).
            - etiquetas_peso_bajo (set): Etiquetas de formato o tono (peso implícito 1).

    """
    etiquetas_peso_alto = {}
    etiquetas_peso_medio = {}
    etiquetas_peso_bajo = {}

    # Etiqurtas para PELICULAS
    if tipo == "peliculas":
        etiquetas_peso_alto = {"Dinosaurios","Fantasía de Mundo","Cyberpunk","Arqueología", "Juventud", "Superhéroes",}
        etiquetas_peso_medio = {"Tecnología","Distopía","Histórica","Mar","Magia","Sobrenatural",}
        etiquetas_peso_bajo = {"Acción", "Aventura", "Comedia", "Drama", "Familia",}
    
    # Etiquetas para DOCUMENTALES 
    elif tipo == "documentales":
        etiquetas_peso_alto = {"Ciencia", "Historia", "Medio-Ambiente", "Crimen-Real", "Biografía", "Política"}
        etiquetas_peso_medio = {"Música", "Arte", "Exploración", "Guerra", "Deporte", "Tecnología"}
        etiquetas_peso_bajo = {"Entrevista", "Narración-en-off", "Investigación", "Social", "Viajes"}
    
    # Etiquetas para SERIES
    elif tipo == "series":
        etiquetas_peso_alto = {"Fantasia-Oscura", "Ciencia-Ficción", "Thriller-Psicológico", "Misterio", "Western", "Histórica"}
        etiquetas_peso_medio = {"Policial", "Comedia-Negra", "Juvenil", "Superhéroes", "Romance", "Acción-Militar"}
        etiquetas_peso_bajo = {"Sitcom", "Procedimental", "Telenovela", "Animación", "Épica"}

    return etiquetas_peso_alto, etiquetas_peso_medio, etiquetas_peso_bajo


def _calcular_pesos_maraton(a, b, tipo=None):
    """
    Calcula el peso de similitud para rutas de 'Maratón Temático' (DFS).
    Prioriza ETIQUETAS DE BAJO PESO (Estilo/Formato) y PALABRAS CLAVE.
    """
    peso = 0
    
    # 1. SECUELAS (Máxima prioridad)
    if b.id in a.ids_secuelas or a.id in b.ids_secuelas:
        return 100.0

    # 2. DIRECTOR (Menos importante para la inmersión temática)
    if hasattr(a, "director") and a.director == b.director:
        peso += 0.5 # Valor nominal

    # --- ETIQUETAS PREDEFINIDAS ---
    ETIQUETAS_ALTO_PESO, ETIQUETAS_MEDIO_PESO, ETIQUETAS_BAJO_PESO = _obtener_etiquetas_predefinidas(tipo=tipo)
    etiquetas_comunes = set(a.etiquetas.keys()) & set(b.etiquetas.keys())

    for tag in etiquetas_comunes:
        valor_base = min(a.etiquetas.get(tag, 0), b.etiquetas.get(tag, 0))

        if tag in ETIQUETAS_BAJO_PESO:
            # 🚀 Nivel ORO Maratón: Coherencia de Estilo/Tono es crucial para el DFS.
            peso += valor_base * 5.0
        
        elif tag in ETIQUETAS_MEDIO_PESO:
            # Nivel PLATA.
            peso += valor_base * 2.5
            
        elif tag in ETIQUETAS_ALTO_PESO:
            # 🐌 Nivel BRONCE: Reducimos el peso de Género principal para explorar.
            peso += valor_base * 0.5
        
        else:
            peso += valor_base * 1.0

    # 3. PALABRAS CLAVE (CRÍTICO para la profundidad temática)
    comunes_keywords = set(a.palabras_claves) & set(b.palabras_claves)
    # 🚀 Aumentamos el peso: Asegura que el DFS siga una línea narrativa o subtema fuerte.
    peso += 5.0 * len(comunes_keywords) 

    return peso

def _calcular_pesos_similares(a, b, tipo=None):
    """
    Calcula el peso de similitud para recomendaciones 'Similares' (BFS).
    Prioriza ETIQUETAS DE ALTO PESO (Género y Tema Principal) y DIRECTOR.
    """
    peso = 0
    
    # 1. SECUELAS (Máxima prioridad)
    if b.id in a.ids_secuelas or a.id in b.ids_secuelas:
        return 100.0

    # 2. DIRECTOR (El toque personal - importante para afinidad general)
    if hasattr(a, "director") and a.director == b.director:
        peso += 2.0 # Subimos un poco el peso del director

    # --- ETIQUETAS PREDEFINIDAS ---
    ETIQUETAS_ALTO_PESO, ETIQUETAS_MEDIO_PESO, ETIQUETAS_BAJO_PESO = _obtener_etiquetas_predefinidas(tipo=tipo)
    etiquetas_comunes = set(a.etiquetas.keys()) & set(b.etiquetas.keys())

    for tag in etiquetas_comunes:
        valor_base = min(a.etiquetas.get(tag, 0), b.etiquetas.get(tag, 0))

        if tag in ETIQUETAS_ALTO_PESO:
            # 🚀 Nivel ORO: Lo más importante para el BFS de afinidad.
            peso += valor_base * 5.0

        elif tag in ETIQUETAS_MEDIO_PESO:
            # Nivel PLATA.
            peso += valor_base * 2.5

        elif tag in ETIQUETAS_BAJO_PESO:
            # 🐌 Nivel BRONCE: Poca importancia en la similitud inmediata.
            peso += valor_base * 0.5
        
        else:
            peso += valor_base * 1.0

    # 3. PALABRAS CLAVE (Refuerzo, pero no dominante)
    comunes_keywords = set(a.palabras_claves) & set(b.palabras_claves)
    peso += 2.0 * len(comunes_keywords) 

    return peso



def obtener_pesos_aristas(a, b, tipo=None, algoritmo=None):
    """
    Calcula un peso de similitud entre dos contenidos para construir relaciones
    de recomendación en el grafo.

    Parameters
    ----------
    a : ContenidoBase
        Primer objeto de contenido (película, serie, documental).
    b : ContenidoBase
        Segundo objeto de contenido (película, serie, documental).

    Notas
    -----
    Los objetos 'a' y 'b' deben contener los siguientes atributos para el cálculo:
        - director (str)
        - actores (set)
        - produccion (str)
        - etiquetas (dict con niveles 0-1)
        - palabras_claves (set)

    Returns
    -------
    float
        Peso de la arista (valor de similitud) entre los contenidos, normalmente entre 0.0 y 1.0.
    """
    peso = 0

    if algoritmo == "similares":
        peso = _calcular_pesos_similares(a, b, tipo)
    if algoritmo == "maraton":
        peso = _calcular_pesos_maraton(a, b, tipo)
    return peso


def _obtener_path(tipo: str):
    path = ""
    if tipo:
        if tipo == "peliculas":
            path = "db/peliculas.json"
        elif tipo == "documentales":
            path = "db/documentales.json"
        elif tipo == "series":
            path = "db/series.json"
    return path


def obtener_contenido(tipo):
    """Obtiene los contenidos de la base de datos por tipo de contenido.

    Args:
        tipo (str): "películas", "documentales" o "series"

    Returns :
        Catálogo de contenidos por tipo

    """

    path = _obtener_path(tipo)

    # Catálogo global
    with open(path, encoding="utf8") as f:
        data = json.load(f)
        catalogo_pelis = data[tipo]

    return catalogo_pelis


def guardar_contenido(tipo, contenido, path):
    """Guardar contenido en la base de datos"""
    path = _obtener_path(tipo)

    # 1. Leer los datos existentes
    try:
        with open(path, "r", encoding="utf8") as f:
            data = json.load(f)
    except FileNotFoundError:
        # Si el archivo no existe, inicializa la estructura
        data = {tipo: []}
    except json.JSONDecodeError:
        # Si el archivo existe pero está vacío o corrupto
        data = {tipo: []}

    # 2. Modificar los datos
    data[tipo].append(contenido.to_dict())

    # 3. Sobrescribir el archivo con los datos actualizados
    with open(path, "w", encoding="utf8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    return True


def eliminar_contenido(tipo, contenido_id, path):
    path = _obtener_path(tipo)
    # 1. Leer los datos existentes
    try:
        with open(path, "r", encoding="utf8") as f:
            data = json.load(f)
    except FileNotFoundError:
        return False  # Archivo no existe
    except json.JSONDecodeError:
        return False  # Archivo corrupto
    # 2. Modificar los datos
    items = data.get(tipo, [])
    contenido = [item for item in items if item["id"] != contenido_id]
    data[tipo] = contenido
    # 3. Sobrescribir el archivo con los datos actualizados
    with open(path, "w", encoding="utf8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    return True
