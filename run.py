# Search methods

import search
from project_stub import *

from node import Node

ab = search.GPSProblem('A', 'B', search.romania)

print("PROBLEM BFS")
BFS = search.breadth_first_graph_search(ab)
BFS_path = BFS.path()
test_list = [Node('B'), Node('F'), Node('S'), Node('A')]

BFS_path_str = [str(n) for n in BFS.path()]
test_list_str = ["<Node B>", "<Node F>", "<Node S>", "<Node A>"]

print("RESSSS: ", BFS_path_str == test_list_str)

print("T1: ", type(BFS_path[0]), " | T2: ", type(test_list[0]))
print("T1: ", type(BFS_path_str[0]), " | T2: ", type(test_list_str[0]))
for n, n2 in zip(BFS_path_str, test_list_str):
    print("Node: ", n, " | Test: ", n2, " | Res: ", n==n2)

'''
print("PROBLEM DFS")
DFS = search.depth_first_graph_search(ab)
DFS_path = DFS.path()
print(DFS_path)
'''



# print("PROBLEM BAB")
# BAB = search.branch_and_bound(ab)
# print("PROBLEM BAB_SUB")
# BAB_SUB = search.branch_and_bound_underestimation(ab)

# Result:
# [<Node B>, <Node P>, <Node R>, <Node S>, <Node A>] : 101 + 97 + 80 + 140 = 418
# [<Node B>, <Node F>, <Node S>, <Node A>] : 211 + 99 + 140 = 450
