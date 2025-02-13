from ..lib.point import Point
from ..lib.curve import Curve

# Add point to the identity element.
curve = Curve(0, 7, 97)
p = Point(17, 19)
q = Point.infinite()

r = curve.add_points(p, q)
assert(not r.inf)
assert(r.x == 17)
assert(r.y == 19)

# Add the same point.
r = curve.add_points(p, p)
assert(not r.inf)
assert(r.x == 95)
assert(r.y == 75)

# Add different points.
q = Point(27, 22)

r = curve.add_points(p, q)
assert(not r.inf)
assert(r.x == 56)
assert(r.y == 76)

# Add symetrical points.
q = Point(17, 78)

r = curve.add_points(p, q)
assert(r.inf)
print('test_add_points -- passed')