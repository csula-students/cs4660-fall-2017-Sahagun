"""
Searches module defines all different search algorithms
"""
from graph import graph as Graph
import queue
import math

def bfs(graph, initial_node, dest_node):
    """
    Breadth First Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """

    # vars
    open_set = [] # will vist, will be of tuples, treat as queue
    close_set = [] # have visted, will be of edges

    distance_dict = {}
    parent_nodes = {}

    v = (0, initial_node) 
    # u later one will be the same struct as v


    # initialize
    distance_dict[initial_node] = v[0];
    open_set.append(v)


    if initial_node == dest_node:
        return []

    while open_set:
        # current = [dist, node]
        current = open_set.pop(0) 
        current_dist = current[0]
        current_node = current[1]

        for child_node in graph.neighbors(current_node):

            # calculate the dist of the current node and its child plus the dist already traveled
            child_dist = distance_dict[current_node] + graph.distance(current_node, child_node)
            child = (child_dist, child_node)

            # already visted
            if child in close_set:
                continue

            # put the child into the dict
            if child not in open_set:
                distance_dict[child_node] = child_dist
                parent_nodes[child_node] = current_node
                
                if child_node == dest_node:
                    return construct_path(child_node, parent_nodes, graph)

                open_set.append(child)

        close_set.append(current)


def construct_path(node, parents, graph):
    path = []
    while node in parents:
        path.append(Graph.Edge(parents[node], node, graph.distance(parents[node], node)))
        node = parents[node]
    return list(reversed(path))




def dfs(graph, initial_node, dest_node):
    """
    Depth First Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """

    parent_nodes = {} #dict of child to parent
    discovered_nodes = [] #list of found nodes
    dfs_recursion_aux(graph, initial_node,discovered_nodes,parent_nodes)


    # find the path back starting at the dest node
    path = []
    current_node = dest_node
    while current_node != initial_node:
        next_node = parent_nodes[current_node]
        path.insert(0, Graph.Edge(next_node, current_node, graph.distance(next_node, current_node)))
        current_node = next_node

    return path

def dfs_recursion_aux(graph, current_node, discovered, parents):
    # discovered is a dict of node and bool
    # parents is a dict of child to parent nodes
    for neighbor in graph.neighbors(current_node):
        if neighbor not in discovered:
            discovered.append(neighbor)
            parents[neighbor] = current_node
            dfs_recursion_aux(graph, neighbor, discovered, parents)

def dijkstra_search(graph, initial_node, dest_node):
    """
    Dijkstra Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    # vars
    open_set = []# will vist, will be of tuples, treat as queue
    close_set = [] # have visted, will be of edges

    distance_dict = {}
    parent_nodes = {}

    v = (0, initial_node)
    # u later one will be the same struct as v

    last_node = None;

    # initialize
    distance_dict[initial_node] = v[0];
    open_set.append(v)


    if initial_node == dest_node:
        return []

    while open_set:
        # current = [dist, node]
        current = open_set.pop(0)
        current_dist = current[0]
        current_node = current[1]

        for child_node in graph.neighbors(current_node):
            # calculate the dist of the current node and its child plus the dist already traveled
            child_dist = distance_dict[current_node] + graph.distance(current_node, child_node)
            child = (child_dist, child_node)

            # put the child into the dict
            # queues are not iterable so cant check if in openset
            if child_node not in distance_dict or (child_dist < distance_dict[child_node]):
                distance_dict[child_node] = child_dist
                parent_nodes[child_node] = current_node
                if dest_node == child_node:
                    last_node = child_node
                open_set.append(child)
        close_set.append(current)
    return construct_path(dest_node, parent_nodes, graph)

def a_star_search(graph, initial_node, dest_node):
    """
    A* Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """

    frontier = [] # treat as a queue
    explored_set = [] # treat as a set
    parent_nodes = {}

    initial = (0, initial_node) 
    frontier.append(initial)

    g_score = {}
    g_score[initial_node] = 0

    f_score = {}
    f_score[initial_node] = heuristicCost(initial_node, dest_node)

    while frontier:
        current = frontier.pop(0)
        current_dist = current[0]
        current_node = current[1]

        if current_node == dest_node:
            return construct_path(dest_node, parent_nodes, graph)
        explored_set.append(current_node)

        for node in graph.neighbors(current_node):
            if node in explored_set:
                continue

            temp_g_score = g_score[current_node] + graph.distance(current_node, node)

            if node not in g_score:
                frontier.append((float('inf'), node))
                g_score[node] = float('inf')
                f_score[node] = float('inf')

            elif temp_g_score >= g_score[node]:
                continue

            parent_nodes[node] = current_node
            g_score[node] = temp_g_score
            f_score[node] = g_score[node] + heuristicCost(node, dest_node)

    return []


def heuristicCost(from_node, to_node):
    d = 1
    dx = abs(from_node.data.x - to_node.data.x)  
    dy = abs(from_node.data.y - to_node.data.y)
    return d * math.sqrt(dx * dx + dy * dy)