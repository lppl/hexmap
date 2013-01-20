import pytest

from hexmap.grid import is_point, distance, in_distance
from hexmap.grid import num_points_in_circle, num_points_in_distance
from hexmap.grid import points_in_circle, points_in_distance
from hexmap.grid import move_point, NotRecognizedMoveError



def test_is_point():
    assert is_point((1, 2))
    assert is_point((-1, 2))
    assert not is_point((1.0, 2))
    assert not is_point((1, 2.0))
    assert not is_point((1,'2'))
    assert not is_point(('1',2))
    assert not is_point({0:1, 1:3})
    assert not is_point([])

def test_distance(distances):
    for a, b, d in distances:
        assert distance(a, a) == 0
        assert distance(a, b) == d
        assert distance(b, a) == d

def test_in_distance(distances):
    for a, b, d in distances:
        assert in_distance(a, a, 0)
        assert in_distance(a, b, d)
        assert in_distance(b, a, d)
        assert in_distance(a, b, d + 1)
        assert in_distance(b, a, d + 1)
        assert not in_distance(a, b, d - 1)
        assert not in_distance(b, a, d - 1)

def test_num_points_in_circle(circles):
    for i, c in enumerate(circles):
        assert len(c) == num_points_in_circle(i)


def test_num_points_in_distance(hexagons):
    for i, c in enumerate(hexagons):
        assert len(c) == num_points_in_distance(i)


def test_points_in_circle(circles, points):
    for i, c in enumerate(circles):
        assert c == points_in_circle(points["CENTER"], i)

def test_points_in_distance(hexagons, points):
    for i, c in enumerate(hexagons):
        assert c == points_in_distance(points["CENTER"], i)

def test_moves():
    assert (-1, 0) == move_point((-2,-1), 0, 1)
    assert (-1,-1) == move_point((-2,-1), 1, 1)
    assert (-2,-2) == move_point((-2,-1), 2, 1)
    assert (-3,-2) == move_point((-2,-1), 3, 1)
    assert (-3,-1) == move_point((-2,-1), 4, 1)
    assert (-2, 0) == move_point((-2,-1), 5, 1)

    with pytest.raises(NotRecognizedMoveError):
        move_point((-2,-1), -1, 1)    
    with pytest.raises(NotRecognizedMoveError):
        move_point((-2,-1), 6, 1)
    with pytest.raises(NotRecognizedMoveError):
        move_point((-2,-1), '0', 1)
    with pytest.raises(NotRecognizedMoveError):
        move_point((-2,-1), 0.0, 1)