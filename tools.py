def get_neighbors(this_element, grid):
    """Returns a list of neighbor location objects

    this_element: A 2-tuple representing the x and y coordinates of an element
    grid: A dictionary containing all elements and their state
    """
    x_coord, y_coord = this_element
    x_offsets = [-1, 0, 1]
    y_offsets = [-1, 0, 1]

    neighbors = list()
    for x_offset in x_offsets:
        for y_offset in y_offsets:
            if x_offset == 0 and y_offset == 0:
                continue

            coord = (x_coord + x_offset, y_coord + y_offset)
            if coord in grid:
                neighbors.append(coord)
    return neighbors
