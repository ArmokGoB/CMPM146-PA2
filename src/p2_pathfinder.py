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

    #print(mesh['adj'])
    #print(source_point)

    # Pseudocode found at: https://en.wikipedia.org/wiki/A*_search_algorithm (10/12/18)

    source_box = find_box(source_point, mesh['boxes'])
    destination_box = find_box(destination_point, mesh['boxes'])

    boxes = {}
    evaluated = [] # set of black nodes
    queue = [(0, source_point, source_box)] # priority queue of nodes to look at
    parent = {} # dict containing child nodes with parent as key
    distances = {source_point: 0} # dict containing distance from start to key node
    heuristic = {source_point: pythagorean(source_point[1]-destination_point[1], source_point[0]-destination_point[0])}
    # dict containing distance from start node to key node + Euclidean distance from key node to end node

    while queue:
        temp_heurstic, currentNode, current_box = heappop(queue) # take the node with least distance off the queue for examination

        boxes[current_box] = mesh['adj'][current_box]

        if current_box == destination_box: # if it's the node we're looking for, compute and return the path
            pathcost = distances[currentNode] + pythagorean(currentNode[1] - destination_point[1], currentNode[0] - destination_point[0])
            distances[destination_point] = pathcost
            heuristic[destination_point] = 0
            parent[destination_point] = currentNode

            currentNode = destination_point

            point_path = form_path(parent, currentNode)

            path = segment_path(point_path)

            return path, boxes.keys()


        evaluated.append(current_box) # add the current node to the list of black nodes

        print(mesh['adj'][current_box])

        for adj_box in mesh['adj'][current_box]: # looks at each node in adjacency list of current node

            if adj_box in evaluated: # if the node is black, ignore it
                continue

            detail_list = find_detail_points(adj_box, currentNode)

            adj_cost, adjacentNode = find_least_cost(detail_list, currentNode)

            # otherwise, try to calculate a better heuristic
            temp_distance = distances[currentNode] + adj_cost

            new_heuristic = temp_distance + pythagorean(adjacentNode[1] - destination_point[1], adjacentNode[0] - destination_point[0])

            if adjacentNode not in distances: # node has been discovered
                    #print(new_heuristic)
                heappush(queue, (new_heuristic, adjacentNode, adj_box))

            elif temp_distance >= distances[adjacentNode]: # the heuristic is not better
                continue

            # record best path
            parent[adjacentNode] = currentNode
            distances[adjacentNode] = temp_distance
            heuristic[adjacentNode] = distances[adjacentNode] + adj_cost
            #pythagorean(adjacentNode[1] - destination_point[1], adjacentNode[0] - destination_point[0])

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

def find_detail_points(box, point):
    #print("box: ", box)
    detail_points = []
    y1, y2, x1, x2 = box

    if point[0] >= y1 and point[0] <= y2:
        if point[1] < x1:
            detail_points.append((point[0], x1))
        elif point[1] > x2:
            detail_points.append((point[0], x2))

    elif point[1] >= x1 and point[1] <= x2:
        if point[0] < y1:
            detail_points.append((y1, point[1]))
        elif point[0] > y2:
            detail_points.append((y2, point[1]))
            
    for y in (y1, y2):
        for x in (x1, x2):
            detail_points.append((y, x))

    return detail_points

def find_least_cost(detail_points, point):
    temp_heap = []

    for box_point in detail_points:
        heappush(temp_heap, (pythagorean(box_point[1] - point[1], box_point[0] - point[0]), box_point))

    return heappop(temp_heap)


def find_box(point, box_list):
    for box in box_list:
        if point[0] >= box[0] and point[0] <= box[1]:
            if point[1] >= box[2] and point[1] <= box[3]:
                return box

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

def segment_path(points):
    path = []
    for i in range(len(points) - 1, 0, -1):
        #print(points[len(points) - 1], points[len(points) - i - 2])
        path.append((points[i], points[i - 1]))

    return path