import geopandas as gpd
import pandas as pd
import numpy as np

class Grafo():
    def __init__(self, path, tipo):
        self.naturalEarth = gpd.read_file(path)
        self.mapa = self.naturalEarth[["NAME",tipo,"POP_EST",'geometry']]
        self.geometria = self.mapa.geometry
        self.vertices = self.mapa.NAME
        self.grafoMatriz = []
        self.grafoDataFrame = None
        self.vertices_cores = np.zeros(len(self.vertices), dtype=int)
    
    def criarGrafoMatriz(self):
        for linha in self.vertices:
            auxGrafo = []
            v = self.vertices[self.vertices == linha].index.values[0]
            regiaolinha = self.geometria[v]

            for coluna in self.vertices:
                u = self.vertices[self.vertices  == coluna].index.values[0]
                regiaocoluna = self.geometria[u]

                if regiaolinha.intersects(regiaocoluna):
                    auxGrafo.append(1)
                else:
                    auxGrafo.append(0)
            self.grafoMatriz.append(auxGrafo)

        self.grafoDataFrame = pd.DataFrame(data=self.grafoMatriz, index=self.vertices, columns=self.vertices)

    def colorirGrafo(self):
        # Percorre todos os vértices do grafo
        for vertex in range(len(self.vertices)):
            # Obtém as cores dos vértices adjacentes
            adjacent_colors = set(self.vertices_cores[adjacente] for adjacente in range(len(self.vertices)) if self.grafoMatriz[vertex][adjacente])

            # Encontra a cor disponível não utilizada pelos vértices adjacentes
            color = 1
            while color in adjacent_colors:
                color += 1

            # Atribui a cor encontrada ao vértice atual
            self.vertices_cores[vertex] = color
        
        self.mapa['colors'] = self.vertices_cores



