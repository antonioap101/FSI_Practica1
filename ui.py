import tkinter as tk
from collections import deque
from tkinter import font
from tkinter import ttk  # Importar ttk para el Combobox

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from problem import GPSProblem
from search import romania, graph_search_generator, BidirectionalIterator
from utils import Stack, FIFOQueue

# Utilizando el objeto 'romania' del código proporcionado
edges = [(node, neighbour, romania.dict[node][neighbour]) for node in romania.dict for neighbour in romania.dict[node]]
locations = {node: (x, y) for node, (x, y) in zip(romania.locations.keys(), romania.locations.values())}

# Convierte los nombres de los nodos a los nombres reales basados en la imagen
node_labels = {'A': 'Arad', 'B': 'Bucharest', 'C': 'Craiova', 'D': 'Drobeta', 'E': 'Eforie',
               'F': 'Fagaras', 'G': 'Giurgiu', 'H': 'Hirsova', 'I': 'Iasi', 'L': 'Lugoj',
               'M': 'Mehadia', 'N': 'Neamt', 'O': 'Oradea', 'P': 'Pitesti', 'R': 'Rimnicu Vilcea',
               'S': 'Sibiu', 'T': 'Timisoara', 'U': 'Urziceni', 'V': 'Vaslui', 'Z': 'Zerind'}

global_ui = None
global_algorithm = None

def set_global_ui(search):
    global global_ui
    global_ui = UI(search)

def advance_global_ui():
    if global_ui:
        global_ui.advance_ui()
    else:
        raise Exception("Global UI not set")

def reverse_global_ui():
    if global_ui:
        global_ui.reverse_ui()
    else:
        raise Exception("Global UI not set")


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
        self.search = BidirectionalIterator(search)
        self.position = 0
        self.last_path = None

        self.generated = None
        self.visited = None
        self.path = None
        self.path_cost = None
        self.closed = None
        self.fringe = None

    def update_ui(self):
        # Imprime por pantalla el estado actual de los elementos
        # self.print_status()
        # Actualiza la UI con los valores actuales
        status_label.config(
            text=f"Generated: {self.generated}, Visited: {self.visited}, Path Cost: {self.path_cost}, Step: {self.position}\n"
                 f"Visited: {self.closed}\nFringe: {self.fringe}"
        )
        # Colorea el nodo actualmente visitado
        if self.path:
            current_node = self.path[0].state # Agrega el nodo actual a los visitados

            ax.clear()  # Redibuja el grafo para reflejar los nodos visitados
            # Dibujamos los nodos visibles
            nx.draw(G, locations, with_labels=True, node_size=1000, node_color='#00A9FF', font_size=10)

            nx.draw(G, pos, with_labels=True, nodelist=list(n.state for n in self.fringe), node_size=1100,
                    node_color='#FFD600', font_size=10)

            # Dibujamos los nodos visitados
            nx.draw(G, pos, with_labels=True, nodelist=list(self.closed), node_size=1000,
                    node_color='#A9FF00', font_size=10)

            edge_labels = nx.get_edge_attributes(G, 'weight')

            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
            # Asegúrate de que el nodo actual está en el grafo antes de intentar colorearlo
            if current_node in pos:
                nx.draw_networkx_nodes(G, pos, nodelist=[current_node], node_color='#FF00A9', node_size=700)
            canvas.draw()
            fig.canvas.flush_events()
        # Programa la siguiente actualización
        # root.after(250, self.update_ui)  # 500 milisegundos entre actualizaciones

    def handle_search_completion(self):
        # status_label.config(text="Search completed.")
        print("Search completed")
        # Dibujamos el camino
        print("LAST: ", self.last_path)

        final_path_nodes = [node.state for node in self.last_path]
        nx.draw_networkx_nodes(G, pos, nodelist=final_path_nodes, node_color='black', node_size=1300)

        # Dibujar las etiquetas de los nodos del camino en blanco
        nx.draw_networkx_labels(G, pos, labels={n: n for n in final_path_nodes}, font_color='white', font_size=10)

        canvas.draw()

    def advance_ui(self):
        try:
            self.generated, self.visited, self.path_cost, self.path, self.closed, self.fringe = self.search.next()
            self.position += 1 # Almacenamos la posicion del iterador
            self.last_path = self.path.copy()
            self.update_ui()
        except StopIteration:
            self.handle_search_completion()

    def reverse_ui(self):
        try:
            self.generated, self.visited, self.path_cost, self.path, self.closed, self.fringe = self.search.prev()
            self.position -= 1  # Almacenamos la posicion del iterador
            self.last_path = self.path.copy()
            self.update_ui()
        except IndexError:
            pass


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


