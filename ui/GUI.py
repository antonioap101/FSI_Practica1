import tkinter as tk
from tkinter import font, ttk
from collections import deque
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from core.problem import GPSProblem
from core.search import romania, graph_search_generator
from core.utils import Stack, FIFOQueue
from ui.graph_data import GraphData

from ui.graph_visualizer import GraphVisualizer

class GUI:
    def __init__(self):
        # Set class variables
        self.graph_data = GraphData()
        self.graph_visualizer = GraphVisualizer(graph_data=self.graph_data, search=None)

        # Create Tkinter window
        self.root = tk.Tk()
        self.root.title("Search Algorithm Viewer")

        # Load required font and images for buttons
        self.__load_assets()

        # Setup frame for graph visualization
        self.__setup_graph_frame()

        # Setup frame for control buttons
        self.__setup_right_frame()

    def run(self):
        # Configura un manejador de eventos para el cierre de la ventana
        self.root.protocol("WM_DELETE_WINDOW", self.root.quit())
        self.root.mainloop()

    def __load_assets(self):
        self.custom_font = font.Font(family='Helvetica', size=14, weight='bold')
        self.button_design_image = tk.PhotoImage(file='assets/button_design.png')
        self.right_arrow_image = tk.PhotoImage(file='assets/right_arrow.png')
        self.left_arrow_image = tk.PhotoImage(file='assets/left_arrow.png')

    def __setup_graph_frame(self):
        self.graph_frame = tk.Frame(self.root)
        self.graph_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.graph_visualizer.draw_fixed_graph()
        self.canvas = FigureCanvasTkAgg(self.graph_data.fig, master=self.graph_frame)
        canvas_widget = self.canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)

        # Add label to show algorithm status
        self.status_label = tk.Label(self.graph_frame, text="", justify=tk.LEFT, font=self.custom_font)
        self.status_label.pack(side=tk.BOTTOM, anchor='sw')

    def __setup_right_frame(self):
        self.right_frame = tk.Frame(self.root)
        self.right_frame.pack(side=tk.RIGHT, padx=20)

        self.__create_legend()
        self.__create_dropdown_list()
        self.__create_buttons()

    def __create_dropdown_list(self):
        # Dropdown list of available paths
        routes = ['A - B', 'O - E', 'G - Z', 'N - D', 'M - F']

        # Create frame for route selection
        route_selection_frame = tk.Frame(self.right_frame)
        route_selection_frame.pack(side=tk.TOP, pady=40)

        # Create label for route selection
        route_label = tk.Label(route_selection_frame, text="Route:", font=self.custom_font)
        route_label.pack(side=tk.TOP)

        # Create Combobox to select route
        self.route_selector = ttk.Combobox(route_selection_frame, values=routes, font=self.custom_font,
                                           state="readonly", width=5)
        self.route_selector.pack(side=tk.TOP)
        self.route_selector.current(0)  # Establecer la selección predeterminada

    def __create_buttons(self):
        # Custom button design
        button_style = {'fg': 'black', 'font': ('Helvetica', 16, 'bold'),
                        'borderwidth': 0, 'relief': tk.FLAT, 'compound': tk.CENTER,
                        'image': self.button_design_image}

        # Custom button design
        button_style2 = {'fg': 'black', 'font': ('Helvetica', 16, 'bold'),
                         'borderwidth': 0, 'relief': tk.FLAT, 'compound': tk.CENTER,
                         'image': self.right_arrow_image}

        # Custom button design
        button_style3 = {'fg': 'black', 'font': ('Helvetica', 16, 'bold'),
                         'borderwidth': 0, 'relief': tk.FLAT, 'compound': tk.CENTER,
                         'image': self.left_arrow_image}

        # Create buttons for each search algorithm
        bfs_button = tk.Button(self.right_frame, text='BFS', command=self.__on_bfs, **button_style)
        dfs_button = tk.Button(self.right_frame, text='DFS', command=self.__on_dfs, **button_style)
        bab_button = tk.Button(self.right_frame, text='B&B', command=self.__on_bab, **button_style)
        bab_s_button = tk.Button(self.right_frame, text='B&B Sub', command=self.__on_bab_s, **button_style)

        # Adjust button position
        for b in [bfs_button, dfs_button, bab_button, bab_s_button]:
            b.pack(side=tk.TOP, pady=10)

        # Button to advance execution step by step
        advance_button = tk.Button(self.right_frame, text="", command=self.__advance_ui, **button_style2)
        advance_button.pack(side=tk.RIGHT, pady=10)

        # Button to reverse execution step by step
        reverse_button = tk.Button(self.right_frame, text="", command=self.__reverse_ui, **button_style3)
        reverse_button.pack(side=tk.LEFT, pady=10)

    def __create_legend(self):
        # Create a frame to hold color circles and their descriptions
        legend_frame = tk.Frame(self.right_frame)
        legend_frame.pack(side=tk.TOP, anchor='se', padx=10, pady=10)

        # Create a label to display the color legend
        legend_label = tk.Label(legend_frame, text="Node Color Legend:", font=self.custom_font)
        legend_label.grid(row=0, column=0, sticky='w', columnspan=2)

        # Function to create a color circle and its label in the legend
        def create_color_legend(row, color, description):
            canvas = tk.Canvas(legend_frame, width=20, height=20)
            canvas.grid(row=row, column=0)
            canvas.create_oval(5, 5, 20, 20, fill=color, outline=color)
            label = tk.Label(legend_frame, text=description, font=self.custom_font)
            label.grid(row=row, column=1, sticky='w')

        # Create entries in the legend with colors and descriptions
        create_color_legend(1, '#A9FF00', "Green = Visited")
        create_color_legend(2, '#FFD600', "Yellow = Visible")
        create_color_legend(3, '#00A9FF', "Blue = Unvisited")
        create_color_legend(4, '#FF00A9', "Red = Current Node")

    def __advance_ui(self):
        self.__update_ui(self.graph_visualizer.advance_graph)

    def __reverse_ui(self):
        self.__update_ui(self.graph_visualizer.reverse_graph)

    def __update_ui(self, function):
        if self.graph_data.algorithm is not None:
            generated, visited, path_cost, path, closed, fringe, position = function()
            # Updates te bottom label with current values
            self.status_label.config(
                text=f"Generated: {generated}, Visited: {visited}, Path Cost: {path_cost}, Step: {position}\n"
                     f"Visited: {closed}\nFringe: {fringe}"
            )
            self.canvas.draw()
        else:
            print("Search Algorithm not set!")

    def __get_selected_problem(self):
        selected_route = self.route_selector.get().split(' - ')
        if len(selected_route) == 2:
            start, end = selected_route
            return GPSProblem(start, end, romania)
        return None

    def __on_dfs(self):
        print("DFS algorithm")

        # We get the selected GPSProblem to solve and create the generator.
        search = graph_search_generator(self.__get_selected_problem(), Stack())

        # Updates the UI with the selected algorithm
        self.graph_data.algorithm = search
        self.graph_visualizer = GraphVisualizer(self.graph_data.algorithm, self.graph_data)
        self.__advance_ui()

    def __on_bfs(self):
        print("BFS algorithm")

        # We get the selected GPSProblem to solve and create the generator.
        search = graph_search_generator(self.__get_selected_problem(), FIFOQueue())

        # Updates the UI with the selected algorithm
        self.graph_data.algorithm = search
        self.graph_visualizer = GraphVisualizer(self.graph_data.algorithm, self.graph_data)
        self.__advance_ui()

    def __on_bab(self):
        print("Branch and Bound algorithm")

        def sort_by_path_cost(node, problem):
            return node.path_cost

        # We get the selected GPSProblem to solve and create the generator.
        search = graph_search_generator(self.__get_selected_problem(), deque(), sort_by_path_cost)

        # Updates the UI with the selected algorithm
        self.graph_data.algorithm = search
        self.graph_visualizer = GraphVisualizer(self.graph_data.algorithm, self.graph_data)
        self.__advance_ui()

    def __on_bab_s(self):
        print("Branch and Bound with Underestimation algorithm")

        def underestimation(node, problem):
            return node.path_cost + problem.h(node)

        # We get the selected GPSProblem to solve and create the generator.
        search = graph_search_generator(self.__get_selected_problem(), deque(), underestimation)

        # Updates the UI with the selected algorithm
        self.graph_data.algorithm = search
        self.graph_visualizer = GraphVisualizer(self.graph_data.algorithm, self.graph_data)
        self.__advance_ui()

