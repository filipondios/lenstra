from lib.curve import Curve
from lib.point import Point
import math
import random
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-n', '--number', type=int, required=True, help='number to test')
parser.add_argument('-i', '--iterations', type=int, default=100, help='max number of iterations')
parser.add_argument('-v', '--verbose', action='store_true', help='activate extra logs')
args = parser.parse_args()

n = args.number
iteration = 1

while iteration <= args.iterations:
    try:
        A = random.randint(1, n - 1)
        B = random.randint(0, int(math.sqrt(n - 1)))
        curve = Curve(A, B, n)
        point = Point(0, pow(curve.b, 2))

        if args.verbose:
            print('Iteration ' + str(iteration) + 
                '. Using ' + str(curve) 
                + 'And initial point = ' + str(point) + '\n')
        
        curve.mul_point(point, 30894)
        iteration += 1

    except ValueError:
        # Modulo inverse just failed so a non-trivial factor of
        # n has been found. This means n is not a prime number.
        print('End of procedure. ' + hex(n) + ' is not prime.')
        exit(0)


# At this point n may be a prime number or, alternatively,
# none of its non-trivial factors have been involved in inverse
# modulo operations.
print('End of procedure. Maybe ' + hex(n) + 
      ' is prime or the generated curves are not ideal.')