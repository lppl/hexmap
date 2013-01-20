import pytest


@pytest.fixture(scope="module")
def points():
    """Returns dictionary of named points."""
    return { "CENTER": ( 0, 0),
             "A":      ( 2, 5),
             "B":      ( 4, 2),
             "C":      ( 5, 0),
             "D":      ( 5, 5),
             "E":      ( 3, 3),
             "F":      ( 4, 1),
             "G":      ( 1, 4),
             "H":      (-1,-2),
             "I":      (-3,-2),
             "J":      (-2, 1),
             "K":      ( 1,-1)
    }

@pytest.fixture(scope="module")
def distances(points):
    """Return list of point pairs with distances between them."""
    return ((points["A"], points["G"], 1),
            (points["B"], points["C"], 3),
            (points["C"], points["H"], 6),
            (points["D"], points["J"], 7),
            (points["E"], points["I"], 6),
            (points["F"], points["A"], 6),
            (points["G"], points["F"], 6),
            (points["H"], points["D"], 7),
            (points["I"], points["K"], 4),
            (points["J"], points["B"], 6),
            (points["K"], points["E"], 4))


@pytest.fixture(scope="module")
def circles(points):
    """Returns list of hexagon circles.

    Every circle contain points that lies in distance equal to index of 
    that circle.
    """
    return (set((( 0, 0), )),
            set(((-1, 0),(0,1),
                 (-1,-1),(1,1),
                 ( 0,-1),(1,0))),
            set(((-2,0),(-1,1),(0,2),
                 (-2,-1),(1,2),
                 (-2,-2),(2,2),
                 (-1,-2),(2,1),
                 (0,-2),(1,-1),(2,0))),
            set(((-3, 0),(-2, 1),(-1,2),(0,3),
                 (-3,-1),( 1, 3),
                 (-3,-2),( 2, 3),
                 (-3,-3),( 3, 3),
                 (-2,-3),( 3, 2),
                 (-1,-3),( 3, 1),
                 ( 0,-3),( 1,-2),(2,-1),(3,0))))

@pytest.fixture(scope="module")
def hexagons(circles):
    """Return list of filled hexagon circles.

    Every circle contain points that lies in distance equal or smaller 
    to index of that circle.
    """
    def merge(c):
        r = set()
        for s in c:
            r = r | s
        return r
    return [merge(circles[:i+1]) for i, c in enumerate(circles)]

@pytest.fixture
def hx(points):
    import hexmap
    return hexmap.map.HexMap(points["CENTER"], 20)