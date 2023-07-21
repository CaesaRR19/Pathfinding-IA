import json
#Se define el graph
class Directed_Graph:
    def __init__(self) :
        self.nodes = {}
        self.ways = []

    def add_node(self, node):
        self.nodes[node.id] = node

    def add_way(self, way):
        self.ways.append(way)

    def get_neighbors(self, node):
        if node is None:
            raise ValueError("El nodo no existe en el grafo.")
        neighbors = []

        #Se buscan las vias 
        for way in self.ways:

            #Se comprueba que el nodo exista en la via
            if node.id in [n.id for n in way.nodes]:
                edges=way.get_edges()

                #Se buscan todas las aristas de las vias
                for way_edge in edges:
                    fnode = way_edge.get_fnode()

                    #Se comprueba que el nodo no sea un valor nulo y sea igual al identificador de alguna de las aristas
                    if fnode is not None and fnode.get_id()== node.id:
                        neighbor = way_edge.get_lnode()

                        #Se comprueba que el nodo resultante (vecino) no sea un valor nulo, que sea diferente al nodo inicial
                        # y aun no se haya introducido a la lista de vecinos
                        if neighbor is not None and neighbor.get_id() != node.id and neighbor not in neighbors:

                            edge_weight = way_edge.get_weight()
                            surface = way.get_surface()
                            
                            #Se agrupan los objetos del nodo vecino resultante, el peso de la arista que lo contiene 
                            # y la superficie de su via
                            neighbors.append((neighbor, edge_weight, surface))
        return neighbors
    
    def print_graph(self):

        #Se imprimen los nodos
        print("Nodos:")
        for node in self.nodes.values():
            print(f"\tID: {node.id}, Latitud: {node.lat}, Longitud: {node.lon}")

        #Se imprimen las vias
        print("\nVías:")
        for way in self.ways:
            print(f"\tID: {way.id}")

            #Se imprimen los nodos de las vias
            print("\tNodos:")
            for node in way.nodes:
                print(f"\t\tID: {node.id}")

            #Se imprimen las aristas de las vias
            print("\tAristas:")
            for edge in way.edges:
                if edge.lnode is not None and edge.fnode is not None:
                    print(f"\t\tArista de {edge.fnode.id} a {edge.lnode.id}, Peso: {edge.weight}")
            print(f"\tDirección: {way.oneway}")
            print(f"\tSuperficie: {way.surface}")
            print("------------------------------------------------------------------------")


#Se definen las ways
class Way:

    def __init__(self, id, nodes, edges, oneway, surface):
        self.id = id
        self.nodes = nodes
        self.edges = edges
        self.oneway = oneway
        self.surface = surface

    def get_id(self):
        return self.id
    
    def get_oneway(self):
        return self.oneway
    
    def get_surface(self):
        return self.surface
    
    def get_edges(self):
        return self.edges
    
    def get_nodes(self):
        return self.nodes
    
    def get_node(self, node):
        return self.nodes.get(node.id, "No se encontró el nodo")

    def __str__(self):
        return f'{self.id} : Peso {self.weight}, Dirección {self.oneway}, Superficie {self.surface}'
    
#Se definen las aristas
class Edge :
    def __init__(self, fnode, lnode, weight):
        self.fnode = fnode
        self.lnode = lnode
        self.weight = weight

    def get_fnode(self):
        return self.fnode
    
    def get_lnode(self):
        return self.lnode
    
    def get_weight(self):
        return self.weight

#Se definen los nodos
class Node:
    def __init__(self, id, lat, lon):
        self.id = id
        self.lat=lat
        self.lon=lon
        self.g = 0 
        self.h=0
        self.f_cost = 0
        self.parent = None
    
    def get_id(self):
        return self.id

    def get_coordinates(self):
        return {"lat": self.lat, "lng": self.lon}
    
    def __str__(self):
        return self.id

#Creación del grafo
def create_graph(doc):

    #Se extraen los datos del Json
    with open(doc) as file:
        data = json.load(file)

    graph = Directed_Graph()
        
    #Se rellenan los nodos del grafo
    for node_data in data['nodos']:
        node = Node(node_data['id'], node_data['lat'], node_data['lon'])
        graph.add_node(node)
    
    #Se rellenan las vias del grafo
    #Se rellenan los nodos de la via
    for way_data in data['vias']:
        nodes_way = [graph.nodes[node_id] for node_id in way_data['nodos'] if node_id in graph.nodes]

        #Se rellenan las aristas de la via
        edges_way = []

        for fnode_id in way_data['arista']:

            #Se busca el primer nodo de la arista dentro de la via
            fnode = None
            for n in nodes_way:
                if str(n.get_id()) == fnode_id:
                    fnode = n
                    break
            
            #Se busca el segundo nodo de la arista dentro de la via
            # y se agrega el peso de la conexión
            if  len(way_data['arista'][fnode_id]) > 0:
                lnode_id, weight = way_data['arista'][fnode_id].popitem()
            else :
                lnode_id = None
                weight = None

            lnode = None
            for n in nodes_way:
                if str(n.get_id()) == lnode_id:
                    lnode = n
                    break
        
            #Se crean las aristas y determina si la via es de doble o única dirección 
            #Si es de única dirección solo se crean conexiones en un sentido
            if way_data['direccion']:
                edge = Edge(fnode, lnode, weight)
                edges_way.append(edge)

            #Si es de doble dirección en ambos
            else:
                edge = Edge(fnode, lnode, weight)
                edges_way.append(edge)

                edge = Edge(lnode, fnode, weight)
                edges_way.append(edge)
                
        #Creación de la via
        way = Way(way_data['id'], nodes_way, edges_way, way_data['direccion'], way_data['superficie'])
        graph.add_way(way)

    return graph