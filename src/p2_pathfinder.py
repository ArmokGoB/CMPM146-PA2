from p1 import dijkstras_shortest_path, navigation_edges
from heapq import heappop, heappush
from math import inf, sqrt

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

    path = []
    boxes = {}

    # Print source and destination coordinates
    print("Source coordinates: ", source_point, "\n")
    print("Destination coordinates: ", destination_point, "\n")

    points, boxes = dijkstras_shortest_path(source_point, destination_point, mesh)
    
    for i in range(len(points) - 1):
        print(points[i], points[i+1])
        path.append((points[i], points[i + 1]))

    print(path)

    return path, boxes.keys()

""" Finds the box accociated with a point
"""
def find_box(point, boxes, visited):
    for box in boxes:
        #print(point)
        #print(box)
        if point[1] >= box[2] and point[1] <= box[3]:
            if point[0] >= box[0] and point[0] <= box[1]:
                if box != visited:
                    #print("found")
                    return box
    print("none found")
    return None

def dijkstras_shortest_path(initial_position, destination, mesh):
    """ Searches for a minimal cost path through a graph using BFS algorithm.

    Args:
        initial_position: The initial box from which the path extends.
        destination: The end location for the path.
        adj: An adjacency dictionary containing boxes adjacent to a given box.

    Returns:
        If a path exits, return a list containing all cells from initial_position to destination.
        Otherwise, return None.

    """
    # The priority queue
    queue = [(0, initial_position)]

    # The dictionary that will be returned with the costs
    distances = {initial_position: 0}

    # The dictionary holding the boxes we've traversed
    boxes = {}

    # The dictionary holding the heuristic
    heuristic = {initial_position: pythagorean(initial_position[1] - destination[1], initial_position[0] - destination[0])}

    # The dictionary holding backpointers
    backpointers = {initial_position: None}

    current_box = None

    destination_node = find_box(destination, mesh['boxes'], current_box)

    while queue:
        print("queue: ", queue)
        current_dist, current_point = heappop(queue)
        current_dist = distances[current_point]
        #print(current_point)
        #print(current_dist)
        current_node = find_box(current_point, mesh['boxes'], current_box)
        #print(current_node)

        boxes[current_node] = mesh['adj'][current_node]

        if current_node == destination_node:
            pathcost = current_dist + pythagorean(current_point[1] - destination[1], current_point[0] - destination[0])
            distances[destination] = pathcost
            heuristic[destination] = 0
            backpointers[destination] = current_point

            current_point = destination

            # List containing all cells from initial_position to destination
            path = [current_point]

            # Go backwards from destination until the source using backpointers
            # and add all the nodes in the shortest path into a list
            current_back_point = backpointers[current_point]
            while current_back_point is not None:
                path.append(current_back_point)
                current_back_point = backpointers[current_back_point]

            return path[::-1], boxes

        # Calculate cost from current note to all the adjacent ones
        for adj_node, adj_node_cost in navigation_edges(boxes[current_node], current_point):
            pathcost = current_dist + adj_node_cost

            # If the cost is new
            if adj_node not in distances or pathcost < distances[adj_node]:
                distances[adj_node] = pathcost
                heuristic[adj_node] = pathcost + pythagorean(adj_node[1] - destination[1], adj_node[0] - destination[0])
                backpointers[adj_node] = current_point
                heappush(queue, (heuristic[adj_node], adj_node))
                current_box = current_node

    return None

def navigation_edges(level, cell):
    """ Provides a list of adjacent cells and their respective costs from the given cell.

    Args:
        level: A list of adjacent cells to the current cell
        cell: A target location.

    Returns:
        A list of tuples containing an adjacent cell's coordinates and the cost of the edge joining it and the
        originating cell.

        E.g. from (0,0):
            [((0,1), 1),
             ((1,0), 1),
             ((1,1), 1.4142135623730951),
             ... ]
    """

    detail_points = {}

    for box in level:
        #print(box)
        y1, y2, x1, x2 = box

        if cell[0] >= y1 and cell[0] <= y2:
            if cell[1] < x1:
                detail_points[cell[0], x1] = pythagorean(cell[1] - x1, 0)
            elif cell[1] > x2:
                detail_points[cell[0], x2] = pythagorean(cell[1] - x2, 0)

        elif cell[1] >= x1 and cell[1] <= x2:
            if cell[0] < y1:
                detail_points[y1, cell[1]] = pythagorean(0, cell[0] - y1)
            elif cell[0] > y2:
                detail_points[y2, cell[1]] = pythagorean(0, cell[0] - y2)

        else:
            temp_heap = []
            for x in (x1, x2):
                for y in (y1, y2):

                    next_point = x, y
                    heappush(temp_heap, (pythagorean(cell[1] - x, cell[0] - y), (y, x)))

            #print("temp heap: ", temp_heap)
            cost, new_point = heappop(temp_heap)
            detail_points[new_point] = cost

        #print(detail_points.items())

    return detail_points.items()

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