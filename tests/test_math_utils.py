import pytest

from src.math_utils import divide, percentage, moving_average


def test_divide_basic():
    assert divide(6, 3) == 2


def test_percentage_basic():
    assert percentage(1, 4) == 25.0


def test_moving_average_basic():
    assert moving_average([1, 2, 3, 4], 2) == [1.5, 2.5, 3.5]