from p1 import dijkstras_shortest_path, navigation_edges
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

    path = []
    boxes = {}

    # Print source and destination coordinates
    print("Source coordinates: ", source_point, "\n")
    print("Destination coordinates: ", destination_point, "\n")

    # Source Coordinates
    sx = source_point[1]
    sy = source_point[0]

    # Destination Coordinates
    dx = destination_point[1]
    dy = destination_point[0]

    # Initialize source and destination boxes
    source_box = None
    destination_box = None

    """ Iterate through mesh boxes and put them in the dictionary: boxes.
        Prints out the source and destination box if found.
    """
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
                source_box = box
                #path.append(box)
        if dx >= x1 and dx < x2:
            if dy >= y1 and dy < y2:
                print("Destination Box: ", box, "\n")
                destination_box = box
                #path.append(box)

    #print(boxes)
    #print(mesh)

    path = breadth_first_search(source_box, destination_box, boxes)
    print(path)

    return path, boxes.keys()

def breadth_first_search(initial_position, destination, adj):
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
    queue = [initial_position]

    # The dictionary that will be returned with the costs
    visited = []
    visited.append(initial_position)

    # The dictionary that will store the backpointers
    backpointers = {}
    backpointers[initial_position] = None

    while queue:
        current_node = heappop(queue)

        # Check if current node is the destination
        if current_node == destination:

            # List containing all cells from initial_position to destination
            path = [current_node]

            # Go backwards from destination until the source using backpointers
            # and add all the nodes in the shortest path into a list
            current_back_node = backpointers[current_node]
            while current_back_node is not None:
                path.append(current_back_node)
                current_back_node = backpointers[current_back_node]

            return path[::-1]

        # Calculate cost from current note to all the adjacent ones
        for adj_node in adj[current_node]:
            #pathcost = current_dist + adj_node_cost

            # If the cost is new
            if adj_node not in visited:
                visited.append(adj_node)
                backpointers[adj_node] = current_node
                heappush(queue, adj_node)

    return None