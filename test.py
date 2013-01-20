#!/usr/bin/env python
import pytest

CENTER = (0,0)
A = ( 2, 5)
B = ( 4, 2)
C = ( 5, 0)
D = ( 5, 5)
E = ( 3, 3)
F = ( 4, 1)
G = ( 1, 4)
H = (-1,-2)
I = (-3,-2)
J = (-2, 1)
K = ( 1,-1)

            
            
distances = ((A, G, 1),
             (B, C, 3),
             (C, H, 6),
             (D, J, 7),
             (E, I, 6),
             (F, A, 6),
             (G, F, 6),
             (H, D, 7),
             (I, K, 4),
             (J, B, 6),
             (K, E, 4))


circumference_0 = set((CENTER, ))
circumference_1 = set(((-1, 0),(0,1),
                       (-1,-1),(1,1),
                       ( 0,-1),(1,0)))
circumference_2 = set(((-2,0),(-1,1),(0,2),
                       (-2,-1),(1,2),
                       (-2,-2),(2,2),
                       (-1,-2),(2,1),
                       (0,-2),(1,-1),(2,0)))
circumference_3 = set(((-3, 0),(-2, 1),(-1,2),(0,3),
                       (-3,-1),( 1, 3),
                       (-3,-2),( 2, 3),
                       (-3,-3),( 3, 3),
                       (-2,-3),( 3, 2),
                       (-1,-3),( 3, 1),
                       ( 0,-3),( 1,-2),(2,-1),(3,0)))

circumferences = [circumference_0,
                  circumference_1,
                  circumference_2,
                  circumference_3]

def merge(c):
    r = set()
    for s in c:
        r = r | s
    return r
circles = [merge(circumferences[:i+1]) for i, c in enumerate(circumferences)]


"""
Here I test basic functions that 
"""
import hexmap
from hexmap import is_point, distance, in_distance
from hexmap import num_points_in_circle, num_points_in_distance
from hexmap import points_in_circle, points_in_distance
from hexmap import move_point, NotRecognizedMoveError
from hexmap import Field, HexMap, HexMapCursor


def test_is_point():
    assert is_point((1, 2))
    assert is_point((-1, 2))
    assert not is_point((1.0, 2))
    assert not is_point((1, 2.0))
    assert not is_point((1,'2'))
    assert not is_point(('1',2))
    assert not is_point({0:1, 1:3})
    assert not is_point([])

def test_distance():
    for a, b, d in distances:
        assert distance(a, a) == 0
        assert distance(a, b) == d
        assert distance(b, a) == d

def test_in_distance():
    for a, b, d in distances:
        assert in_distance(a, a, 0)
        assert in_distance(a, b, d)
        assert in_distance(b, a, d)
        assert in_distance(a, b, d + 1)
        assert in_distance(b, a, d + 1)
        assert not in_distance(a, b, d - 1)
        assert not in_distance(b, a, d - 1)

def test_num_points_in_circle():
    for i, c in enumerate(circumferences):
        assert len(c) == num_points_in_circle(i)


def test_num_points_in_distance():
    for i, c in enumerate(circles):
        assert len(c) == num_points_in_distance(i)


def test_points_in_circle():
    for i, c in enumerate(circumferences):
        assert c == points_in_circle(CENTER, i)

def test_points_in_distance():
    for i, c in enumerate(circles):
        assert c == points_in_distance(CENTER, i)


def test_moves():

    with pytest.raises(NotRecognizedMoveError):
        move_point((-2,-1), "ele", 1)    
    with pytest.raises(NotRecognizedMoveError):
        move_point((-2,-1), "trele", 1)    

    assert hexmap.orientation == hexmap.orientation_we


    hexmap.orientation = hexmap.orientation_sn
    assert (-1, 0) == move_point((-2,-1), "n",  1)
    assert (-1,-1) == move_point((-2,-1), "ne", 1)
    assert (-2,-2) == move_point((-2,-1), "se", 1)
    assert (-3,-2) == move_point((-2,-1), "s",  1)
    assert (-3,-1) == move_point((-2,-1), "sw", 1)
    assert (-2, 0) == move_point((-2,-1), "nw", 1)
    with pytest.raises(NotRecognizedMoveError):
        move_point((-2,-1), "w", 1)    
    with pytest.raises(NotRecognizedMoveError):
        move_point((-2,-1), "e", 1)

    hexmap.orientation = hexmap.orientation_we
    assert (-1, 0) == move_point((-2,-1), "e",  1)
    assert (-1,-1) == move_point((-2,-1), "se", 1)
    assert (-2,-2) == move_point((-2,-1), "sw", 1)
    assert (-3,-2) == move_point((-2,-1), "w",  1)
    assert (-3,-1) == move_point((-2,-1), "nw", 1)
    assert (-2, 0) == move_point((-2,-1), "ne", 1)
    with pytest.raises(NotRecognizedMoveError):
        move_point((-2,-1), "s", 1)
    with pytest.raises(NotRecognizedMoveError):
        move_point((-2,-1), "n", 1)

@pytest.fixture
def hx():
    return HexMap(CENTER, 20)

def test_Field():
    f = Field(CENTER)

def test_HexMapCursor(hx):
    cursor = hx.get_cursor(A)
    assert A == cursor.position()
    assert (-1, 0) == cursor.go_to((-2,-1)).move("e",  1).position()
    assert (-1,-1) == cursor.go_to((-2,-1)).move("se", 1).position()
    assert (-2,-2) == cursor.go_to((-2,-1)).move("sw", 1).position()
    assert (-3,-2) == cursor.go_to((-2,-1)).move("w",  1).position()
    assert (-3,-1) == cursor.go_to((-2,-1)).move("nw", 1).position()
    assert (-2, 0) == cursor.go_to((-2,-1)).move("ne", 1).position()
    
    fa = Field(A)
    fb = Field(B)
    fc = Field(C)
    assert fa == cursor.go_to(A).set_field(fa).get_field()
    assert fb == cursor.go_to(B).set_field(fb).get_field()
    assert fc == cursor.go_to(C).set_field(fc).get_field()

    raise Exception("Need more tests")

def test_HexMap():
    hx = HexMap()
    assert isinstance(hx.get_cursor(), HexMapCursor)
    assert hx.get_cursor() != hx.get_cursor()
    raise Exception("Need more tests")


if __name__ == '__main__':
    test_is_point()
    test_distance()
