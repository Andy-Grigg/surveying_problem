""" A recursive implementation of the surveying problem
find_reservoirs: Determine the number and location of contiguous reservoirs in a grid
get_neighbors: Find the number of active neighbor elements for a given element
"""

from tools import get_neighbors

METHOD_NAME = "Recursive Method"
REQUIRED_GRID_TYPE = (int, int)


def find_reservoirs(this_grid, reservoir=None, original_grid=None):
    """ Recursively determines how many wells are needed, making the assumption that
    only one well is needed per contiguous field

    this_grid: This is the list of locations to be checked for the current reservoir
    reservoir: If being called recursively, this contains the current reservoir that is being built
    original_grid: If being called recursively, this is the full grid to find neighbor elements
    """



    # well is None iff this is the 'outer' call of this function
    if reservoir is None:
        # Initialize variables
        global checked_elements
        checked_elements = set()

        recursing = False
        reservoir = set()
        reservoirs = []
        original_grid = this_grid.copy()
    else:
        recursing = True
        reservoirs = None

    for element in this_grid:
        if element in checked_elements:
            continue

        checked_elements.add(element)

        # Add this location to the active well
        reservoir.add(element)

        neighbors = get_neighbors(element, original_grid)
        if len(neighbors) != 0:
            find_reservoirs(neighbors, reservoir, original_grid)

        # Only add the well to the return object if we are in the outer layer
        if not recursing:
            reservoirs.append(reservoir)
            reservoir = set()

    return reservoirs
