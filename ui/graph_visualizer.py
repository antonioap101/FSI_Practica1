import networkx as nx
import matplotlib.pyplot as plt

from core.search import romania, BidirectionalIterator


class GraphVisualizer:
    def __init__(self, search, global_data):
        self.search = BidirectionalIterator(search)     # Iterator for the search algorithm
        self.global_data = global_data                  # Global data shared among the GUI and visualizer
        self.position = 0                               # Current position or step in the visualization
        self.last_path = None                           # Stores the last path for comparison

        self.generated = None           # Number of generated nodes during the search
        self.visited = None             # Number of visited nodes during the search
        self.path = None                # Current path being explored
        self.path_cost = None           # Cost of the current path
        self.closed = None              # Set of closed (visited) nodes
        self.fringe = None              # Fringe or frontier nodes in the search

    def draw_fixed_graph(self):
        """ Method to draw the graph with fixed position for its nodes """
        self.graph_data.G = nx.Graph()

        # Usamos las claves originales para los nodos, sin usar node_labels para convertirlos
        for node, neighbours in romania.dict.items():
            for neighbour, distance in neighbours.items():
                self.graph_data.G.add_edge(node, neighbour, weight=distance)

        # Dibujar el grafo
        self.graph_data.fig, self.graph_data.ax = plt.subplots(figsize=(12, 8))

        # Usamos las posiciones originales sin la conversión de las claves
        self.graph_data.pos = {node: (x, y) for node, (x, y) in zip(romania.locations.keys(), romania.locations.values())}

        nx.draw(self.graph_data.G, self.graph_data.pos, with_labels=True, node_size=1000, node_color='#00A9FF', font_size=10)

        # Dibujar las etiquetas de los pesos en las aristas
        edge_labels = nx.get_edge_attributes(self.graph_data.G, 'weight')
        nx.draw_networkx_edge_labels(self.graph_data.G, self.graph_data.pos, edge_labels=edge_labels, font_size=8)

        plt.axis('off')

    def update_graph(self):
        # Imprime por pantalla el estado actual de los elementos
        # self.print_status()

        # Colorea el nodo actualmente visitado
        if self.path:
            current_node = self.path[0].state # Agrega el nodo actual a los visitados

            self.graph_data.ax.clear()  # Redibuja el grafo para reflejar los nodos visitados
            # Dibujamos los nodos visibles
            nx.draw(self.graph_data.G, self.graph_data.pos , with_labels=True, node_size=1000, node_color='#00A9FF', font_size=10)

            nx.draw(self.graph_data.G, self.graph_data.pos, with_labels=True, nodelist=list(n.state for n in self.fringe), node_size=1100,
                    node_color='#FFD600', font_size=10)

            # Dibujamos los nodos visitados
            nx.draw(self.graph_data.G, self.graph_data.pos, with_labels=True, nodelist=list(self.closed), node_size=1000,
                    node_color='#A9FF00', font_size=10)

            edge_labels = nx.get_edge_attributes(self.graph_data.G, 'weight')

            nx.draw_networkx_edge_labels(self.graph_data.G, self.graph_data.pos, edge_labels=edge_labels, font_size=8)
            # Asegúrate de que el nodo actual está en el grafo antes de intentar colorearlo
            if current_node in self.graph_data.pos:
                nx.draw_networkx_nodes(self.graph_data.G, self.graph_data.pos, nodelist=[current_node], node_color='#FF00A9', node_size=700)

            self.graph_data.fig.canvas.flush_events()
        # Programa la siguiente actualización
        # root.after(250, self.update_graph)  # 500 milisegundos entre actualizaciones

    def handle_search_completion(self):
        # status_label.config(text="Search completed.")
        print("Search completed")
        # Dibujamos el camino
        print("LAST: ", self.last_path)

        final_path_nodes = [node.state for node in self.last_path]
        nx.draw_networkx_nodes(self.graph_data.G, self.graph_data.pos, nodelist=final_path_nodes, node_color='black', node_size=1300)

        # Dibujar las etiquetas de los nodos del camino en blanco
        nx.draw_networkx_labels(self.graph_data.G, self.graph_data.pos, labels={n: n for n in final_path_nodes}, font_color='white', font_size=10)


    def advance_graph(self):
        try:
            self.generated, self.visited, self.path_cost, self.path, self.closed, self.fringe = self.search.next()
            self.position += 1 # Almacenamos la posicion del iterador
            self.last_path = self.path.copy()
            self.update_graph()
        except StopIteration:
            self.handle_search_completion()

        return self.generated, self.visited, self.path_cost, self.path, self.closed, self.fringe, self.position

    def reverse_graph(self):
        try:
            self.generated, self.visited, self.path_cost, self.path, self.closed, self.fringe = self.search.prev()
            self.position -= 1  # Almacenamos la posicion del iterador
            self.last_path = self.path.copy()
            self.update_graph()
        except IndexError:
            pass

        return self.generated, self.visited, self.path_cost, self.path, self.closed, self.fringe, self.position

    def print_status(self):
        print("-------------------------------")
        print(f"Generated: {self.generated}")
        print(f"Visited: {self.visited}")
        print(f"Path Cost: {self.path_cost}")
        print(f"Path: {self.path}")
        print(f"Closed: {self.closed}")
        print(f"Fringe: {self.fringe}")
        print(f"STATE:  {self.path[0].state}")
        print("-------------------------------")
