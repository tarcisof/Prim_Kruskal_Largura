import heapq
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def ler_matrizes_de_arquivo(nome_arquivo):
    with open(nome_arquivo, 'r') as arquivo:
        matrizes = []
        matriz_atual = []
        for linha in arquivo:
            linha = linha.strip()
            if linha == "":
                if matriz_atual:
                    matrizes.append(np.array(matriz_atual, dtype=int))
                    matriz_atual = []
            else:
                matriz_atual.append(list(map(int, linha.split())))
        if matriz_atual:
            matrizes.append(np.array(matriz_atual, dtype=int))
    return matrizes

def prim(matriz, vertice_inicial):
    n = len(matriz)
    if n == 0:
        return [], 0

    mst = []
    visitados = set()  # Conjunto para acompanhar os vértices visitados.
    arestas = []  # Heap (fila de prioridade) para armazenar as arestas candidatas.
    peso_total = 0

    def adicionar_arestas(vertice):
        nonlocal peso_total
        visitados.add(vertice)  # Marca o vértice como visitado.
        for i in range(n):
            peso = matriz[vertice][i]  #
            if peso != 0 and i not in visitados:  # Se a aresta existe e o vértice 'i' não foi visitado.
                heapq.heappush(arestas, (peso, vertice, i))  # Adiciona a aresta ao heap com (peso, vértice inicial, vértice adjacente).

    adicionar_arestas(vertice_inicial)  # Adiciona as arestas do vértice inicial ao heap.

    while arestas and len(visitados) < n:
        peso, vertice, adjacente = heapq.heappop(arestas)  # Extrai a aresta de menor peso do heap.
        if adjacente not in visitados:  # Se o vértice adjacente não foi visitado.
            mst.append((vertice + 1, adjacente + 1, peso))  # Adiciona a aresta à MST (ajusta os índices para começar de 1).
            peso_total += peso
            adicionar_arestas(adjacente)

    return mst, peso_total

def plotar_grafo(matriz, titulo):
    G = nx.from_numpy_array(matriz)
    pos = nx.spring_layout(G)
    edge_labels = {(i, j): matriz[i][j] for i in range(matriz.shape[0]) for j in range(matriz.shape[1]) if
                   matriz[i][j] != 0}

    nx.draw(G, pos, with_labels=True, labels={n: n + 1 for n in G.nodes()}, node_color='lightblue',
            edge_color='gray', node_size=500, font_size=12)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title("Grafo gerado a partir da matriz de adjacência")
    plt.show()

def plotar_mst(mst):
    G = nx.Graph()
    for aresta in mst:
        G.add_edge(aresta[0], aresta[1], weight=aresta[2])

    pos = nx.spring_layout(G)
    plt.figure(figsize=(8, 6))

    nx.draw(G, pos, with_labels=True, node_color='green', node_size=700, edge_color='gray', linewidths=1, font_size=15)
    edge_labels = {(aresta[0], aresta[1]): aresta[2] for aresta in mst}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.title("Árvore Geradora Mínima (MST) - Algoritmo de Prim")
    plt.show()

def main():
    nome_arquivo = "grafo.txt"
    matrizes = ler_matrizes_de_arquivo(nome_arquivo)

    print("Selecione a matriz de adjacência (1 a {}):".format(len(matrizes)))
    for i, matriz in enumerate(matrizes, 1):
        print(f"Matriz {i}:\n{matriz}")

    escolha_matriz = int(input("Escolha a matriz: ")) - 1
    matriz_adjacencia = matrizes[escolha_matriz]

    plotar_grafo(matriz_adjacencia, "Grafo Original")

    vertices = list(range(1, len(matriz_adjacencia) + 1))
    print(f"Vértices disponíveis: {vertices}")
    vertice_inicial = int(input("Escolha o vértice inicial: "))

    if vertice_inicial not in vertices:
        print("Vértice inválido. Usando o vértice 1 como padrão.")
        vertice_inicial = 1

    mst, peso_total = prim(matriz_adjacencia, vertice_inicial - 1)  # Ajustar índice para começar de 0
    print("Árvore Geradora Mínima (MST) pelo algoritmo de Prim:")
    for aresta in mst:
        print(f"{aresta[0]} - {aresta[1]} (Peso: {aresta[2]})")

    print(f"Peso total da Árvore Geradora Mínima (MST): {peso_total}")

    plotar_mst(mst)

if __name__ == "__main__":
    main()
