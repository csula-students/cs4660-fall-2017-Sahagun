"""
quiz2!

Use path finding algorithm to find your way through dark dungeon!

Tecchnical detail wise, you will need to find path from node 7f3dc077574c013d98b2de8f735058b4
to f1f131f647621a4be7c71292e79613f9

TODO: implement BFS
TODO: implement Dijkstra utilizing the path with highest effect number
"""
import graph
import searches

import math

import json
import codecs

# http lib import for Python 2 and 3: alternative 4
try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

GET_STATE_URL = "http://192.241.218.106:9000/getState"
STATE_TRANSITION_URL = "http://192.241.218.106:9000/state"

def get_state(room_id):
    """
    get the room by its id and its neighbor
    """
    body = {'id': room_id}
    return __json_request(GET_STATE_URL, body)

def transition_state(room_id, next_room_id):
    """
    transition from one room to another to see event detail from one room to
    the other.

    You will be able to get the weight of edge between two rooms using this method
    """
    body = {'id': room_id, 'action': next_room_id}
    return __json_request(STATE_TRANSITION_URL, body)

def __json_request(target_url, body):
    """
    private helper method to send JSON request and parse response JSON
    """
    req = Request(target_url)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    jsondata = json.dumps(body)
    jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
    req.add_header('Content-Length', len(jsondataasbytes))
    reader = codecs.getreader("utf-8")
    response = json.load(reader(urlopen(req, jsondataasbytes)))
    return response


def distance(n1, n2):
    n1x = int(n1.data["location"]["x"])
    n1y = int(n1.data["location"]["y"])

    n2x = int(n2.data["location"]["x"])
    n2y = int(n2.data["location"]["y"])
    return math.sqrt((n1x - n2x)**2 + (n1y - n2y)**2)

def bfs(initial_node, end_node_id = "f1f131f647621a4be7c71292e79613f9"):
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

    if initial_node.data == end_node_id:
        return []

    while open_set:
        # current = [dist, node]
        current = open_set.pop(0) 
        current_dist = current[0]
        current_node = current[1]

        neighbors = []
        room = get_state(current_node.data)
        for n in room["neighbors"]: # list of dict
            new_node = graph.Node(n["id"])
            neighbors.append(new_node)

        for child_node in neighbors:
            #effect
            #    print(transition_state(empty_room['id'], empty_room['neighbors'][0]['id']))
            dist = transition_state(current_node.data, child_node.data)["event"]["effect"]
            # calculate the dist of the current node and its child plus the dist already traveled
            child_dist = distance_dict[current_node] + dist
            child = (child_dist, child_node)

            # already visted
            if child_node in close_set:
                continue

            # put the child into the dict
            if child not in open_set:
                distance_dict[child_node] = child_dist
                parent_nodes[child_node] = current_node
                
                if child_node.data == end_node_id:
                    return construct_path(child_node, parent_nodes, distance_dict)

                open_set.append(child)

        close_set.append(current_node)


def construct_path(node, parents, dist_dict):
    path = []
    while node in parents:
        parent = parents[node]
        path.append(parent.data + " to " + node.data + ":" + str(dist_dict[node]))
        node = parents[node]
    return list(reversed(path))



if __name__ == "__main__":
    # Your code starts here
    empty_room = get_state('7f3dc077574c013d98b2de8f735058b4')
    # goal f1f131f647621a4be7c71292e79613f9
    initial_node = graph.Node(empty_room["id"])

    print("BFS Path:")
    b = bfs(initial_node)
    for i in b:
        print(i)
"""
    print(empty_room)
    print()
    print(transition_state(empty_room['id'], empty_room['neighbors'][0]['id']))
"""
