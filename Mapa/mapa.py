import folium

def crear_mapa_interactivo(latitud_centro, longitud_centro, marcadores, path):
    # Crea el mapa con el centro en la ubicación dada
    mapa = folium.Map(location=[latitud_centro, longitud_centro], zoom_start=15)

    # Agrega los marcadores al mapa
    for lat, lon, titulo in marcadores:
        contenido_popup = f'<p style="font-size:16px; font-weight:bold; display: flex; text-align: center; padding: 20px; width: 229px;">{titulo}</p>' 
        popup = folium.Popup(contenido_popup)
        marcador = folium.Marker(location=[lat, lon], popup=popup)
        marcador.add_to(mapa)

    # Trazar la ruta entre los marcadores 1 y 2 (si hay al menos 2 marcadores)
    if len(marcadores) >= 2:

        coordenadas_ruta = []
        for node in path:
           coordenadas_ruta.append([node.lat, node.lon])  

        trazado = folium.PolyLine(locations=coordenadas_ruta, color='red', weight=2)
        trazado.add_to(mapa)

    # Devuelve el mapa
    return mapa

def create_map(start, end, path):

    # Coordenadas del centro del mapa
    latitud_centro = 18.53103035006833
    longitud_centro = -69.90652084350587

    # Lista de marcadores con sus coordenadas y títulos
    marcadores = [
        [start.lat, start.lon, f"Node_id: {start.id}\nLatitud: {start.lat}\nLongitud: {start.lon}"],
        [end.lat, end.lon, f"Node_id: {end.id}\nLatitud: {end.lat}\nLongitud: {end.lon}"],
    ]

    # Crea el mapa interactivo con los dos marcadores y traza la ruta entre ellos
    mapa = crear_mapa_interactivo(latitud_centro, longitud_centro, marcadores , path)

    # Guarda el mapa interactivo como un archivo HTML
    mapa.save("Mapa/Ruta.html")