""" Generate a grid of elements with a random layout of elements that contain oil
build_grid: Build the grid with an optional random seed
get_neighbors: Find the number of active neighbor elements for a given element
"""

import random
import itertools
from abc import ABC, abstractmethod
import time

THRESHOLD = 0.85

Cell = tuple[int, int]


class GridModel(ABC):
    def __init__(
        self, size: int, location_probability: float = THRESHOLD, seed: float = None
    ):
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
        self._grid = set()
        for location in itertools.product(range(0, size), repeat=2):
            if random.random() > location_probability:
                self._grid.add(location)
        self._grid = self._cluster()

    def _cluster(self) -> set[Cell]:
        """Cluster the grid. If an active element is not isolated or if an inactive element has at least 4 active
        neighbors. Kind of Game of Life-esque"""

        clustered_grid = set()
        for location in itertools.product(range(0, self.size), repeat=2):
            state = location in self._grid
            sites_nearby = self.get_neighbors(location)
            neighbor_count = len(sites_nearby)
            if (state and neighbor_count != 0) or neighbor_count >= 4:
                clustered_grid.add(location)
        return clustered_grid

    @property
    def cells(self) -> set[Cell]:
        return self._grid

    def get_neighbors(self, grid_element) -> list[Cell]:
        """Returns a list of neighbor location objects

        this_element: A 2-tuple representing the x and y coordinates of an element
        grid: A dictionary containing all elements and their state
        """
        x_coord, y_coord = grid_element
        x_offsets = [-1, 0, 1]
        y_offsets = [-1, 0, 1]

        neighbors = list()
        for x_offset in x_offsets:
            for y_offset in y_offsets:
                if x_offset == 0 and y_offset == 0:
                    continue
                coord = (x_coord + x_offset, y_coord + y_offset)
                if coord in self.cells:
                    neighbors.append(coord)
        return neighbors

    @abstractmethod
    def find_reservoirs(self) -> list[set[Cell]]:
        pass


class NetworkXMethod(GridModel):
    def find_reservoirs(self) -> list[set[Cell]]:
        """Uses a graph approach to find how many wells are needed, making the assumption that
        only one well is needed per contiguous field

        locations: Set containing all locations with oil
        """

        import networkx as nx

        start = time.perf_counter()
        locations_graph = nx.Graph()
        locations_graph.add_nodes_from(self.cells)

        edges_to_create = set()
        for node in locations_graph:
            neighbors = self.get_neighbors(node)
            _ = [edges_to_create.add((node, neighbor)) for neighbor in neighbors]

        locations_graph.add_edges_from(edges_to_create)

        mid = time.perf_counter()
        connected_subgraphs = nx.connected_components(locations_graph)
        reservoirs = list(connected_subgraphs)
        end = time.perf_counter()
        print(f"Build: {mid - start:.3E} s")
        print(f"{(mid - start) / (end - start) * 100:.2f}% of total")
        print(f"Solve: {end - mid:.3E} s")
        print(f"{(end - mid) / (end - start) * 100:.2f}% of total")
        return reservoirs

    def __str__(self):
        return "NetworkX Method"


class DequeMethod(GridModel):
    def find_reservoirs(self) -> list[set[Cell]]:
        """Recursively determines how many wells are needed, making the assumption that
        only one well is needed per contiguous field
        """

        from collections import deque

        checked_elements = set()
        stack = deque()
        reservoirs = []
        remaining_nodes = self.cells
        while remaining_nodes:
            reservoir = set()
            stack.append(remaining_nodes.pop())
            while stack:
                location = stack.pop()
                if location in checked_elements:
                    continue
                reservoir.add(location)
                checked_elements.add(location)
                stack.extend(self.get_neighbors(location))
            reservoirs.append(reservoir)
            remaining_nodes -= reservoir
        return reservoirs

    def __str__(self):
        return "Deque Method"


