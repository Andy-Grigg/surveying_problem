# content of test_sample.py
import pytest
import build_grid
import random
import lxml.etree as ET


def test_fully_populated_grid():
    my_grid = build_grid.Grid(10, 0).to_set_of_tuples
    assert len(my_grid) == 100


def test_empty_grid():
    my_grid = build_grid.Grid(10, 1).to_set_of_tuples
    assert len(my_grid) == 0


def test_seed():
    seed = random.random()
    my_grid_1 = build_grid.Grid(10, seed=seed).to_set_of_tuples
    my_grid_2 = build_grid.Grid(10, seed=seed).to_set_of_tuples
    assert my_grid_1 == my_grid_2


def test_seed_negative():
    my_grid_1 = build_grid.Grid(10).to_set_of_tuples
    my_grid_2 = build_grid.Grid(10).to_set_of_tuples
    assert my_grid_1 != my_grid_2


def test_xml_output():
    my_grid_xml = build_grid.Grid(10).to_xml
    assert isinstance(my_grid_xml, ET._Element)


def test_default_threshold():
    my_grid_1 = build_grid.Grid(10, seed=0).to_set_of_tuples
    my_grid_2 = build_grid.Grid(10, build_grid.THRESHOLD, seed=0).to_set_of_tuples
    assert my_grid_1 == my_grid_2
