from lib.curve import Curve
from lib.point import Point
from argparse import ArgumentParser


parser = ArgumentParser()
parser.add_argument('-n', '--number', type=str, required=True, help='number to test')
parser.add_argument('-i', '--iterations', type=int, default=100, help='max number of iterations')
parser.add_argument('-v', '--verbose', action='store_true', help='activate extra logs')
parser.add_argument('-b', '--base', type=str, default='dec', help='base of the number to test (binary=bin, octal=oct, decimal=dec, hexadecimal=hex)')
args = parser.parse_args()


bases_parse = { 'bin': 2, 'oct': 8, 'dec': 10, 'hex': 16 } 
bases_str = { 'bin': bin, 'oct': oct, 'dec': str, 'hex': hex } 

n = int(args.number, bases_parse[args.base])
iteration = 1

for iteration in range(args.iterations):
    try:
        curve = Curve(n)
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
        print('End of procedure: ' + bases_str[args.base](n) + ' is not prime.')
        exit(0)


# At this point n may be a prime number or, alternatively,
# none of its non-trivial factors have been involved in inverse
# modulo operations.
print('End of procedure. Maybe ' + bases_str[args.base](n) + 
      ' is prime or the generated curves are not ideal.')  