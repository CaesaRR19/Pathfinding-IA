import copy
def h_Manhattan(status, end):
    scale=100
    distance = abs(end.lon - status.lon) * scale + abs(end.lat - status.lat) * scale
    return distance

def h_surface(surface):
    type={ 
        True : 0,
        False : 0.0005}
    value= type[surface]
    return value

def heuristic(surface, status, end):
    if surface == None:
        h_total = h_Manhattan(status, end)
    else:
        h_total = h_Manhattan(status, end) + h_surface(surface)
    return h_total

def final_path(node):
    path = []

    # Se recorren los padres de cada uno de los nodos hasta el inicio
    while node.parent is not None:
        path.append(node)
        node = node.parent
    path.append(node)
    path.reverse()
    return path


def A_star(graph, start, end):
    
    #Se declaran las listas abierta (Frontera) y cerrada (Explorados)
    frontier = []
    explored = []
    
    #Se inicializan los extremos (inicio y fin) de la ruta
    start.g = 0
    start.h = heuristic(None, start, end)
    start.f_cost = start.g + start.h

    end.g = float('inf')
    end.h = 0
    end.f_cost = end.g + end.h

    #Se agrega el inicio a la frontera
    frontier.append(start)

    while frontier:
        #Se busca el nodo con menor función de costo
        state= min(frontier, key=lambda node: node.f_cost)

        #Se toma el nodo de la lista de prioridad
        frontier.remove(state)

        #Se buscan los vecinos del nodo
        successors = graph.get_neighbors(state)
        for successor, edge_weight, surface in successors:

            #Se calcula la función del costo del nodo
            successor.g = state.g + edge_weight
            successor.h = heuristic(surface, successor, end)
            successor.f_cost = successor.g + successor.h

            # Crear una copia del sucesor antes de modificar su padre
            successor_copy = copy.deepcopy(successor)
            successor_copy.parent = state

            #Se comprueba si el sucesor es la meta
            if successor == end:
                return final_path(successor_copy)

            #Se verifica si existe un nodo en la frontera con una función de coste menor al actual y ser asi se omite
            if any(node for node in frontier if node.id == successor.id and node.f_cost < successor.f_cost):
                continue

            #Se verifica si existe un nodo en la lista de explorados con una función de coste menor al actual y ser asi se omite
            if any(node for node in explored if node.id == successor.id and node.f_cost < successor.f_cost):
                continue

            #Se agrega el nodo a la frontera
            frontier.append(successor_copy)

        #Se completa la exploración del nodo y se agrega a explorados
        explored.append(state)
    
    #Si no se encuentra el nodo se notifica
    return "Ruta no encontrada"
