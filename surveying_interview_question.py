""" Main module for surveying solution.
Calls each separate solution and summarizes results and performance """

import time
import argparse
import sys
import pandas as pd

from build_grid import build_grid
from display import display_set_as_grid
from methods import igraph_method, recursive_method, networkx_method
from methods import stack_method, stack_method_deque, graphtool_method

methods = [recursive_method,
           networkx_method,
           igraph_method,
           graphtool_method,
           stack_method,
           stack_method_deque]
grid_sizes = [10, 50, 100, 500, 1000, 5000, 10000]
location_probabilities = [0.99, 0.95, 0.9, 0.85, 0.8, 0.75, 0.7]

sys.setrecursionlimit(1000000)

def main(grid_size, location_probability = None, print_results = True):
    """ Main module for surveying solution.
    grid_size: One-dimensional size of the grid to be used for evaluation """

    grid = build_grid(grid_size, location_probability, seed=0)
    if print_results:
        display_set_as_grid(grid_size, grid)
    print(f"Populated fraction: {len(grid)/(grid_size*grid_size)}")

    time_taken = dict()

    wells = int()

    for method in methods:
        start = time.perf_counter()
        wells = method.find_reservoirs(grid.copy())
        stop = time.perf_counter()
        time_taken[method.METHOD_NAME] = stop - start

        if print_results:
            number_of_wells_needed = len(wells)
            print(f"{method.METHOD_NAME.ljust(20)}"
                  f"{number_of_wells_needed} wells needed")

            if number_of_wells_needed < 10:
                for reservoir in wells:
                    reservoir = list(reservoir)
                    reservoir.sort()
                    print("Well size = {0}, locations: {1}".format(len(reservoir),
                                                                   "; ".join(map(str, reservoir))))

        average_well_size = sum([len(well) for well in wells])/len(wells) if len(wells) != 0 else 0
        print(f"Average well size: {average_well_size}")
        wells = len(wells)


    if print_results:
        time_taken_sorted = sorted(time_taken.items(), key=lambda item: item[1])
        for idx, (method_name, duration) in enumerate(time_taken_sorted):
            if idx == 0:
                shortest_time = duration
                shortest_method = method_name
                print(f"{1}: "
                      f"{shortest_method.ljust(20)}"
                      f"Time taken: {shortest_time:.3E} s")
            else:
                print(f"{idx+1}: "
                      f"{method_name.ljust(20)}"
                      f"Time taken: {duration:.3E} s, "
                      f"{duration / shortest_time:.2f} times slower than {shortest_method}")

    return time_taken, len(grid), wells, average_well_size


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Implement the surveying interview question")
    parser.add_argument('--grid_size',
                        type=int,
                        help='Size of the grid to be generated',
                        default=50)
    args = parser.parse_args()

    df = pd.DataFrame()

    for grid_size in grid_sizes:
        for location_probability in location_probabilities:
            print(f"Grid size: {grid_size}, Probability: {location_probability}")
            results,number_of_sites, number_of_wells, average_well_size = \
                main(grid_size, location_probability, True)

            row_dict = {"Grid Size": grid_size,
                             "Probability": location_probability}
            row_dict.update(results)
            row_dict.update({"Number of Sites": number_of_sites})
            row_dict.update({"Number of Wells": number_of_wells})
            row = pd.Series(row_dict)
            df = df.append(row, ignore_index=True)

    df = df.astype({"Grid Size": 'int32', "Number of Sites": 'int32', "Number of Wells": 'int32'})
    df.set_index(['Grid Size', 'Probability'], inplace=True)

    df.to_pickle('results/results_all_methods_sparse.pkl')
