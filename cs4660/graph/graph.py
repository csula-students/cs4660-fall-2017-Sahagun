"""
graph module defines the knowledge representations files

A Graph has following methods:

* adjacent(node_1, node_2)
    - returns true if node_1 and node_2 are directly connected or false otherwise
* neighbors(node)
    - returns all nodes that is adjacency from node
* add_node(node)
    - adds a new node to its internal data structure.
    - returns true if the node is added and false if the node already exists
* remove_node
    - remove a node from its internal data structure
    - returns true if the node is removed and false if the node does not exist
* add_edge
    - adds a new edge to its internal data structure
    - returns true if the edge is added and false if the edge already existed
* remove_edge
    - remove an edge from its internal data structure
    - returns true if the edge is removed and false if the edge does not exist
"""

from io import open
from operator import itemgetter

def construct_graph_from_file(graph, file_path):
    """
    TODO: read content from file_path, then add nodes and edges to graph object

    note that grpah object will be either of AdjacencyList, AdjacencyMatrix or ObjectOriented

    In example, you will need to do something similar to following:

    1. add number of nodes to graph first (first line)
    2. for each following line (from second line to last line), add them as edge to graph
    3. return the graph
    """
    file = open(file_path, encoding="utf-8")
    lines = file.readlines()

    num_nodes = int(lines[0]) #  number of nodes read from the first line of the files.

    for i in range(num_nodes):
        node = Node(i)
        graph.add_node(node)


    lines.pop(0) # removes the first line from the file.

    for line in lines:
        # Converts "1:2:3" -> [1,2,3]
        data = list(map(int, line.split(':')))
        edge = Edge(Node(data[0]), Node(data[1]), data[2])
        graph.add_edge(edge)

    file.close()
    return graph

class Node(object):
    """Node represents basic unit of graph"""
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return 'Node({})'.format(self.data)
    def __repr__(self):
        return 'Node({})'.format(self.data)

    def __eq__(self, other_node):
        return self.data == other_node.data
    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.data)

class Edge(object):
    """Edge represents basic unit of graph connecting between two edges"""
    def __init__(self, from_node, to_node, weight):
        self.from_node = from_node
        self.to_node = to_node
        self.weight = weight
    def __str__(self):
        return 'Edge(from {}, to {}, weight {})'.format(self.from_node, self.to_node, self.weight)
    def __repr__(self):
        return 'Edge(from {}, to {}, weight {})'.format(self.from_node, self.to_node, self.weight)

    def __eq__(self, other_node):
        return self.from_node == other_node.from_node and self.to_node == other_node.to_node and self.weight == other_node.weight
    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.from_node, self.to_node, self.weight))


class AdjacencyList(object):
    """
    AdjacencyList is one of the graph representation which uses adjacency list to
    store nodes and edges
    """
    def __init__(self):
        # adjacencyList should be a dictonary of node to edges
        self.adjacency_list = {}

    def adjacent(self, node_1, node_2):
        if node_1 not in self.adjacency_list:
            return False

        for edge in self.adjacency_list[node_1]:
            if edge.to_node == node_2:
                return True

        return False

    def neighbors(self, node):
        neighbors = []
        if node in self.adjacency_list:
            for edge in self.adjacency_list[node]:
                neighbors.append(edge.to_node)

        return neighbors

    def add_node(self, node):
        if node in self.adjacency_list.keys():
            return False
        self.adjacency_list[node] = []
        return True

    def remove_node(self, node):
        if node not in self.adjacency_list.keys():
            return False

        self.adjacency_list.pop(node)

        for edges_list in self.adjacency_list.values():
            remove_list = []
            for edge in edges_list:
                if edge.to_node == node:
                    remove_list.append(edge)
            for edge in remove_list:
                edges_list.remove(edge)

        return True

    def add_edge(self, edge):
        from_node = edge.from_node
        to_node = edge.to_node

        if from_node not in self.adjacency_list.keys():
            return False

        if to_node not in self.adjacency_list.keys():
            return False

        if edge in self.adjacency_list[from_node]:
            return False

        self.adjacency_list[from_node].append(edge)

        return True

    def remove_edge(self, edge):
        from_node = edge.from_node

        if from_node not in self.adjacency_list.keys():
            return False

        if edge not in self.adjacency_list[from_node]:
            return False

        self.adjacency_list[from_node].remove(edge)

        return True


    def distance(self, node_1, node_2):
        if node_1 in self.adjacency_list:
            for edge in self.adjacency_list[node_1]:
                if edge.to_node == node_2:
                    return edge.weight

        return None


