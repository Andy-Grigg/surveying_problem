import copy

from methods import (
    igraph_method,
    recursive_method,
    networkx_method,
    stack_method,
    stack_method_deque,
)


def test_method_equality():
    grid = build_grid.Grid(100).to_set_of_tuples

    igraph_results = igraph_method.find_reservoirs(copy.deepcopy(grid))
    recursive_results = recursive_method.find_reservoirs(copy.deepcopy(grid))
    networkx_results = networkx_method.find_reservoirs(copy.deepcopy(grid))
    stack_results = stack_method.find_reservoirs(copy.deepcopy(grid))
    deque_results = stack_method_deque.find_reservoirs(copy.deepcopy(grid))
    # graphtool_results = graphtool_method.find_reservoirs(copy.deepcopy(grid))

    for well in igraph_results:
        assert well in igraph_results
        assert well in recursive_results
        assert well in networkx_results
        assert well in stack_results
        assert well in deque_results
        # assert well in graphtool_results

    assert (
        len(igraph_results)
        == len(recursive_results)
        == len(networkx_results)
        == len(stack_results)
        == len(deque_results)
        # == len(graphtool_results)
    )
