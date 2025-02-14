from lib.point import Point
from random import randint
from math import sqrt


class Curve:

    modulo: int
    a: int
    b: int

    def __init__(self, modulo: int):
        self.modulo = modulo
        
        while True:
            A = randint(1, self.modulo - 1)
            B = randint(0, int(sqrt(self.modulo - 1)))

            # 'a' and 'b' are valid if the curve they form is not singular
            if (((4 * pow(A, 3)) + (27 * pow(B, 2))) % self.modulo) != 0:
                self.a = A
                self.b = B
                return


    def add_points(self, p: Point, q: Point) -> Point:
        if p.inf: return q
        if q.inf: return p

        if p.x != q.x:
            # Add two different points
            slope = (p.y - q.y) * pow(p.x - q.x, -1, self.modulo)
            x = (pow(slope, 2) - p.x - q.x) % self.modulo
            y = (-(p.y - slope * (p.x - x))) % self.modulo
            return Point(x, y)
        
        if not ((p.y + q.y) % self.modulo):
            # Add symetrical points
            return Point.infinite()
        
        # In other case, add the same point (p = q)
        slope = (3 * pow(p.x, 2) + self.a) * pow(2*p.y, -1, self.modulo)
        x = (pow(slope, 2) - 2 * p.x) % self.modulo
        y = (-(p.y - slope * (p.x - x))) % self.modulo
        return Point(x, y)      
        

    def mul_point(self, p: Point, n: int) -> Point:
        sum = Point.infinite()
        bit_mask = 1

        while bit_mask <= n:
            if n & bit_mask:
                sum = self.add_points(sum, p)

            p = self.add_points(p, p)
            bit_mask <<= 1
        return sum


    def __str__(self):
        a = 'a = ' + hex(self.a) + '\n'
        b = 'b = ' + hex(self.b) + '\n'
        return 'curve y^2 = x^3 + ax + b where\n' + a + b