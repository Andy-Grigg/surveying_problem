import argparse

from src.model import (
    NetworkXMethod,
    DequeMethod,
    StackMethod,
    IGraphMethod,
    RecursiveMethod,
)
from doe import DesignOfExperiments


parser = argparse.ArgumentParser(
    description="Implement the surveying interview question"
)
parser.add_argument(
    "--grid_size", type=int, help="Size of the grid to be generated", default=50
)
args = parser.parse_args()

doe = DesignOfExperiments(
    grid_sizes=[
        10,
        50,
        # 100,
        # 500,
        # 1000,
        # 5000,
        # 10000,
    ],
    location_probabilities=[
        0.99,
        0.95,
        0.9,
        # 0.85,
        # 0.8,
        # 0.75,
        # 0.7,
    ],
    model_types=[
        NetworkXMethod,
        DequeMethod,
        RecursiveMethod,
        StackMethod,
        IGraphMethod,
    ],
    pyjion_state=[True, False],
)

df = doe.run()

# time_taken_sorted = sorted(time_taken.items(), key=lambda item: item[1])
# for idx, (method_name, duration) in enumerate(time_taken_sorted):
#     if idx == 0:
#         shortest_time = duration
#         shortest_method = method_name
#         print(
#             f"{1}: "
#             f"{shortest_method.ljust(20)}"
#             f"Time taken: {shortest_time:.3E} s"
#         )
#     else:
#         print(
#             f"{idx + 1}: "
#             f"{method_name.ljust(20)}"
#             f"Time taken: {duration:.3E} s, "
#             f"{duration / shortest_time:.2f} times slower than {shortest_method}"
#         )
# df = df.astype(
#     {"Grid Size": "int32", "Number of Sites": "int32", "Number of Wells": "int32"}
# )
# df.set_index(["Grid Size", "Probability"], inplace=True)
# df.to_pickle('results/results_all_methods_sparse.pkl')