def get_selected_problem():
    selected_route = route_selector.get().split(' - ')
    if len(selected_route) == 2:
        start, end = selected_route
        return GPSProblem(start, end, romania)
    return None

# Aquí debes definir las funciones que se llamarán cuando se presionen los botones
def on_dfs():
    print("DFS algorithm")

    # Obtenemos el problema de GPS que deseamos resolver y creamos el generador
    search = graph_search_generator(get_selected_problem(), Stack())

    # Inicia la actualización de la UI
    set_global_ui(search)
    advance_global_ui()


def on_bfs():
    print("BFS algorithm")

    # Obtenemos el problema de GPS que deseamos resolver y creamos el generador
    search = graph_search_generator(get_selected_problem(), FIFOQueue())

    # Inicia la actualización de la UI
    set_global_ui(search)
    advance_global_ui()

def on_bab():
    print("Branch and Bound algorithm")

    def sort_by_path_cost(node, problem):
        return node.path_cost

    # Obtenemos el problema de GPS que deseamos resolver y creamos el generador
    search = graph_search_generator(get_selected_problem(), deque(), sort_by_path_cost)

    # Inicia la actualización de la UI
    set_global_ui(search)
    advance_global_ui()


def on_bab_s():
    print("Branch and Bound with Underestimation algorithm")

    def underestimation(node, problem):
        return node.path_cost + problem.h(node)

    # Creamos el generador
    search = graph_search_generator(get_selected_problem(), deque(), underestimation)

    # Inicia la actualización de la UI
    set_global_ui(search)
    advance_global_ui()


# Crear la ventana principal de Tkinter
root = tk.Tk()
root.title("Visualizador de Algoritmos de Búsqueda")

# Crear una fuente personalizada con tamaño y negrita
custom_font = font.Font(family='Helvetica', size=14, weight='bold')


# Crear un frame para el panel del grafo
graph_frame = tk.Frame(root)
graph_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# ..................... GRAFO .....................
# Dibujar el grafo en la figura y añadirlo al frame de Tkinter
fig, ax, G, pos = draw_fixed_graph()
canvas = FigureCanvasTkAgg(fig, master=graph_frame)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(fill=tk.BOTH, expand=True)

# ..................... INFORMACION ADDICONAL ABAJO  .....................
# Agregamos la etiqueta para mostrar el estado del algoritmo
status_label = tk.Label(graph_frame, text="", justify=tk.LEFT, font=custom_font)
status_label.pack(side=tk.BOTTOM, anchor='sw')

# ================================ PANEL DERECHO ===================================

# Crear el frame para los botones de selección de algoritmo
right_frame = tk.Frame(root)
right_frame.pack(side=tk.RIGHT, padx=20)

# ..................... LISTA DESPLEGABLE .....................
# Lista de recorridos disponibles
routes = ['A - B', 'O - E', 'G - Z', 'N - D', 'M - F']

# Crear un frame para la selección de recorridos
route_selection_frame = tk.Frame(right_frame)
route_selection_frame.pack(side=tk.TOP, pady=40)

# Crear una etiqueta para el selector de recorridos
route_label = tk.Label(route_selection_frame, text="Recorrido:", font=custom_font)
route_label.pack(side=tk.TOP)

