"""Search (Chapters 3-4)

The way to use this code is to subclass Problem to create a class of problems,
then create problem instances and solve them with calls to the various search
functions."""

from node import Node
from utils import *
from collections import deque
from problem import Problem, GPSProblem
from graph import Graph, UndirectedGraph, RandomGraph
import random, sys

romania = UndirectedGraph(Dict(
    A=Dict(Z=75, S=140, T=118),
    B=Dict(U=85, P=101, G=90, F=211),
    C=Dict(D=120, R=146, P=138),
    D=Dict(M=75),
    E=Dict(H=86),
    F=Dict(S=99),
    H=Dict(U=98),
    I=Dict(V=92, N=87),
    L=Dict(T=111, M=70),
    O=Dict(Z=71, S=151),
    P=Dict(R=97),
    R=Dict(S=80),
    U=Dict(V=142)))
romania.locations = Dict(
    A=(91, 492), B=(400, 327), C=(253, 288), D=(165, 299),
    E=(562, 293), F=(305, 449), G=(375, 270), H=(534, 350),
    I=(473, 506), L=(165, 379), M=(168, 339), N=(406, 537),
    O=(131, 571), P=(320, 368), R=(233, 410), S=(207, 457),
    T=(94, 410), U=(456, 350), V=(509, 444), Z=(108, 531))

australia = UndirectedGraph(Dict(
    T=Dict(),
    SA=Dict(WA=1, NT=1, Q=1, NSW=1, V=1),
    NT=Dict(WA=1, Q=1),
    NSW=Dict(Q=1, V=1)))
australia.locations = Dict(WA=(120, 24), NT=(135, 20), SA=(135, 30),
                           Q=(145, 20), NSW=(145, 32), T=(145, 42), V=(145, 37))

# ______________________________________________________________________________
## Uninformed Search algorithms

def graph_search_old(problem, fringe):
    """Search through the successors of a problem to find a goal.
    The argument fringe should be an empty queue.
    If two paths reach a state, only use the best one. [Fig. 3.18]"""
    closed = set()
    fringe.append(Node(problem.initial))
    generated = 1  # Counter for generated nodes (starts in 1)
    visited = 0    # Counter for visited nodes

    while fringe:
        node = fringe.pop()
        visited += 1
        if problem.goal_test(node.state):
            return generated, visited, node.path_cost, node.path()

        if node.state not in closed:
            closed.add(node.state)
            successors = node.expand(problem)
            generated += len(successors)
            fringe.extend(successors)

    return None


def depth_first_graph_search_generator(problem, fringe, sort_function=None):
    """Search the deepest nodes in the search tree first. [p 74]"""
    closed = set()
    fringe.append(Node(problem.initial))
    generated = 1  # Counter for generated nodes (starts in 1)
    visited = 0    # Counter for visited nodes

    while fringe:
        if sort_function:
            fringe = deque(sorted(list(fringe), key=lambda n: sort_function(n, problem)))
            node = fringe.popleft()
        else:
            node = fringe.pop()

        visited += 1
        if problem.goal_test(node.state):
            yield generated, visited, node.path_cost, node.path(), closed, fringe
            return
        if node.state not in closed:
            closed.add(node.state)
            successors = node.expand(problem)
            generated += len(successors)
            fringe.extend(successors)
            yield generated, visited, node.path_cost, node.path(), closed, fringe

    yield generated, visited, 0, None, closed, fringe


def graph_search(problem, fringe, sort_function=None):
    """Search through the successors of a problem to find a goal."""
    closed = set()
    fringe.append(Node(problem.initial))
    generated = 1  # Counter for generated nodes (starts in 1)
    visited = 0    # Counter for visited nodes

    while fringe:
        # Ordenar la cola en cada iteración si se proporciona una función de ordenación
        if sort_function:
            fringe = deque(sorted(list(fringe), key=lambda n: sort_function(n, problem)))
            node = fringe.popleft()
        else:
            node = fringe.pop()

        visited += 1

        if problem.goal_test(node.state):
            return generated, visited, node.path_cost, node.path()

        if node.state not in closed:
            closed.add(node.state)
            successors = node.expand(problem)
            generated += len(successors)
            fringe.extend(successors)

    return None


def breadth_first_graph_search(problem) -> Node:
    """Search the shallowest nodes in the search tree first. [p 74]"""
    return graph_search(problem, FIFOQueue())  # FIFOQueue -> fringe


def depth_first_graph_search(problem) -> Node:
    """Search the deepest nodes in the search tree first. [p 74]"""
    return graph_search(problem, Stack())


def branch_and_bound(problem) -> Node:
    """Branch and Bound search algorithm using graph_search."""
    def sort_by_path_cost(node, problem):
        return node.path_cost

    return graph_search(problem, deque(), sort_by_path_cost)


def branch_and_bound_underestimation(problem) -> Node:
    """Branch and Bound search algorithm with underestimation using graph_search."""
    def underestimation(node, problem):
        return node.path_cost + problem.h(node)

    # return bab_underestimation(problem, deque())
    return graph_search(problem, deque(), underestimation)

# _____________________________________________________________________________
# The remainder of this file implements examples for the search algorithms.


