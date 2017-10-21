"""
utils package is for some quick utility methods

such as parsing
"""

from . import graph as g

class Tile(object):
    """Node represents basic unit of graph"""
    def __init__(self, x, y, symbol):
        self.x = x
        self.y = y
        self.symbol = symbol

    def __str__(self):
        return 'Tile(x: {}, y: {}, symbol: {})'.format(self.x, self.y, self.symbol)
    def __repr__(self):
        return 'Tile(x: {}, y: {}, symbol: {})'.format(self.x, self.y, self.symbol)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.x == other.x and self.y == other.y and self.symbol == other.symbol
        return False
    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(str(self.x) + "," + str(self.y) + self.symbol)



def parse_grid_file(graph, file_path):
    """
    ParseGridFile parses the grid file implementation from the file path line
    by line and construct the nodes & edges to be added to graph

    Returns graph object
    """
    # TODO: read the filepaht line by line to construct nodes & edges

    # TODO: for each node/edge above, add it to graph
    file = open(file_path)
    lines = file.readlines()

    rows = [] 

    for line in lines:
        # corner piece or the last and first rows
        if line[0] == '+':
            continue

        # exculde the edges
        board = line[1:-2]
        # add a list of every to blocks as an entry to the row
        rows.append([board[i:i+2] for i in range(0, len(board), 2)])


    nodes = []
    edges = []

    y = 0
    for row in rows:
        x = 0
        for coord in row:
            # not a wall
            if coord != '##':
                node = g.Node(Tile(x,y,coord))
                nodes.append(node)

                # surrounding coord
                adjacents = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
                for adjacent in adjacents:
                    #check if coord is in bounds
                    if not (adjacent[0] >= len(rows[0]) or adjacent[0] < 0 or adjacent[1] >= len(rows) or adjacent[1] < 0):
                        # again if not wall
                        current_coord = rows[adjacent[1]][adjacent[0]]
                        if current_coord != '##':
                            to_node = g.Node(Tile(adjacent[0], adjacent[1], current_coord))
                            edges.append(g.Edge(node, to_node, 1))
            x += 1
        y += 1 


    for node in nodes:
        graph.add_node(node)
    for edge in edges:
        graph.add_edge(edge)

    file.close()
    return graph

def convert_edge_to_grid_actions(edges):
    """
    Convert a list of edges to a string of actions in the grid base tile

    e.g. Edge(Node(Tile(1, 2), Tile(2, 2), 1)) => "S"
    """
    actions = ""
    for edge in edges:
        if edge.from_node.data.y > edge.to_node.data.y:
            actions += 'N'
        elif edge.from_node.data.x < edge.to_node.data.x:
            actions += 'E'
        elif edge.from_node.data.y < edge.to_node.data.y:
            actions +='S'
        else:
            actions += 'W'
    return actions