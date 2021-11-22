""" A networkx implementation of the surveying problem
find_reservoirs: Determine the number and location of contiguous reservoirs in a grid
"""

import time
import networkx as nx

from tools import get_neighbors

METHOD_NAME = "NetworkX Method"


def find_reservoirs(grid) -> list[set[tuple[int, int]]]:
    """Uses a graph approach to find how many wells are needed, making the assumption that
    only one well is needed per contiguous field

    locations: Set containing all locations with oil
    """

    start = time.perf_counter()
    locations_graph = nx.Graph()
    locations_graph.add_nodes_from(grid)

    edges_to_create = set()
    for node in locations_graph:
        neighbors = get_neighbors(node, locations_graph)
        _ = [edges_to_create.add((node, neighbor)) for neighbor in neighbors]

    locations_graph.add_edges_from(edges_to_create)

    mid = time.perf_counter()
    connected_subgraphs = nx.connected_components(locations_graph)
    wells = list(connected_subgraphs)
    end = time.perf_counter()
    print(f"Build: {mid-start:.3E} s")
    print(f"{(mid - start)/(end-start)*100:.2f}% of total")
    print(f"Solve: {end-mid:.3E} s")
    print(f"{(end - mid) / (end - start) * 100:.2f}% of total")
    return wells
