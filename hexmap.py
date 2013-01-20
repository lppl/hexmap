
orientation_sn = ("n", "ne", "se", "s", "sw", "nw")
orientation_we = ("e", "se", "sw", "w", "nw", "ne")
orientation = orientation_we
moves = (( 1, 1),
         ( 1, 0),
         ( 0,-1),
         (-1,-1),
         (-1, 0),
         ( 0, 1))

class NotRecognizedMoveError(Exception): pass
class InvalidPointException(Exception): pass
class PointOutsideOfMapException(Exception): pass

def is_point (a):
    """Checks if a is valid point. 

    Points are tuples with two elements wich are integer coordinates
    """
    return isinstance(a, tuple) and isinstance(a[0], int) and isinstance(a[1], int)


def point_guard(a):
    if not is_point(a): 
        raise InvalidPointException("Point expected but `%s` given." % a)

def distance (a, b): 
    """Return distance betwen a and b."""
    ax, ay = a
    bx, by = b
    dx = bx - ax
    dy = by - ay
    return (abs(dx) + abs(dy) + abs(dx-dy)) / 2

def in_distance (a, b, d):
    """Checks if a and b are in given distance d"""
    return distance(a, b) <= d 

def num_points_in_circle (d):
    """Calculates how many points lies in circle in d distance"""
    return 6 * d if d > 0 else 1

def num_points_in_distance (d):
    """Calculates how many points lies in given distance"""
    return 1 + 3 * d * (d+1)

def points_in_circle (c, d):
    """Returns list of points in circle from given center"""
    if d == 0:
        return set((c,))
    circle = set()
    x, y = (c[0] + d*moves[4][0], c[1] + d*moves[4][1])
    for m in moves:
        for i in range(1, d+1):
            x, y = x + m[0], y + m[1]
            circle.add((x, y))
    return circle

def points_in_distance (c, d):
    """Return set of points in distance from given center"""
    points = set()
    for i in range(0, d+1):
        points = points | points_in_circle(c, i)
    return points

def move_point(p, m, d=1):
    """Moves point in one of six directions by given distance"""
    if m not in orientation:
        raise NotRecognizedMoveError("Not recognized move `%s`, should be one of %s" % (m, orientation))
    x, y = p
    dx, dy = moves[orientation.index(m)]
    return (x + dx, y + dy)


class Field:
    def __init__(self, p):
        point_guard(p)
        self.p = p

class HexMapCursor:

    def __init__(self, hexmap, p):
        self.hexmap = hexmap
        self.go_to(p)

    def go_to(self, p):
        point_guard(p)
        self.p = p
        return self

    def move(self, m, d=1):
        self.go_to(move_point(self.p, m, d))
        return self

    def position(self):
        return self.p

    def get_field(self):
        return self.hexmap.get_field(self.p)

    def set_field(self, field):
        self.hexmap.set_field(self.p, field)
        return self


class HexMap:
    
    fields = {}

    def __init__(self, center=(0,0), size=9):
        point_guard(center)
        self.center = center
        self.size = size

    def get_cursor(self, p=None):
        return HexMapCursor(self, p if is_point(p) else self.center)

    def set_field(self, p, field):
        self.__map_point_guard(p)
        self.fields[p] = field

    def get_field(self, p):
        self.__map_point_guard(p)
        return self.fields[p] if p in self.fields else None

    def __map_point_guard(self, p):
        point_guard(p)
        if not in_distance(self.center, p, self.size - 1):
            raise PointOutsideOfMapException(
                "Point %s exists outside of map center: %s, size: %s" % 
                (p, self.center, self.size))
