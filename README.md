# FSI Practice 1: Search Algorithm Viewer

## Description

This project, "Search Algorithm Viewer," is a Python-based visualizer for graph search algorithms. It provides a Graphical User Interface (GUI) to visualize the operations of various search algorithms on graphs or networks, making it an excellent educational tool for understanding algorithmic behavior in graph theory.

## Project Objectives

The project's primary objective, as described in the practice instructions, revolves around developing and comparing search algorithms. The tasks include:

1. Implementing the Branch and Bound search strategy, utilizing the Romanian cities graph provided in the base code.
2. Comparing the number of nodes expanded by this method against Breadth-First Search and Depth-First Search methods.
3. Optionally, manually tracing a search to demonstrate understanding.

Additionally, a second part involves:

1. Implementing Branch and Bound with Underestimation (an informed search strategy). The Romanian cities graph is again used, with a straight-line distance heuristic.
2. Comparing the nodes expanded by this method against the standard Branch and Bound method.
3. Optionally, demonstrating through a manual example that if the heuristic is not consistent, the optimality of the search is not guaranteed.

This comprehensive approach allows for a deeper understanding of search algorithms in AI, with a focus on algorithm efficiency and heuristic effectiveness.

## Project Structure

The project is organized into several main directories, each serving a specific purpose:

- `core`: Contains the core logic of the project. This includes the implementation of search algorithms, node and problem definitions, and various utilities.
- `ui`: Hosts files related to the user interface, including the graph visualizer and the main GUI components.
- `assets`: Contains graphical resources such as images used in the user interface.
- `test`: Includes tests to validate the functionality of the project components.

### Key Components

- `run.py`: The main script to run the application.
- `core/search.py`: Implements various search algorithms, including Depth-First-Search, Breadth-First-Search, Branch and Bound and Branch and Bound with Sub-estimation
- `ui/GUI.py`: Defines the primary user interface for interacting with the search algorithms.

## Running the Project

To run the visualizer, ensure you have the necessary dependencies installed, and then execute the `run.py` script:

```bash
python run.py
```

## Implemented Tests
To verify the correct functioning of the implemented algorithms, the following tests have been developed and checked:

| ID | Origin  | Destination | Breadth-First Search | Depth-First Search | Branch and Bound | Branch and Bound with Underestimation |
|----|---------|-------------|----------------------|--------------------|------------------|--------------------------------------|
| 1  | Arad    | Bucharest   | Generated: 21<br>Visited: 16<br>Cost: 450<br>Path: B, F, S, A | Generated: 18<br>Visited: 10<br>Cost: 733<br>Path: B, P, C, D, M, L, T, A | Generated: 31<br>Visited: 24<br>Cost: 418<br>Path: B, P, R, S, A | Generated: 16<br>Visited: 6<br>Cost: 418<br>Path: B, P, R, S, A |
| 2  | Oradea  | Eforie      | Generated: 45<br>Visited: 43<br>Cost: 730<br>Path: E, H, U, B, F, S, O | Generated: 41<br>Visited: 31<br>Cost: 698<br>Path: E, H, U, B, P, R, S, O | Generated: 43<br>Visited: 40<br>Cost: 698<br>Path: E, H, U, B, P, R, S, O | Generated: 32<br>Visited: 15<br>Cost: 698<br>Path: E, H, U, B, P, R, S, O |
| 3  | Giurgiu | Zerind      | Generated: 41<br>Visited: 34<br>Cost: 615<br>Path: Z, A, S, F, B, G | Generated: 32<br>Visited: 21<br>Cost: 1284<br>Path: Z, A, T, L, M, D, C, P, R, S, F, B, G | Generated: 41<br>Visited: 35<br>Cost: 583<br>Path: Z, A, S, R, P, B, G | Generated: 26<br>Visited: 12<br>Cost: 583<br>Path: Z, A, S, R, P, B, G |
| 4  | Neamt   | Drobeta     | Generated: 32<br>Visited: 26<br>Cost: 765<br>Path: D, C, P, B, U, V, I, N | Generated: 31<br>Visited: 19<br>Cost: 1151<br>Path: D, C, P, R, S, F, B, U, V, I, N | Generated: 32<br>Visited: 26<br>Cost: 765<br>Path: D, C, P, B, U, V, I, N | Generated: 23<br>Visited: 12<br>Cost: 765<br>Path: D, C, P, B, U, V, I, N |
| 5  | Mehadia | Fagaras     | Generated: 31<br>Visited: 23<br>Cost: 520<br>Path: F, S, R, C, D, M | Generated: 29<br>Visited: 18<br>Cost: 928<br>Path: F, B, P, R, S, A, T, L, M | Generated: 36<br>Visited: 27<br>Cost: 520<br>Path: F, S, R, C, D, M | Generated: 25<br>Visited: 16<br>Cost: 520<br>Path: F, S, R, C, D, M |

## Dependencies

This project relies on several Python libraries, including Tkinter for the user interface and NetworkX for graph manipulation. Ensure these libraries are installed before running the project. The project was developed using Python version 3.9.18. You can install the dependencies with the following commands:

```bash
pip install matplotlib networkx tk
```

Note: Tkinter usually comes pre-installed with Python. If it's not installed, you can install it using your system's package manager.

## Contributing

Contributions to the project are welcome. If you wish to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your changes.
3. Submit a pull request with your changes.

## License

This project is licensed under the GNU General Public License v3.0. For more information, see the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html).

---

