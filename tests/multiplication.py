from ..lenstra.point import Point
from ..lenstra.curve import Curve

# 101 times (72,57) in secp256k1 modulo 107
curve = Curve(0, 7, 107)
p = Point(72, 57)

r = curve.mul_point(p, 101)
assert(not r.inf)
assert(r.x == 99)
assert(r.y == 43)

# 69 times (16,25) in secp256k1 modulo 37
curve = Curve(0, 7, 37)
p = Point(16, 25)

r = curve.mul_point(p, 69)
assert(not r.inf)
assert(r.x == 24)
assert(r.y == 20)

# 1218 times (32,37) in secp256k1 modulo 41
curve = Curve(0, 7, 41)
p = Point(32, 37)

r = curve.mul_point(p, 1218)
assert(r.inf)

# 3218 times (56,18) in curve25519 modulo 71
curve = Curve(486662, 1, 71)
p = Point(56, 18)

r = curve.mul_point(p, 3218)
assert(not r.inf)
assert(r.x == 38)
assert(r.y == 42)

# 5022 times (27,21) in curve25519 modulo 97
curve = Curve(486662, 1, 97)
p = Point(27, 21)

r = curve.mul_point(p, 5022)
assert(r.inf)
print('test_mul_point -- passed')