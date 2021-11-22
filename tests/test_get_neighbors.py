import pytest

from tools import get_neighbors
import build_grid


def test_no_neighbors():
    grid = {(1, 1)}
    neighbors = get_neighbors((1, 1), grid)

    assert neighbors == []


def test_all_neighbors():
    grid = build_grid.Grid(3, 0).to_set_of_tuples
    neighbors = get_neighbors((1, 1), grid)

    assert set(neighbors) == grid - {(1, 1)}


def test_diagonal_neighbors():
    grid = {(0, 0), (2, 0), (1, 1), (0, 2), (2, 2)}
    neighbors = get_neighbors((1, 1), grid)

    assert set(neighbors) == grid - {(1, 1)}
