from lib.point import Point
from lib.curve import Curve


def make_curve(a, b, modulo):
    curve = Curve(modulo)
    curve.a, curve.b = a, b
    return curve


def test_add_points():
    curve = make_curve(0, 7, 97)
    p = Point(17, 19)

    # Add point to the identity element.
    r = curve.add_points(p, Point.infinite())
    assert (r.inf, r.x, r.y) == (False, 17, 19)

    # Add the same point (doubling).
    r = curve.add_points(p, p)
    assert (r.inf, r.x, r.y) == (False, 95, 75)

    # Add different points.
    r = curve.add_points(p, Point(27, 22))
    assert (r.inf, r.x, r.y) == (False, 56, 76)

    # p + (-p) = infinite.
    assert curve.add_points(p, Point(17, 78)).inf


def test_mul_point():
    # 101 times (72,57) modulo 107
    curve = make_curve(0, 7, 107)
    r = curve.mul_point(Point(72, 57), 101)
    assert (r.inf, r.x, r.y) == (False, 99, 43)

    # 69 times (16,25) modulo 37
    curve = make_curve(0, 7, 37)
    r = curve.mul_point(Point(16, 25), 69)
    assert (r.inf, r.x, r.y) == (False, 24, 20)

    # 1218 times (32,37) modulo 41
    curve = make_curve(0, 7, 41)
    assert curve.mul_point(Point(32, 37), 1218).inf

    # 3218 times (56,18) modulo 71
    curve = make_curve(486662, 1, 71)
    r = curve.mul_point(Point(56, 18), 3218)
    assert (r.inf, r.x, r.y) == (False, 38, 42)

    # 5022 times (27,21) modulo 97
    curve = make_curve(486662, 1, 97)
    assert curve.mul_point(Point(27, 21), 5022).inf


def test_generated_point_lies_on_curve():
    curve = Curve(101)
    point = curve.generate_point()

    lhs = pow(point.y, 2)
    rhs = pow(point.x, 3) + curve.a * point.x + curve.b
    assert (lhs - rhs) % curve.modulo == 0
    assert (4 * pow(curve.a, 3) + 27 * pow(curve.b, 2)) % curve.modulo != 0
