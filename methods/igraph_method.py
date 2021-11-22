""" An igraph-python implementation of the surveying problem
find_reservoirs: Determine the number and location of contiguous reservoirs in a grid
"""

import igraph

from tools import get_neighbors

METHOD_NAME = "IGraph Method"


def find_reservoirs(locations) -> list[set[tuple[int, int]]]:
    """Uses a graph approach to find how many wells are needed, making the assumption that
    only one well is needed per contiguous field

    locations: Set containing all locations with oil
    """

    locations_igraph = igraph.Graph()
    locations_str = [",".join(map(str, location)) for location in locations]
    locations_igraph.add_vertices(locations_str)

    edge_list = set()
    for coords in locations:
        neighbor_coords = get_neighbors(coords, locations)
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
