""" A graph-tools implementation of the surveying problem
find_reservoirs: Determine the number and location of contiguous reservoirs in a grid
"""

import graph_tool as gt
import graph_tool.topology as topology

from tools import get_neighbors

METHOD_NAME = "Graph-Tool Method"


def find_reservoirs(locations):
    """ Uses a graph approach to find how many wells are needed, making the assumption that
    only one well is needed per contiguous field

    locations: Set containing all locations with oil
    """

    locations = {location: idx for idx, location in enumerate(locations)}

    locations_graph = gt.Graph()
    locations_graph.set_directed(False)

    locations_graph.add_vertex(len(locations))
    locations_prop = locations_graph.new_vertex_property("object", locations)

    edge_list = []
    for location in locations:
        neighbor_coords = get_neighbors(location, locations)
        edge_list.extend([(locations[location], locations[neighbor])
                          for neighbor in neighbor_coords])

    locations_graph.add_edge_list(edge_list)

    components, _ = topology.label_components(locations_graph, directed=False)
    wells = dict()
    for vertex, label in enumerate(components.a):
        if label not in wells:
            wells[label] = []
        wells[label].append(locations_prop[vertex])

    return [set(well) for well in wells.values()]
