# content of test_sample.py
import random
from src.model import THRESHOLD
from common import create_grid_with_cells, DummyModel


def test_fully_populated_grid():
    my_grid = DummyModel(10, 0).cells
    assert len(my_grid) == 100


def test_empty_grid():
    my_grid = DummyModel(10, 1).cells
    assert len(my_grid) == 0


def test_seed():
    seed = random.random()
    my_grid_1 = DummyModel(10, seed=seed).cells
    my_grid_2 = DummyModel(10, seed=seed).cells
    assert my_grid_1 == my_grid_2


def test_seed_negative():
    my_grid_1 = DummyModel(10).cells
    my_grid_2 = DummyModel(10).cells
    assert my_grid_1 != my_grid_2


# def test_xml_output():
#     my_grid_xml = DummyModel.Grid(10)
#     assert isinstance(my_grid_xml, ET._Element)


def test_default_threshold():
    my_grid_1 = DummyModel(10, seed=0).cells
    my_grid_2 = DummyModel(10, THRESHOLD, seed=0).cells
    assert my_grid_1 == my_grid_2

def test_no_neighbors():
    dummy = DummyModel(1, 1)
    neighbors = dummy.get_neighbors((1, 1))
    assert neighbors == []


def test_all_neighbors():
    grid = DummyModel(3, 0)
    neighbors = grid.get_neighbors((1, 1))
    assert set(neighbors) == grid.cells - {(1, 1)}


def test_diagonal_neighbors():
    cells = {(0, 0), (2, 0), (1, 1), (0, 2), (2, 2)}
    grid = create_grid_with_cells(cells)
    neighbors = grid.get_neighbors((1, 1))

    assert set(neighbors) == grid.cells - {(1, 1)}
