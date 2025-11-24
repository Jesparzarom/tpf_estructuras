from .contenidos import Pila, Cola, obtener_pesos_aristas

# --- Grafo para recomendaciones y topológico ---
class GrafoContenido:
    def __init__(self):
        """Inicializa un grafo vacío para el catálogo de contenidos, por tipo de contenido:
        Grafo de Peliculas, Grafo de Documentales o Grafo de Series.
        """
        
        # Vertices del grado
        self.vertices_contenido = {}
        # Grafo ponderado para Similares (BFS)
        self.adyacencia_similitud = {} 
        # Grafo ponderado para Maratón (DFS)
        self.adyacencia_maraton = {} 
        # Grafo no ponderado para Orden Topológico
        self.adyacencia_orden_sagas = {}

    def agregar(self, contenido):
        """Agrega un contenido al grafo, inicializando sus listas de adyacencia.
        Args:
            contenido (ContenidoBase): El contenido a agregar al grafo.
        """
        self.vertices_contenido[contenido.id] = contenido
        self.adyacencia_similitud[contenido.id] = []
        self.adyacencia_maraton[contenido.id] = []
        self.adyacencia_orden_sagas[contenido.id] = []



    def ver_vertices(self):
        """Retorna una lista de los IDs de los contenidos en el grafo."""
        return list(self.vertices_contenido.keys())

    def ver_adyacencia_similitud(self):
        """Retorna la lista de contenidos similares a un nodo dado.
        Args:
            nodo_id (str): El ID del contenido.
        Returns:
            list: Lista de IDs de contenidos similares.
        """
        #print("[SIMILITUD]", self.adyacencia_similitud) para debug
        #print("[MARATON]", self.adyacencia_maraton) para debug
        #print("[VERTICES]", self.vertices_contenido) para debug

    def ver_adyacencia_orden(self, nodo_id):
        """Retorna la lista de contenidos en orden a partir de un nodo dado.
        Args:
            nodo_id (str): El ID del contenido.
        Returns:
            list: Lista de IDs de contenidos en orden.
        """
        return self.adyacencia_orden_sagas.get(nodo_id, [])

    def generar_similitud(self, umbral=4, tipo=None):
        """Genera aristas de similitud usando el peso ponderado para recomendaciones."""

        ids = list(self.vertices_contenido.keys())

        for i in range(len(ids)):
            for j in range(i + 1, len(ids)):
                a, b = self.vertices_contenido[ids[i]], self.vertices_contenido[ids[j]]
                
                # CALCULAR AMBOS SCORES
                score_similares = obtener_pesos_aristas(a, b, tipo, "similares")
                score_maraton = obtener_pesos_aristas(a, b, tipo, "maraton")
                
                if score_similares >= umbral and a.id != b.id:
                    # Almacenar en el grafo de Similitud
                    self.adyacencia_similitud[a.id].append((b.id, score_similares))
                    self.adyacencia_similitud[b.id].append((a.id, score_similares))
                
                # Usar un umbral (quizás el mismo) para el grafo de maratón
                if score_maraton >= umbral and a.id != b.id:
                    # Almacenar en el grafo de Maratón
                    self.adyacencia_maraton[a.id].append((b.id, score_maraton))
                    self.adyacencia_maraton[b.id].append((a.id, score_maraton))

    def generar_orden(self):
        """Genera las aristas de orden entre los contenidos del grafo
        basándose en las secuelas indicadas en cada contenido.
        Cada contenido apunta a sus secuelas en la lista de adyacencia de orden.
        """
        for c in self.vertices_contenido.values():  # Iterar sobre cada contenido
            for sec in c.ids_secuelas:  # Iterar sobre sus secuelas
                if sec in self.vertices_contenido:  # Verificar que la secuela exista en el grafo
                    self.adyacencia_orden_sagas[c.id].append(sec)  # Agregar arista de orden

    def construir_desde_contenidos(self, contenidos, tipo: str = None):
        """
        Conveniencia: construye el grafo a partir de una lista de contenidos.
        `contenidos` puede ser una lista de objetos TDA (recomendado) o
        una lista de diccionarios tal como salen del JSON. Si son diccionarios,
        es necesario pasar `tipo` ('peliculas'|'documentales'|'series') para
        convertirlos al TDA correspondiente usando el método `from_dict`.
        """
        # Import dinámico para evitar importaciones circulares en el módulo
        if tipo is not None:
            from .contenidos.pelicula import Pelicula as _Pelicula
            from .contenidos.documental import Documental as _Documental
            from .contenidos.serie import Serie as _Serie
            mapper = {
                "peliculas": _Pelicula,
                "documentales": _Documental,
                "series": _Serie,
            }

        for item in contenidos:
            if isinstance(item, dict):
                if tipo is None:
                    # No sabemos cómo convertir el dict sin el tipo
                    continue
                cls = mapper.get(tipo)
                if not cls:
                    continue
                try:
                    obj = cls.from_dict(dict(item))
                except Exception:
                    # Si falla la conversión, saltar ese elemento
                    continue
                self.agregar(obj)
            else:
                # Asumimos que item ya es un objeto con atributo `id`
                self.agregar(item)

    def dfs_autoplay(self, start_id):
        """
        implementacion de DFS para `autoplay`.
        toma el id de un contenido puntual
        - **retorna** un recorrido en profundidad basado en similitud de contenidos,
        priorizando aquellos con mayor score de similitud.

        Args:
            start_id (str): id del contenido inicial
        """
        # lista de nodos visitados en orden
        visitados = []

        # Pila para DFS
        pila = Pila()
        pila.apilar(start_id)

        # DFS iterativo
        while not pila.esta_vacia():  # Mientras haya nodos por visitar
            nodo_id = pila.desapilar()  # Obtener el nodo superior de la pila

            if nodo_id not in visitados:  # Si no ha sido visitado
                visitados.append(nodo_id)  # Marcar como visitado
                vecinos = self.adyacencia_similitud.get(nodo_id, [])  # Obtener vecinos

                # ordenar vecinos por score descendente
                vecinos_ordenados = sorted(
                    vecinos,
                    # ordenar por el índice 1, que es el score.
                    key=lambda v: v[1], 
                    reverse=True,
                )

                # agregamos al stack en orden inverso para mantener score descendente
                for vecino_tuple in reversed(vecinos_ordenados):
                    vecino_id = vecino_tuple[0] # Extraemos el ID del índice 0
                    if vecino_id not in visitados:  # Si el vecino no ha sido visitado
                        pila.apilar(vecino_id)  # Apilar el vecino para visitar luego

        return visitados[:7]

    def bfs_ver_similar(self, start_id):
        """
        implementacion de BFS para `ver contenido similar`.
        toma el id de un contenido puntual.
        - **retorna** un recorrido en anchura basado en similitud de contenidos,
        priorizando aquellos con mayor score de similitud.

        Args:
            start_id (str): id del contenido inicial
        """
        # lista de nodos visitados en orden
        visitados = []

        # Cola para BFS
        cola = Cola()
        cola.encolar(start_id)

        # Iteración sobre la cola
        while not cola.esta_vacia():  # Mientras haya nodos por visitar
            nodo_id = cola.desencolar()  # Obtener el nodo frontal de la cola

            if nodo_id not in visitados:  # Si no ha sido visitado
                visitados.append(nodo_id)  # Marcar como visitado
                vecinos = self.adyacencia_maraton.get(nodo_id, [])  # Obtener vecinos

                # ordenar vecinos por score descendente
                vecinos_ordenados = sorted(
                    vecinos,
                    # ¡CAMBIO CLAVE! 'v' YA NO ES UN ID. 'v' es la tupla (ID, score).
                    # Debes ordenar por el índice 1, que es el score.
                    key=lambda v: v[1], 
                    reverse=True,
                )

                for vecino_tuple in vecinos_ordenados:  # Iterar sobre vecinos
                    # Si el vecino no ha sido visitado ni está en la cola
                    vecino_id = vecino_tuple[0]
                    if vecino_id not in visitados and vecino_id not in cola:
                        cola.encolar(vecino_id)  # Encolar el vecino para visitar luego

        return visitados[:7]

    def generar_topologico(self, start_id=None):
        """Genera un orden topológico de contenidos puntuales en el grafo
        toma el id de un contenido puntual (opcional). Sirve para buscar sagas enteras en orden.
        Si no se provee un id, se genera el orden topológico para todo el grafo.
        - **retorna** una lista con el orden topológico de los contenidos.

        Args:
            start_id (str, optional): id del contenido inicial. Defaults to None.
        """
        visitados = set()
        orden = []

        def dfs_topo(nodo):
            if nodo in visitados:
                return
            visitados.add(nodo)
            for vecino in self.adyacencia_orden_sagas.get(nodo, []):
                dfs_topo(vecino)
            orden.append(nodo)

        if start_id:
            dfs_topo(start_id)
            return orden[::-1]
        for nodo in self.vertices_contenido:
            if nodo not in visitados:
                dfs_topo(nodo)
        return orden[::-1]
