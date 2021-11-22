""" A recursive implementation of the surveying problem
find_reservoirs: Determine the number and location of contiguous reservoirs in a grid
get_neighbors: Find the number of active neighbor elements for a given element
"""
from collections import deque

from tools import get_neighbors

METHOD_NAME = "Stack Method (deque)"


def find_reservoirs(this_grid) -> list[set[tuple[int, int]]]:
    """Recursively determines how many wells are needed, making the assumption that
    only one well is needed per contiguous field

    this_grid: This is the list of locations to be checked for the current reservoir
    reservoir: If being called recursively, this contains the current reservoir that is being built
    original_grid: If being called recursively, this is the full grid to find neighbor elements
    """

    # well is None iff this is the 'outer' call of this function

    checked_elements = set()
    stack = deque()
    reservoirs = []

    remaining_nodes = this_grid

    while remaining_nodes:
        reservoir = set()
        stack.append(remaining_nodes.pop())

        while stack:
            location = stack.pop()

            if location in checked_elements:
                continue

            reservoir.add(location)
            checked_elements.add(location)

            stack.extend(get_neighbors(location, this_grid))

        reservoirs.append(reservoir)
        remaining_nodes -= reservoir

    return reservoirs
