from p1 import dijkstras_shortest_path, navigation_edges
from math import inf, sqrt
from heapq import heappop, heappush

def find_path (source_point, destination_point, mesh):

    """
    Searches for a path from source_point to destination_point through the mesh

    Args:
        source_point: starting point of the pathfinder
        destination_point: the ultimate goal the pathfinder must reach
        mesh: pathway constraints the path adheres to

    Returns:

        A path (list of points) from source_point to destination_point if exists
        A list of boxes explored by the algorithm
    """

    print(mesh['adj'])
    print(source_point)

    # Pseudocode found at: https://en.wikipedia.org/wiki/A*_search_algorithm (10/12/18)

    evaluated = [] # set of black nodes
    queue = [(0,source_point)] # priority queue of nodes to look at
    parent = {} # dict containing child nodes with parent as key
    distances = {source_point: 0} # dict containing distance from start to key node
    heuristic = {source_point: pythagorean(source_point[1]-destination_point[1], source_point[0]-destination_point[0])}
    # dict containing distance from start node to key node + Euclidean distance from key node to end node

    while len(queue) > 0:
        currentNode = heappop(queue) # take the node with least distance off the queue for examination

        if currentNode == destination_point: # if it's the node we're looking for, compute and return the path
            return form_path(parent, currentNode)

        evaluated.append(currentNode) # add the current node to the list of black nodes

        for adjacentNode in mesh['adj'][currentNode]: # looks at each node in adjacency list of current node
            
            if adjacentNode in evaluated: # if the node is black, ignore it
                continue

            else: # otherwise, try to calculate a better heuristic
                tempHeuristic = heuristic[currentNode] + pythagorean((currentNode[1]-adjacentNode[1]), (currentNode[0]-adjacentNode[0]))

                if not adjacentNode in queue: # node has been discovered
                    heappush(queue, adjacentNode)

                elif adjacentNode in heuristic.keys() and tempHeuristic >= heuristic[adjacentNode]: # the heuristic is not better
                    continue

            # record best path
            parent[adjacentNode] = currentNode
            heuristic[adjacentNode] = tempHeuristic
            distances[adjacentNode] = heuristic[adjacentNode] + pythagorean((adjacentNode[1]-destination_point[1]), (adjacentNode[0]-destination_point[0]))

"""
    # Print source and destination coordinates
    print("Source coordinates: ", source_point, "\n")
    print("Destination coordinates: ", destination_point, "\n")

    # Source Coordinates
    sx = source_point[1]
    sy = source_point[0]

    # Destination Coordinates
    dx = destination_point[1]
    dy = destination_point[0]

        # Iterate through mesh boxes and put them in the dictionary: boxes.
        # Prints out the source and destination box if found.

        # Currently sets all box values in the dictionary to None
    for box in mesh['boxes']:
        # Box x Coordinates
        x1 = box[2]
        x2 = box[3]

        # Box y Coordinates
        y1 = box[0]
        y2 = box[1]

        # Initialize all box values to their adjacency list
        boxes[box] = mesh['adj'][box]

        # Check if equal to source or destination box and append to path, then print out.
        if sx >= x1 and sx < x2:
            if sy >= y1 and sy < y2:
                print("Source Box: ", box, "\n")
        if dx >= x1 and dx < x2:
            if dy >= y1 and dy < y2:
                print("Destination Box: ", box, "\n")

    #print(boxes)
    #print(mesh)

    return path, boxes.keys()
"""

# uses Pythagorean Theorem to calculate straght-line dist between two Cartesian coordinates
def pythagorean (a, b):
    return sqrt((a*a)+(b*b))

# reconstructs path
def form_path(parent, currentNode):
    path = [currentNode]
    while currentNode in parent.keys():
        currentNode = parent[currentNode]
        path.append(currentNode)
    return path