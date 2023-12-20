import unittest
import search  # Asegúrate de que este módulo esté en tu PATH o proporciona la ruta completa.
from collections import namedtuple, deque
import time

from utils import FIFOQueue, Stack

# Defining a namedtuple for the search results
Result = namedtuple('Result', ['generated', 'visited', 'total_cost', 'path'])

class SearchAlgorithmTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.routes = ['Arad-Bucharest', 'Oradea-Eforie', 'Giurgiu-Zeriod','Neamt-Dobreta', 'Mehadia-Fagaras']

        cls.problems = {
            'Arad-Bucharest': search.GPSProblem('A', 'B', search.romania),
            'Oradea-Eforie': search.GPSProblem('O', 'E', search.romania),
            'Giurgiu-Zeriod': search.GPSProblem('G', 'Z', search.romania),
            'Neamt-Dobreta': search.GPSProblem('N', 'D', search.romania),
            'Mehadia-Fagaras': search.GPSProblem('M', 'F', search.romania)
        }

        # Results for Breadth-First Search (DFS)
        cls.resultsBFS = {
            'Arad-Bucharest': Result(generated=21, visited=16, total_cost=450, path=['B', 'F', 'S', 'A']),
            'Oradea-Eforie': Result(generated=45, visited=43, total_cost=730, path=['E', 'H', 'U', 'B', 'F', 'S', 'O']),
            'Giurgiu-Zeriod': Result(generated=41, visited=34, total_cost=615, path=['Z', 'A', 'S', 'F', 'B', 'G']),
            'Neamt-Dobreta': Result(generated=32, visited=26, total_cost=765, path=['D', 'C', 'P', 'B', 'U', 'V', 'I', 'N']),
            'Mehadia-Fagaras': Result(generated=31, visited=23, total_cost=520, path=['F', 'S', 'R', 'C', 'D', 'M'])
        }

        # Results for Depth-First Search (DFS)
        cls.resultsDFS = {
            'Arad-Bucharest': Result(generated=18, visited=10, total_cost=733, path=['B', 'P', 'C', 'D', 'M', 'L', 'T', 'A']),
            'Oradea-Eforie': Result(generated=41, visited=31, total_cost=698, path=['E', 'H', 'U', 'B', 'P', 'R', 'S', 'O']),
            'Giurgiu-Zeriod': Result(generated=32, visited=21, total_cost=1284, path=['Z', 'A', 'T', 'L', 'M', 'D', 'C', 'P', 'R', 'S', 'F', 'B', 'G']),
            'Neamt-Dobreta': Result(generated=31, visited=19, total_cost=1151, path=['D', 'C', 'P', 'R', 'S', 'F', 'B', 'U', 'V', 'I', 'N']),
            'Mehadia-Fagaras': Result(generated=29, visited=18, total_cost=928, path=['F', 'B', 'P', 'R', 'S', 'A', 'T', 'L', 'M'])
        }

        # Results for Branch and Bound (BAB)
        cls.resultsBAB = {
            'Arad-Bucharest': Result(generated=31, visited=24, total_cost=418, path=['B', 'P', 'R', 'S', 'A']),
            'Oradea-Eforie': Result(generated=43, visited=40, total_cost=698, path=['E', 'H', 'U', 'B', 'P', 'R', 'S', 'O']),
            'Giurgiu-Zeriod': Result(generated=41, visited=35, total_cost=583, path=['Z', 'A', 'S', 'R', 'P', 'B', 'G']),
            'Neamt-Dobreta': Result(generated=32, visited=26, total_cost=765, path=['D', 'C', 'P', 'B', 'U', 'V', 'I', 'N']),
            'Mehadia-Fagaras': Result(generated=36, visited=27, total_cost=520, path=['F', 'S', 'R', 'C', 'D', 'M'])
        }

        # Results for Branch and Bound with Underestimation (BAB_U)
        cls.resultsBAB_U = {
            'Arad-Bucharest': Result(generated=16, visited=6, total_cost=418, path=['B', 'P', 'R', 'S', 'A']),
            'Oradea-Eforie': Result(generated=32, visited=15, total_cost=698, path=['E', 'H', 'U', 'B', 'P', 'R', 'S', 'O']),
            'Giurgiu-Zeriod': Result(generated=26, visited=12, total_cost=583, path=['Z', 'A', 'S', 'R', 'P', 'B', 'G']),
            'Neamt-Dobreta': Result(generated=23, visited=12, total_cost=765, path=['D', 'C', 'P', 'B', 'U', 'V', 'I', 'N']),
            'Mehadia-Fagaras': Result(generated=25, visited=16, total_cost=520, path=['F', 'S', 'R', 'C', 'D', 'M'])
        }

    def __measure_execution_time(self, problem, fringe, sort_function=None):
        """
        Función para medir el tiempo de ejecución de un algoritmo de búsqueda.
        """
        start_time = time.perf_counter()
        search.graph_search(problem, fringe, sort_function)
        end_time = time.perf_counter()
        execution_time = (end_time - start_time)* 1000  # Convertir a milisegundos
        return execution_time


    def __test_with_function(self, search_function=None, expected_results=None, print_enable=False):
        if search_function is None or expected_results is None:
            return

        for route in self.routes:
            # Check the result is not None
            result = search_function(self.problems[route])
            self.assertIsNotNone(result)

            # Save the results to the class property
            self.result = Result(generated=result[0],
                                 visited=result[1],
                                 total_cost=result[2],
                                 path=result[3])

            # Creating formatted path variables to test
            expected_path = [f"<Node {n}>" for n in expected_results[route].path]
            returned_path = [str(n) for n in self.result.path]

            # Assert the generated nodes are right
            if print_enable:
                print("[GEN] Res: ", self.result.generated, " | Exp: ", expected_results[route].generated)
            self.assertEqual(expected_results[route].generated, self.result.generated)

            # Assert the visited nodes are right
            if print_enable:
                print("[VIS] Res: ", self.result.visited, " | Exp: ", expected_results[route].visited)
            self.assertEqual(expected_results[route].visited, self.result.visited,)

            # Assert the total cost is right
            if print_enable:
                print("[TOT] Res: ", self.result.total_cost, " | Exp: ", expected_results[route].total_cost)
            self.assertEqual(expected_results[route].total_cost, self.result.total_cost)

            # Assert the path is right
            if print_enable:
                print("[PATH] Res: ", self.result.path, " | Exp: ", expected_results[route].path)
            self.assertEqual(expected_path, returned_path)

    def test_times(self):
        print("========================TIEMPOS DE EJECUCIÓN========================")
        for route in self.routes:
            # Check the result is not None
            problem = self.problems[route]
            time_bfs = self.__measure_execution_time(problem, FIFOQueue())
            time_dfs = self.__measure_execution_time(problem, Stack())
            time_bab = self.__measure_execution_time(problem, deque())
            time_bab_s = self.__measure_execution_time(problem, deque())

            print("--------------", route, "--------------")
            print("Tiempo BFS:", time_bfs, "ms")
            print("Tiempo DFS:", time_dfs, "ms")
            print("Tiempo Branch and Bound:", time_bab, "ms")
            print("Tiempo Branch and Bound con Subestimación:", time_bab_s, "ms")

    def test_breadth_first_search(self):
        self.__test_with_function(search_function=search.breadth_first_graph_search,
                                  expected_results=self.resultsBFS, print_enable=False)

    def test_depth_first_search(self):
        self.__test_with_function(search_function=search.depth_first_graph_search,
                                  expected_results=self.resultsDFS, print_enable=False)

    def test_branch_and_bound(self):
        self.__test_with_function(search_function=search.branch_and_bound,
                                  expected_results=self.resultsBAB, print_enable=False)

    def test_branch_and_bound_underestimation(self):
        self.__test_with_function(search_function=search.branch_and_bound_underestimation,
                                  expected_results=self.resultsBAB_U, print_enable=False)


if __name__ == '__main__':
    unittest.main()
