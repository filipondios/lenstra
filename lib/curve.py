from lib.point import Point
from random import randint
from math import sqrt


class InversionImpossible(Exception):
    """The modular inverse does not exist; the denominator 
       shares a factor with the modulus."""
    def __init__(self, denominator):
        self.denominator = denominator


class Curve:

    modulo: int
    a: int
    b: int

    def __init__(self, modulo: int):
        self.modulo = modulo

        while True:
            A = randint(1, self.modulo - 1)
            B = randint(0, int(sqrt(self.modulo - 1)))

            if self._no_singular(A, B):
                self.a = A
                self.b = B
                return

    def _no_singular(self, a: int, b: int) -> bool:
        return (4 * pow(a, 3) + 27 * pow(b, 2)) % self.modulo != 0

    def generate_point(self) -> Point:
        """Pick (x, y) and derive b so that the point lies on the curve."""
        while True:
            x = randint(0, self.modulo - 1)
            y = randint(0, self.modulo - 1)
            b = (y * y - x * x * x - self.a * x) % self.modulo

            if self._no_singular(self.a, b):
                self.b = b
                return Point(x, y)

    def _inverse(self, denominator: int) -> int:
        try:
            return pow(denominator, -1, self.modulo)
        except ValueError:
            raise InversionImpossible(denominator) from None

    def add_points(self, p: Point, q: Point) -> Point:
        if p.inf: return q
        if q.inf: return p

        if p.x != q.x:
            # Add two different points.
            slope = (p.y - q.y) * self._inverse(p.x - q.x)
            x = (pow(slope, 2) - p.x - q.x) % self.modulo
            y = (-(p.y - slope * (p.x - x))) % self.modulo
            return Point(x, y)

        if not ((p.y + q.y) % self.modulo):
            # Add symmetrical points.
            return Point.infinite()

        # Otherwise, add the same point (p = q).
        slope = (3 * pow(p.x, 2) + self.a) * self._inverse(2 * p.y)
        x = (pow(slope, 2) - 2 * p.x) % self.modulo
        y = (-(p.y - slope * (p.x - x))) % self.modulo
        return Point(x, y)

    def mul_point(self, p: Point, n: int) -> Point:
        total = Point.infinite()
        bit_mask = 1

        while bit_mask <= n:
            if n & bit_mask:
                total = self.add_points(total, p)

            p = self.add_points(p, p)
            bit_mask <<= 1
        return total

    def __str__(self):
        a = 'a = ' + hex(self.a) + '\n'
        b = 'b = ' + hex(self.b) + '\n'
        return 'curve y^2 = x^3 + ax + b where\n' + a + b