class IGraphMethod(GridModel):
    def find_reservoirs(self) -> list[set[Cell]]:
        """Uses a graph approach to find how many wells are needed, making the assumption that
        only one well is needed per contiguous field

        locations: Set containing all locations with oil
        """

        import igraph

        locations_igraph = igraph.Graph()
        locations_str = [",".join(map(str, location)) for location in self.cells]
        locations_igraph.add_vertices(locations_str)

        edge_list = set()
        for coords in self.cells:
            neighbor_coords = self.get_neighbors(coords)
            edge_list.update(
                {
                    (",".join(map(str, coords)), ",".join(map(str, neighbor_coord)))
                    for neighbor_coord in neighbor_coords
                }
            )
        locations_igraph.add_edges(edge_list)
        clusters = locations_igraph.clusters(mode="STRONG")
        wells = [
            {
                locations_igraph.vs[vertex]["name"] for vertex in cluster
            }  # pylint: disable=E1136
            for cluster in clusters
        ]
        return [
            {tuple(int(value) for value in site.split(",")) for site in igraph_result}
            for igraph_result in wells
        ]


class RecursiveMethod(GridModel):
    checked_elements = None

    def find_reservoirs(self) -> list[set[Cell]]:
        self.checked_elements = set()
        return self._find_reservoirs_recursive(self.cells)

    def _find_reservoirs_recursive(
        self, this_grid, reservoir=None, original_grid=None
    ) -> list[set[Cell]]:
        """Recursively determines how many wells are needed, making the assumption that
        only one well is needed per contiguous field

        this_grid: This is the list of locations to be checked for the current reservoir
        reservoir: If being called recursively, this contains the current reservoir that is being built
        original_grid: If being called recursively, this is the full grid to find neighbor elements
        """

        # well is None iff this is the 'outer' call of this function
        if reservoir is None:
            recursing = False
            reservoir = set()
            reservoirs = []
            original_grid = this_grid.copy()
        else:
            recursing = True
            reservoirs = None

        for element in this_grid:
            if element in self.checked_elements:
                continue

            self.checked_elements.add(element)

            # Add this location to the active well
            reservoir.add(element)

            neighbors = self.get_neighbors(element)
            if len(neighbors) != 0:
                self._find_reservoirs_recursive(neighbors, reservoir, original_grid)

            # Only add the well to the return object if we are in the outer layer
            if not recursing:
                reservoirs.append(reservoir)
                reservoir = set()

        return reservoirs


class StackMethod(GridModel):
    def find_reservoirs(self) -> list[set[Cell]]:
        """Recursively determines how many wells are needed, making the assumption that
        only one well is needed per contiguous field

        this_grid: This is the list of locations to be checked for the current reservoir
        reservoir: If being called recursively, this contains the current reservoir that is being built
        original_grid: If being called recursively, this is the full grid to find neighbor elements
        """

        # well is None iff this is the 'outer' call of this function

        checked_elements = set()
        stack = list()
        reservoirs = []

        remaining_nodes = self.cells

        while remaining_nodes:
            reservoir = set()
            stack.append(remaining_nodes.pop())

            while stack:
                location = stack.pop()

                if location in checked_elements:
                    continue

                reservoir.add(location)
                checked_elements.add(location)

                stack.extend(self.get_neighbors(location))

            reservoirs.append(reservoir)
            remaining_nodes -= reservoir

        return reservoirs


class GraphToolMethod(GridModel):
    def find_reservoirs(self) -> list[set[Cell]]:
        """Uses a graph approach to find how many wells are needed, making the assumption that
        only one well is needed per contiguous field

        locations: Set containing all locations with oil
        """

        raise NotImplementedError
        import graph_tool as gt
        import graph_tool.topology as topology

        locations = {location: idx for idx, location in enumerate(self.cells)}

        locations_graph = gt.Graph()
        locations_graph.set_directed(False)

        locations_graph.add_vertex(len(locations))
        locations_prop = locations_graph.new_vertex_property("object", locations)

        edge_list = []
        for location in locations:
            neighbor_coords = self.get_neighbors(location)
            edge_list.extend(
                [
                    (locations[location], locations[neighbor])
                    for neighbor in neighbor_coords
                ]
            )

        locations_graph.add_edge_list(edge_list)

        components, _ = topology.label_components(locations_graph, directed=False)
        wells = dict()
        for vertex, label in enumerate(components.a):
            if label not in wells:
                wells[label] = []
            wells[label].append(locations_prop[vertex])

        return [set(well) for well in wells.values()]
