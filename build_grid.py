""" Generate a grid of elements with a random layout of elements that contain oil
build_grid: Build the grid with an optional random seed
get_neighbors: Find the number of active neighbor elements for a given element
"""

import random
import itertools
import lxml.etree as ET

from tools import get_neighbors

THRESHOLD = 0.85


class Grid:
    def __init__(self, size, location_probability=THRESHOLD, seed=None):
        """Build a square grid of elements, where each element may or may not contain oil

        size: The number of elements along one edge of the grid
        seed: Random seed to be used to generate the grid
        """
        self.size = size
        self.location_probability = location_probability
        self.seed = seed
        random.seed(seed)

        if location_probability is None:
            location_probability = THRESHOLD

        initial_grid = set()
        for location in itertools.product(range(0, size), repeat=2):
            if random.random() > location_probability:
                initial_grid.add(location)

        self._grid = set()
        # Cluster the grid. If an active element is not isolated,
        # or if an inactive element has at least 4 active neighbors
        for location in itertools.product(range(0, size), repeat=2):
            state = location in initial_grid
            sites_nearby = get_neighbors(location, initial_grid)
            neighbor_count = len(sites_nearby)
            if (state and neighbor_count != 0) or neighbor_count >= 4:
                self._grid.add(location)

    @property
    def number_of_sites(self) -> int:
        return len(self._grid)

    @property
    def density(self) -> int:
        return self.number_of_sites / (self.size * self.size)

    @property
    def to_set_of_tuples(self) -> set[tuple[int, int]]:
        return self._grid

    @property
    def to_xml(self) -> ET.Element:
        root = ET.Element("grid")
        sortable_grid = list(self._grid)
        sortable_grid.sort()
        for location in sortable_grid:
            y_element = ET.Element("y")
            x_element = ET.Element("x")
            x_element.text, y_element.text = map(str, location)
            location_element = ET.Element("el")
            location_element.extend([x_element, y_element])
            root.append(location_element)
        return root


if __name__ == "__main__":
    grid = Grid(25).to_xml
    with open("../surveying_xslt/input.xml", "w") as f:
        f.write((ET.tostring(grid, pretty_print=True).decode()))
