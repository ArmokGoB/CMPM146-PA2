from p1 import dijkstras_shortest_path, navigation_edges

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
        if dx >= x1 and dx < x2:
            if dy >= y1 and dy < y2:
                print("Destination Box: ", box, "\n")

    #print(boxes)
    #print(mesh)

    return path, boxes.keys()