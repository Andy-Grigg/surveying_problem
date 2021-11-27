from src.model import GridModel, Cell


class DummyModel(GridModel):
    def find_reservoirs(self) -> list[set[Cell]]:
        pass


def create_grid_with_cells(cells: set[Cell]) -> DummyModel:
    dummy = DummyModel(1, 1)
    dummy._grid = cells
    return dummy
