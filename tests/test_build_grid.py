# content of test_sample.py
import pytest
import build_grid
import random
import lxml.etree as ET

def test_fully_populated_grid():
    my_grid = build_grid.build_grid(10, 0)
    assert len(my_grid) == 100

def test_empty_grid():
    my_grid = build_grid.build_grid(10, 1)
    assert len(my_grid) == 0

def test_seed():
    seed = random.random()
    my_grid_1 = build_grid.build_grid(10, seed=seed)
    my_grid_2 = build_grid.build_grid(10, seed=seed)
    assert my_grid_1 == my_grid_2

def test_seed_negative():
    my_grid_1 = build_grid.build_grid(10)
    my_grid_2 = build_grid.build_grid(10)
    assert my_grid_1 != my_grid_2

def test_xml_output():
    my_grid_xml = build_grid.build_grid(10, output_format=ET._Element)
    assert isinstance(my_grid_xml, ET._Element)

def test_unsupported_output():
    with pytest.raises(NotImplementedError):
        _ = build_grid.build_grid(10, output_format=str)

def test_default_threshold():
    my_grid_1 = build_grid.build_grid(10, seed=0)
    my_grid_2 = build_grid.build_grid(10, build_grid.THRESHOLD, seed=0)
    assert my_grid_1 == my_grid_2
