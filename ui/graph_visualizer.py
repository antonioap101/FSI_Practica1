import networkx as nx
import matplotlib.pyplot as plt

from core.search import romania, BidirectionalIterator


class GraphVisualizer:
    def __init__(self, search, graph_data):
        self.search = BidirectionalIterator(search)     # Iterator for the search algorithm
        self.graph_data = graph_data                  # Global data shared among the GUI and visualizer
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

        # Iterate through the nodes and their neighbors in the Romania graph
        for node, neighbours in romania.dict.items():
            for neighbour, distance in neighbours.items():
                self.graph_data.G.add_edge(node, neighbour, weight=distance) # Add an edge to the graph with the node, neighbor, and edge weight

        # Create a figure and axis for the graph with a specified size of (12, 8)
        self.graph_data.fig, self.graph_data.ax = plt.subplots(figsize=(12, 8))

        # We use the original position of the graphs nodes to draw it
        self.graph_data.pos = {node: (x, y) for node, (x, y) in zip(romania.locations.keys(), romania.locations.values())}

        # Once all properties are set, we draw the graph
        self.draw_original_graph()

    def draw_original_graph(self):
        """Draws the whole graph with all its nodes in blue."""
        self.graph_data.ax.clear()  # Limpia el gráfico actual

        # Draw the graph nodes
        nx.draw(self.graph_data.G, self.graph_data.pos, with_labels=True,
                node_size=1000, node_color='#00A9FF', font_size=10)

        # Draw the graph labels
        edge_labels = nx.get_edge_attributes(self.graph_data.G, 'weight')
        nx.draw_networkx_edge_labels(self.graph_data.G, self.graph_data.pos,
                                     edge_labels=edge_labels, font_size=8)
        plt.axis('off')

        # Update figure and graph
        self.graph_data.fig.canvas.draw()
        self.graph_data.fig.canvas.flush_events()

    def update_graph(self):
        # Prints the current status of every element
        # self.print_status()

        # Colors each visited and visible node
        if self.path:
            current_node = self.path[0].state # Agrega el nodo actual a los visitados

            self.graph_data.ax.clear()  # Clears drawing status to update it

            # Draw non-changed nodes
            nx.draw(self.graph_data.G, self.graph_data.pos , with_labels=True, node_size=1000, node_color='#00A9FF', font_size=10)

            # Paint visible nodes
            nx.draw(self.graph_data.G, self.graph_data.pos, with_labels=True, nodelist=list(n.state for n in self.fringe), node_size=1100,
                    node_color='#FFD600', font_size=10)

            # Paint visited nodes
            nx.draw(self.graph_data.G, self.graph_data.pos, with_labels=True, nodelist=list(self.closed), node_size=1000,
                    node_color='#A9FF00', font_size=10)

            edge_labels = nx.get_edge_attributes(self.graph_data.G, 'weight')

            nx.draw_networkx_edge_labels(self.graph_data.G, self.graph_data.pos, edge_labels=edge_labels, font_size=8)

            # We check that the current node has assigned coordinates in the graph
            if current_node in self.graph_data.pos:
                nx.draw_networkx_nodes(self.graph_data.G, self.graph_data.pos, nodelist=[current_node], node_color='#FF00A9', node_size=700)

            self.graph_data.fig.canvas.flush_events()
        # You could program the next update in a specific time-lapse, the update in this case is manual with forward-backward buttons
        # root.after(250, self.update_graph)  # 250 milliseconds between updates (not used)

    def handle_search_completion(self):
        # Print the final path
        print("Search completed -> Final path: ", self.last_path)

        # Paint all nodes of the resulting path in black
        final_path_nodes = [node.state for node in self.last_path]
        nx.draw_networkx_nodes(self.graph_data.G, self.graph_data.pos, nodelist=final_path_nodes, node_color='black', node_size=1300)

        # Set the label text white for every black node
        nx.draw_networkx_labels(self.graph_data.G, self.graph_data.pos, labels={n: n for n in final_path_nodes}, font_color='white', font_size=10)

    def advance_graph(self):
        try:
            self.generated, self.visited, self.path_cost, self.path, self.closed, self.fringe = self.search.next()
            self.position += 1
            self.last_path = self.path.copy()
            self.update_graph()
        except StopIteration:
            self.handle_search_completion()

        return self.generated, self.visited, self.path_cost, self.path, self.closed, self.fringe, self.position

    def reverse_graph(self):
        try:
            self.generated, self.visited, self.path_cost, self.path, self.closed, self.fringe = self.search.prev()
            self.position -= 1
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
