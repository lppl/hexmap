directions = (( 1,  1),
              ( 1,  0),
              ( 0, -1),
              (-1, -1),
              (-1,  0),
              ( 0,  1))


class NotRecognizedMoveError(Exception):
    pass


class InvalidPointException(Exception):
    pass


def is_point(a):
    """Checks if a is valid point.

    Points are tuples with two elements wich are integer coordinates
    """
    return isinstance(a, tuple) and isinstance(a[0], int) and isinstance(a[1], int)


def point_guard(a):
    if not is_point(a):
        raise InvalidPointException("Point expected but `%s` given." % a)


def direction_guard(m):
    if not isinstance(m, int) or m < 0 or m > 5:
        raise NotRecognizedMoveError("Not recognized move `%s`" % str(m))


def distance(a, b):
    """Return distance betwen a and b."""
    ax, ay = a
    bx, by = b
    dx = bx - ax
    dy = by - ay
    return (abs(dx) + abs(dy) + abs(dx - dy)) / 2


def in_distance(a, b, d):
    """Checks if a and b are in given distance d"""
    return distance(a, b) <= d


def num_points_in_circle(d):
    """Calculates how many points lies in circle in d distance"""
    return 6 * d if d > 0 else 1


def num_points_in_distance(d):
    """Calculates how many points lies in given distance"""
    return 1 + 3 * d * (d + 1)


def points_in_circle(c, d):
    """Returns list of points in circle from given center"""
    if d == 0:
        return set((c,))
    circle = set()
    x, y = (c[0] + d * directions[4][0], c[1] + d * directions[4][1])
    for m in directions:
        for i in range(1, d + 1):
            x, y = x + m[0], y + m[1]
            circle.add((x, y))
    return circle


def points_in_distance(c, d):
    """Return set of points in distance from given center"""
    points = set()
    for i in range(0, d + 1):
        points = points | points_in_circle(c, i)
    return points


def move_point(p, direction, d=1):
    """Moves point in one of six directions by given distance"""
    direction_guard(direction)
    x, y = p
    dx, dy = directions[direction]
    return (x + dx * d, y + dy * d)
