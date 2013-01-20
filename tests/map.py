from hexmap.map import Field, HexMap, HexMapCursor

def test_Field(points):
    f = Field(points["CENTER"])

def test_HexMapCursor(hx, points):
    cursor = hx.get_cursor(points["A"])
    assert points["A"] == cursor.position()
    assert (-1, 0) == cursor.go_to((-2,-1)).move(hx.directions["e"],  1).position()
    assert (-1,-1) == cursor.go_to((-2,-1)).move(hx.directions["se"], 1).position()
    assert (-2,-2) == cursor.go_to((-2,-1)).move(hx.directions["sw"], 1).position()
    assert (-3,-2) == cursor.go_to((-2,-1)).move(hx.directions["w"],  1).position()
    assert (-3,-1) == cursor.go_to((-2,-1)).move(hx.directions["nw"], 1).position()
    assert (-2, 0) == cursor.go_to((-2,-1)).move(hx.directions["ne"], 1).position()
    
    fa = Field(points["A"])
    fb = Field(points["B"])
    fc = Field(points["C"])
    assert fa == cursor.go_to(points["A"]).set_field(fa).get_field()
    assert fb == cursor.go_to(points["B"]).set_field(fb).get_field()
    assert fc == cursor.go_to(points["C"]).set_field(fc).get_field()

    raise Exception("Need specification, need testssss, need blooood...")

def test_HexMap():
    hx = HexMap()
    assert isinstance(hx.get_cursor(), HexMapCursor)
    assert hx.get_cursor() != hx.get_cursor()
    raise Exception("Need specification, need testssss, need blooood...")