class AdjacencyMatrix(object):
    def __init__(self):
        # adjacency_matrix should be a two dimensions array of numbers that
        # represents how one node connects to another
        self.adjacency_matrix = []
        # in additional to the matrix, you will also need to store a list of Nodes
        # as separate list of nodes
        self.nodes = []

    def adjacent(self, node_1, node_2):
        i = self.__get_node_index(node_1)
        j = self.__get_node_index(node_2)
        return self.adjacency_matrix[i][j] != 0

    def neighbors(self, node):
        index = self.__get_node_index(node)
        neighbors = []
        for i in range(len(self.nodes)):
            if self.adjacency_matrix[index][i] != 0:
                neighbors.append(self.nodes[i]) 
        return neighbors

    def add_node(self, node):

        if node in self.nodes:
            return False

        self.nodes.append(node)

        # add a new col of 0s
        for i in range(len(self.adjacency_matrix)):
            self.adjacency_matrix[i].append(0)

        # add new row of 0s
        size = len(self.nodes)
        row = [0 for x in range(size)]
        self.adjacency_matrix.append(row)

        return True


    def remove_node(self, node):
        if node not in self.nodes:
            return False
        

        self.nodes.remove(node)
        index = self.__get_node_index(node)

        # removes the col
        for i in range(len(self.adjacency_matrix)):
            self.adjacency_matrix[i].pop(index - 1)

        # removes the row
        self.adjacency_matrix.pop(index - 1)
        return True




    def add_edge(self, edge):
        i = self.__get_node_index(edge.from_node)
        j = self.__get_node_index(edge.to_node)
        if self.adjacency_matrix[i][j] != 0:
            return False

        self.adjacency_matrix[i][j] = edge.weight
        return True



    def remove_edge(self, edge):
        i = self.__get_node_index(edge.from_node)
        j = self.__get_node_index(edge.to_node)

        if self.adjacency_matrix[i][j] == 0:
            return False

        self.adjacency_matrix[i][j] = 0
        return True


    def __get_node_index(self, node):
        """helper method to find node index"""
        try:
            return self.nodes.index(node)
        except:
            return False

    def distance(self, node_1, node_2):
        if node_1 not in self.nodes or node_2 not in self.nodes:
            return None
        i = self.__get_node_index(node_1)
        j = self.__get_node_index(node_2)
        return self.adjacency_matrix[i][j]

class ObjectOriented(object):
    """ObjectOriented defines the edges and nodes as both list"""
    def __init__(self):
        # implement your own list of edges and nodes
        self.edges = []
        self.nodes = []

    def adjacent(self, node_1, node_2):
        for edge in self.edges:
            if edge.from_node == node_1:
                if edge.to_node == node_2:
                    return True
        return False

    def neighbors(self, node):
        neighbors = []
        for edge in self.edges:
            if edge.from_node == node:
                neighbors.append(edge.to_node)
        return neighbors


    def add_node(self, node):
        if node in self.nodes:
            return False

        self.nodes.append(node)
        return True

    def remove_node(self, node):
        if node not in self.nodes:
            return False

        edges_to_remove = []

        for edge in self.edges:
            if edge.from_node == node or edge.to_node == node:
                edges_to_remove.append(edge)

        for edge in edges_to_remove:
            self.edges.remove(edge)

        return True


    def add_edge(self, edge):
        if edge.from_node not in self.nodes:
            return False

        if edge.to_node not in self.nodes:
            return False

        if edge in self.edges:
            return False

        self.edges.append(edge)
        return True

    def remove_edge(self, edge):
        if edge not in self.edges:
            return False

        self.edges.remove(edge)
        return True

    def distance(self, from_node, to_node):
        for edge in self.edges:
            if edge.from_node == from_node and edge.to_node == to_node:
                return edge.weight
        return None