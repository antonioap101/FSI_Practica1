import tkinter as tk
from tkinter import font

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from problem import GPSProblem
from search import romania, depth_first_graph_search_generator
from utils import Stack

# Utilizando el objeto 'romania' del código proporcionado
edges = [(node, neighbour, romania.dict[node][neighbour]) for node in romania.dict for neighbour in romania.dict[node]]
locations = {node: (x, y) for node, (x, y) in zip(romania.locations.keys(), romania.locations.values())}

# Convierte los nombres de los nodos a los nombres reales basados en la imagen
node_labels = {'A': 'Arad', 'B': 'Bucharest', 'C': 'Craiova', 'D': 'Drobeta', 'E': 'Eforie',
               'F': 'Fagaras', 'G': 'Giurgiu', 'H': 'Hirsova', 'I': 'Iasi', 'L': 'Lugoj',
               'M': 'Mehadia', 'N': 'Neamt', 'O': 'Oradea', 'P': 'Pitesti', 'R': 'Rimnicu Vilcea',
               'S': 'Sibiu', 'T': 'Timisoara', 'U': 'Urziceni', 'V': 'Vaslui', 'Z': 'Zerind'}


# Función para dibujar el grafo fijo como en la imagen
def draw_fixed_graph():
    G = nx.Graph()

    # Usamos las claves originales para los nodos, sin usar node_labels para convertirlos
    for node, neighbours in romania.dict.items():
        for neighbour, distance in neighbours.items():
            G.add_edge(node, neighbour, weight=distance)

    # Dibujar el grafo
    fig, ax = plt.subplots(figsize=(12, 8))
    # Usamos las posiciones originales sin la conversión de las claves
    pos = locations
    nx.draw(G, pos, with_labels=True, node_size=1000, node_color='#00A9FF', font_size=10)

    # Dibujar las etiquetas de los pesos en las aristas
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

    plt.axis('off')
    return fig, ax, G, pos


class UI:
    def __init__(self, search):
        self.visited_nodes = set()   # Conjunto para mantener un registro de los nodos visitados3
        self.search = search

    # Función para actualizar la UI
    def update_ui(self):
        try:
            generated, visited, path_cost, path, closed, fringe = next(self.search)
            print("-------------------------------")
            print(f"Generated: {generated}")
            print(f"Visited: {visited}")
            print(f"Path Cost: {path_cost}")
            print(f"Path: {path}")
            print(f"Closed: {closed}")
            print(f"Fringe: {fringe}")
            print("-------------------------------")

            # Actualiza la UI con los valores actuales
            status_label.config(
                text=f"Generated: {generated}, Visited: {visited}, Path Cost: {path_cost}\n"
                     f"Closed: {closed}\nFringe: {fringe}"
            )
            # Colorea el nodo actualmente visitado
            if path:
                current_node = path[0].state
                self.visited_nodes.add(current_node)  # Agrega el nodo actual a los visitados
                print("STATE: ", current_node)

                #ax.clear() # Redibuja el grafo para reflejar los nodos visitados
                nx.draw(G, pos, with_labels=True, nodelist=list(self.visited_nodes), node_size=1000, node_color='#A9FF00', font_size=10)
                edge_labels = nx.get_edge_attributes(G, 'weight')
                nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
                # Asegúrate de que el nodo actual está en el grafo antes de intentar colorearlo
                if current_node in pos:
                    nx.draw_networkx_nodes(G, pos, nodelist=[current_node], node_color='#FF00A9', node_size=700)
                canvas.draw()
                fig.canvas.flush_events()
            # Programa la siguiente actualización
            root.after(1000, self.update_ui)  # 500 milisegundos entre actualizaciones
        except StopIteration:
            # status_label.config(text="Search completed.")
            print("Search completed")


# Aquí debes definir las funciones que se llamarán cuando se presionen los botones
def on_dfs():
    print("DFS algorithm")

    # Obtenemos el problema de GPS que deseamos resolver
    problem = GPSProblem('A', 'B', romania)  # Usamos las claves tal como están definidas en el grafo

    # Creamos el generador
    search = depth_first_graph_search_generator(problem, Stack())

    myUI = UI(search)

    # Inicia la actualización de la UI
    myUI.update_ui()


def on_bfs():
    print("BFS algorithm")  # Aquí debe ir la lógica para DFS


def on_bab():
    print("Branch and Bound algorithm")  # Aquí debe ir la lógica para BAB


def on_bab_s():
    print("Branch and Bound with Underestimation algorithm")  # Aquí debe ir la lógica para BAB con subestimación


# Crear la ventana principal de Tkinter
root = tk.Tk()
root.title("Visualizador de Algoritmos de Búsqueda")

# Crear un frame para el panel del grafo
graph_frame = tk.Frame(root)
graph_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Dibujar el grafo en la figura y añadirlo al frame de Tkinter
fig, ax, G, pos = draw_fixed_graph()
canvas = FigureCanvasTkAgg(fig, master=graph_frame)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(fill=tk.BOTH, expand=True)

# Crear el frame para los botones de selección de algoritmo
buttons_frame = tk.Frame(root)
buttons_frame.pack(side=tk.RIGHT, padx=20)

# Crear botones para cada algoritmo de búsqueda con diseño personalizado
button_style = { 'fg': 'black', 'font': ('Helvetica', 16, 'bold'),
                'borderwidth': 0, 'relief': tk.FLAT, 'compound': tk.CENTER,
                 'image': tk.PhotoImage(file='./ui/button_design.png')}


# Crear botones para cada algoritmo de búsqueda
bfs_button = tk.Button(buttons_frame, text='BFS', command=on_bfs, **button_style)
dfs_button = tk.Button(buttons_frame, text='DFS', command=on_dfs, **button_style)
bab_button = tk.Button(buttons_frame, text='B&B', command=on_bab, **button_style)
bab_s_button = tk.Button(buttons_frame, text='B&B Sub', command=on_bab_s, **button_style)

# Asociar eventos de entrada/salida a los botones para el efecto de sombra
for b in [bfs_button, dfs_button, bab_button, bab_s_button]:
    b.bind("<Enter>", lambda event, btn=b: btn.config(relief=tk.RAISED))
    b.bind("<Leave>", lambda event, btn=b: btn.config(relief=tk.FLAT))

# Crear una fuente personalizada con tamaño y negrita
custom_font = font.Font(family='Helvetica', size=14, weight='bold')

# Agregamos la etiqueta para mostrar el estado del algoritmo
status_label = tk.Label(graph_frame, text="", justify=tk.LEFT, font=custom_font)
status_label.pack(side=tk.BOTTOM, anchor='sw')

bfs_button.pack(side=tk.TOP, pady=10)
dfs_button.pack(side=tk.TOP, pady=10)
bab_button.pack(side=tk.TOP, pady=10)
bab_s_button.pack(side=tk.TOP, pady=10)




root.mainloop()