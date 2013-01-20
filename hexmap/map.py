from grid import point_guard, move_point, in_distance, is_point

orientation_sn = ("n", "ne", "se", "s", "sw", "nw")
orientation_we = ("e", "se", "sw", "w", "nw", "ne")
orientation = orientation_we

class PointOutsideOfMapException(Exception): pass

class Field:
    def __init__(self, p):
        point_guard(p)
        self.p = p

class HexMapCursor:

    def __init__(self, hexmap, p):
        self.hexmap = hexmap
        self.directions = hexmap.directions
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

    def __init__(self, center=(0,0), size=9, orientation=orientation):
        point_guard(center)
        self.center = center
        self.size = size
        self.orientation = orientation
        self.directions = {}
        for i, d in enumerate(orientation):
            self.directions[d] = i

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
