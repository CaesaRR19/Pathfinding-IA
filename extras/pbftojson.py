import osmium
import json
from heuristicas import haversine

class OSMHandler(osmium.SimpleHandler):
    def __init__(self):
        osmium.SimpleHandler.__init__(self)
        self.nodes = []
        self.ways = []

    def node(self, n):
        self.nodes.append({
            'id': n.id,
            'lat': n.location.lat,
            'lon': n.location.lon
        })

    def way(self, w):
        nodos_refs = [n.ref for n in w.nodes]

        tags_to_avoid = ['building', 'amenity', 'building', 'shop', 'landuse']
        avoid_way = any(tag in w.tags for tag in tags_to_avoid)
        if avoid_way:
            return
    
        weight = {}
        for node_ref in nodos_refs:
            weight[node_ref] = {}
        for i in range(len(nodos_refs) - 1):
            n1 = [n for n in self.nodes if n['id'] == nodos_refs[i]][0]
            n2 = [n for n in self.nodes if n['id'] == nodos_refs[i + 1]][0]
            distancia = haversine(float(n1['lat']), float(n1['lon']), float(n2['lat']), float(n2['lon']))
            weight[nodos_refs[i]][nodos_refs[i + 1]] = distancia
            
        superficie = 'asphalt' in w.tags.get('surface', '').lower()
        direccion = 'oneway' in w.tags.get('oneway', '').lower() and w.tags['oneway'] == 'yes'

        self.ways.append({
            'id': w.id,
            'nodos': nodos_refs,
            'arista': weight,
            'superficie': superficie,
            'direccion': direccion
        })

handler = OSMHandler()
handler.apply_file("hermanas_mirabal.pbf")

data = {
    'nodos': handler.nodes,
    'vias': handler.ways
}

with open('dataHM.json', 'w') as f:
    json.dump(data, f)

