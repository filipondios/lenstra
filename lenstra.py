from lib.curve import Curve
from lib.point import Point
import math
import random

# Suyama curves

n = 0x3790274390284902383242576347
iterations = 100
iteration = 1

while iteration <= iterations:
    try:
        A = random.randint(1, n - 1)
        B = random.randint(0, int(math.sqrt(n - 1)))
        curve = Curve(A, B, n)
        point = Point(0, pow(curve.b, 2))

        print('Iteration ' + str(iteration) + '. Using ' 
            + str(curve) + 'And initial point = '
            + str(point) + '\n')
        
        curve.mul_point(point, 30894)
        iteration += 1

    except ValueError:
        print('Modulo inverse error, ' + hex(n) + ' is not prime.')
        break