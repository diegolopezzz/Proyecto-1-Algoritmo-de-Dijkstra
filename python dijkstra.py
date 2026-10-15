import heapq

class Nodo:
    def __init__(self, nombre):
        self.nombre = nombre
        # Diccionario para guardar las conexiones: {nodo_destino: peso}
        self.conexiones = {}

    def agregar_conexion(self, nodo_vecino, peso):
        self.conexiones[nodo_vecino] = peso

    # Método mágico necesario para que la cola de prioridad (heapq) pueda desempatar
    def __lt__(self, otro):
        return self.nombre < otro.nombre


class Grafo:
    def __init__(self):
        self.nodos = {} # Diccionario para almacenar todos los nodos por su nombre

    def agregar_nodo(self, nombre_nodo):
        if nombre_nodo not in self.nodos:
            self.nodos[nombre_nodo] = Nodo(nombre_nodo)

    def agregar_arista(self, origen, destino, peso, bidireccional=True):
        # Asegurarnos de que los nodos existan
        self.agregar_nodo(origen)
        self.agregar_nodo(destino)
        
        # Conectar origen con destino
        self.nodos[origen].agregar_conexion(self.nodos[destino], peso)
        
        # Si es un grafo no dirigido (bidireccional), conectar también de vuelta
        if bidireccional:
            self.nodos[destino].agregar_conexion(self.nodos[origen], peso)

    def calcular_dijkstra(self, inicio_nombre, fin_nombre):
        # Verificar que los nodos existan en el grafo
        if inicio_nombre not in self.nodos or fin_nombre not in self.nodos:
            return float('inf'), []

        # Inicializar las distancias hacia todos los nodos como "infinito"
        distancias = {nombre: float('inf') for nombre in self.nodos}
        distancias[inicio_nombre] = 0 # La distancia al nodo de origen es 0

        # Diccionario para reconstruir el camino exacto
        nodos_previos = {nombre: None for nombre in self.nodos}

        # Cola de prioridad: almacena tuplas (distancia_acumulada, nodo_actual)
        cola_prioridad = [(0, self.nodos[inicio_nombre])]

        while cola_prioridad:
            distancia_actual, nodo_actual = heapq.heappop(cola_prioridad)

            # Si ya llegamos al destino, podemos detener el cálculo para ahorrar tiempo
            if nodo_actual.nombre == fin_nombre:
                break

            # Si encontramos en la cola un camino viejo más largo, lo ignoramos
            if distancia_actual > distancias[nodo_actual.nombre]:
                continue

            # Analizar a los vecinos del nodo actual
            for vecino, peso in nodo_actual.conexiones.items():
                nueva_distancia = distancia_actual + peso

                # Si encontramos un camino más corto hacia este vecino, actualizamos
                if nueva_distancia < distancias[vecino.nombre]:
                    distancias[vecino.nombre] = nueva_distancia
                    nodos_previos[vecino.nombre] = nodo_actual.nombre
                    # Añadir el vecino a la cola de prioridad para explorarlo después
                    heapq.heappush(cola_prioridad, (nueva_distancia, vecino))

        # Reconstruir la ruta exacta yendo hacia atrás desde el destino
        ruta = []
        actual = fin_nombre
        while actual is not None:
            ruta.append(actual)
            actual = nodos_previos[actual]
        ruta.reverse() # Invertir la lista para que vaya de Inicio -> Fin

        # Validar si efectivamente se encontró una ruta
        if ruta[0] == inicio_nombre:
            return distancias[fin_nombre], ruta
        else:
            return float('inf'), [] # No hay conexión posible

# ==========================================
# Paso 3: Prueba de Ejecución (Resultados)
# ==========================================
if __name__ == "__main__":
    red = Grafo()

    # Creando una red de transporte de ejemplo
    red.agregar_arista("A", "B", 4)
    red.agregar_arista("A", "C", 2)
    red.agregar_arista("B", "C", 1)
    red.agregar_arista("B", "D", 5)
    red.agregar_arista("C", "D", 8)
    red.agregar_arista("C", "E", 10)
    red.agregar_arista("D", "E", 2)
    red.agregar_arista("D", "F", 6)
    red.agregar_arista("E", "F", 3)

    origen = "A"
    destino = "F"

    costo_total, ruta_optima = red.calcular_dijkstra(origen, destino)

    print("=== Resultados del Algoritmo de Dijkstra ===")
    print(f"Origen: {origen} | Destino: {destino}")
    
    if ruta_optima:
        print(f"Costo / Distancia mínima: {costo_total}")
        print(f"Ruta exacta: {' -> '.join(ruta_optima)}")
    else:
        print("No se encontró una ruta posible entre los nodos indicados.")
        