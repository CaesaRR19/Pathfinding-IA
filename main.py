import webbrowser 
from Mapa.mapa import *
from Grafo.Algoritmo import *
from Grafo.EstructuraGrafo import *

graph = create_graph('JSON\dataVM.json')

start = int(input('Ingrese el id del nodo de inicio: '))
end = int(input('Ingrese el id del nodo de destino: '))

try:
    start = graph.nodes[start]
    end = graph.nodes[end]

    solution_path = A_star(graph, start, end)

    if isinstance(solution_path, list):
        create_map(start, end, solution_path)
        file_path = r"file:///C:/Users/Jesus%20D.%20Rodriguez/Desktop/pruebamapaia/Mapa/Ruta.html"
        webbrowser.register('chrome', None, webbrowser.BackgroundBrowser("C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"))
        webbrowser.get('chrome').open(file_path)  
    else:
        print(solution_path)

except:
    print('Alguno de los nodos no se encuentra en el grafo') 
