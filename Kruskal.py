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

def kruskal(matriz):
    def encontrar_pai(parent, i):
        if parent[i] != i:
            parent[i] = encontrar_pai(parent, parent[i])
        return parent[i]

    def unir_conjuntos(parent, rank, x, y):
        if rank[x] < rank[y]:
            parent[x] = y
        elif rank[x] > rank[y]:
            parent[y] = x
        else:
            parent[y] = x
            rank[x] += 1

    arestas = []
    n = len(matriz)
    for i in range(n):
        for j in range(i + 1, n):
            if matriz[i][j] != 0:
                arestas.append((matriz[i][j], i, j))

    arestas = sorted(arestas, key=lambda item: item[0])
    parent = list(range(n))
    rank = [0] * n
    mst = []

    for peso, u, v in arestas:
        x = encontrar_pai(parent, u)
        y = encontrar_pai(parent, v)
        if x != y:
            mst.append((u + 1, v + 1, peso))  # Ajusta índices para começar de 1
            unir_conjuntos(parent, rank, x, y)
            # Mostrar os conjuntos após unir
            conjuntos = {i: [] for i in range(n)}
            for i in range(n):
                conjuntos[encontrar_pai(parent, i)].append(i + 1)
            conjuntos = {k: v for k, v in conjuntos.items() if v}
            print(f"Conjuntos após unir {u + 1} e {v + 1}: {conjuntos}")

    return mst


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

    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=700, edge_color='gray', linewidths=1, font_size=15)
    edge_labels = {(aresta[0], aresta[1]): aresta[2] for aresta in mst}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.title("Árvore Geradora Mínima (MST) - Algoritmo de Kruskal")
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

    mst = kruskal(matriz_adjacencia)
    print("Árvore Geradora Mínima (MST) pelo algoritmo de Kruskal:")
    peso_total = 0
    for aresta in mst:
        print(f"{aresta[0]} - {aresta[1]} (Peso: {aresta[2]})")
        peso_total += aresta[2]

    print(f"Peso total de Kruskal: {peso_total}")
    plotar_mst(mst)

if __name__ == "__main__":
    main()