# Crear el Combobox para seleccionar recorridos
route_selector = ttk.Combobox(route_selection_frame, values=routes, font=custom_font, state="readonly", width=5)
route_selector.pack(side=tk.TOP)
route_selector.current(0)  # Establecer la selección predeterminada

# ..................... BOTONES .....................
# Crear botones para cada algoritmo de búsqueda con diseño personalizado
button_style = { 'fg': 'black', 'font': ('Helvetica', 16, 'bold'),
                'borderwidth': 0, 'relief': tk.FLAT, 'compound': tk.CENTER,
                 'image': tk.PhotoImage(file='./ui/button_design.png')}


# Crear botones para cada algoritmo de búsqueda
bfs_button = tk.Button(right_frame, text='BFS', command=on_bfs, **button_style)
dfs_button = tk.Button(right_frame, text='DFS', command=on_dfs, **button_style)
bab_button = tk.Button(right_frame, text='B&B', command=on_bab, **button_style)
bab_s_button = tk.Button(right_frame, text='B&B Sub', command=on_bab_s, **button_style)

# Asociar eventos de entrada/salida a los botones para el efecto de sombra
for b in [bfs_button, dfs_button, bab_button, bab_s_button]:
    b.bind("<Enter>", lambda event, btn=b: btn.config(relief=tk.RAISED))
    b.bind("<Leave>", lambda event, btn=b: btn.config(relief=tk.FLAT))
    b.pack(side=tk.TOP, pady=10)

# ..................... LEYENDA .....................
# Creamos un frame para contener los círculos de colores y sus descripciones
legend_frame = tk.Frame(right_frame)
legend_frame.pack(side=tk.BOTTOM, anchor='se', padx=10, pady=10)

# Creamos una etiqueta para mostrar la leyenda de colores
legend_label = tk.Label(legend_frame,
                        text="Leyenda de Colores:",
                        font=custom_font)
legend_label.grid(row=0, column=0, sticky='w', columnspan=2)

# Función para crear un círculo de color y su etiqueta en la leyenda
def create_color_legend(row, color, description):
    canvas = tk.Canvas(legend_frame, width=20, height=20)
    canvas.grid(row=row, column=0)
    canvas.create_oval(5, 5, 20, 20, fill=color, outline=color)
    label = tk.Label(legend_frame, text=description, font=custom_font)
    label.grid(row=row, column=1, sticky='w')

# .............................. AVANCE .................................

# Creamos las entradas de la leyenda con los colores y las descripciones
create_color_legend(1, '#A9FF00', "Verde = Visitado")
create_color_legend(2, '#FFD600', "Amarillo = Visible")
create_color_legend(3, '#00A9FF', "Azul = No Visitado")
create_color_legend(4, '#FF00A9', "Rojo = Nodo Actual")

# Crear botones para cada algoritmo de búsqueda con diseño personalizado
button_style2 = { 'fg': 'black', 'font': ('Helvetica', 16, 'bold'),
                'borderwidth': 0, 'relief': tk.FLAT, 'compound': tk.CENTER,
                 'image': tk.PhotoImage(file='./ui/right_arrow.png')}

# Crear botones para cada algoritmo de búsqueda con diseño personalizado
button_style3 = { 'fg': 'black', 'font': ('Helvetica', 16, 'bold'),
                'borderwidth': 0, 'relief': tk.FLAT, 'compound': tk.CENTER,
                 'image': tk.PhotoImage(file='./ui/left_arrow.png')}


# Crear botón para avanzar en la ejecución paso a paso
advance_button = tk.Button(right_frame, text="", command=advance_global_ui, **button_style2)
advance_button.pack(side=tk.RIGHT, pady=10)

# Crear botón para avanzar en la ejecución paso a paso
reverse_button = tk.Button(right_frame, text="", command=reverse_global_ui, **button_style3)
reverse_button.pack(side=tk.LEFT, pady=10)

# Configura un manejador de eventos para el cierre de la ventana
root.protocol("WM_DELETE_WINDOW", root.quit())
root.mainloop()

