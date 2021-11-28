""" Main module for surveying solution.
Calls each separate solution and summarizes results and performance """

import time
import sys
import pandas as pd
import pyjion
from itertools import product
from typing import Type, TYPE_CHECKING

from orchestrator import GridOrchestrator

if TYPE_CHECKING:
    from view import GridView

sys.setrecursionlimit(1000000)


class DesignOfExperiments:
    def __init__(
        self,
        grid_sizes: list[int],
        location_probabilities: list[float],
        model_types: list,
        pyjion_state: list[bool],
    ):

        self.grid_sizes = grid_sizes
        self.location_probabilities = location_probabilities
        self.model_types = model_types
        self.pyjion_state = pyjion_state

    def run(self) -> pd.DataFrame:
        results = []

        for grid_size, location_probability, model_type, pyjion_state in product(
            self.grid_sizes,
            self.location_probabilities,
            self.model_types,
            self.pyjion_state,
        ):
            print("*" * 30)
            print(
                f"Grid size: {grid_size}, Probability: {location_probability}, "
                f"Model Type: {model_type}, Pyjion: {pyjion_state}"
            )
            self._set_pyjion(pyjion_state)
            grid = GridOrchestrator.get_grid_view_with_parameters(
                grid_size=grid_size,
                location_probability=location_probability,
                model_type=model_type,
            )
            row_dict = self._run_method(grid, model_type)
            results.append(row_dict)
        return pd.DataFrame(results)

    @staticmethod
    def _set_pyjion(pyjion_state: bool):
        if pyjion_state:
            pyjion.enable()
            pyjion.config(pgc=False)
        else:
            pyjion.disable()

    @staticmethod
    def _run_method(grid: "GridView", model_type: Type) -> dict[str, int | float | str]:
        print(f"-" * 20)
        print(f"Method: {grid}")
        sim_run = SimulationRun(grid)
        sim_run.execute()
        sim_run.print_grid()
        sim_run.print_results()
        row_dict = {
            "Grid Size": grid.size,
            "Probability": grid.location_probability,
            "Number of Sites": grid.number_of_sites,
            "Method": model_type,
            "Number of Wells": sim_run.number_of_wells,
            "Time": sim_run.time_to_run,
        }
        return row_dict


class SimulationRun:
    def __init__(self, grid: "GridView"):
        self.grid = grid
        self.wells = None
        self._time_taken = None

    @property
    def number_of_wells(self) -> int | None:
        if self.wells is None:
            return None
        return len(self.wells)

    @property
    def time_to_run(self) -> float:
        return self._time_taken

    @property
    def average_well_size(self) -> float | None:
        if self.number_of_wells is None:
            return None
        if self.number_of_wells == 0:
            return 0
        return sum([len(well) for well in self.wells]) / self.number_of_wells

    def execute(self):
        """Main module for surveying solution.
        grid_size: One-dimensional size of the grid to be used for evaluation"""

        start = time.perf_counter()
        self.wells = self.grid.get_reservoirs()
        stop = time.perf_counter()
        self._time_taken = stop - start

    def print_grid(self):
        result = self.grid.to_ascii_art()
        print(result)

    def print_results(self):
        if self.wells is None:
            return

        print("Results...")
        if self.number_of_wells < 10:
            self._print_reservoir_details()
        print(f"Average well size: {self.average_well_size}")
        print(f"Number of wells needed: {self.number_of_wells}")
        print(f"Time to run: {self.time_to_run}")

    def _print_reservoir_details(self):
        if self.number_of_wells < 10:
            for reservoir in self.wells:
                reservoir = list(reservoir)
                reservoir.sort()
                reservoir_locations = "; ".join(map(str, reservoir))
                print(f"Well size = {len(reservoir)}, locations: {reservoir_locations}")
