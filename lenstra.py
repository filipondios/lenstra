import json
import random
import sys
from argparse import ArgumentParser
from time import perf_counter
from lib.factor import FactorizationIncomplete, factorize


BASE_PARSE = { 'bin': 2, 'oct': 8, 'dec': 10, 'hex': 16 }
bases_str = { 'bin': bin, 'oct': oct, 'dec': str, 'hex': hex }


def format_result(n: int, factors: dict[int, int], base: str) -> str:
    fmt = bases_str[base]
    if len(factors) == 1 and next(iter(factors.values())) == 1:
        return f'{fmt(n)} is prime (Miller-Rabin).'
    return (f'{fmt(n)} = ' + ' * '.join(
        f'{fmt(p)}^{e}' if e > 1 else fmt(p) for p, e in factors.items())
        + '  (composite, verified with Miller-Rabin)')


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument('-n', '--number', type=str, required=True, help='number to factorize')
    parser.add_argument('-b', '--base', type=str, default='dec', choices=list(BASE_PARSE),
        help='input base (bin, oct, dec, hex)')
    parser.add_argument('-c', '--curves', type=int, default=100,
        help='maximum number of ECM curves (default: 100)')
    parser.add_argument('--rounds', type=int, default=40,
        help='Miller-Rabin rounds for n >= 2^64 (default: 40)')
    parser.add_argument('--b1', type=int, default=10000,
        help='ECM smoothness bound (default: 10000)')
    parser.add_argument('--seed', type=int, default=None,
        help='seed for the random number generator (reproducibility)')
    parser.add_argument('-v', '--verbose', action='store_true',
        help='print each ECM curve and the elapsed time')
    parser.add_argument('--json', action='store_true', help='emit structured JSON output')
    args = parser.parse_args()

    curves = args.curves

    if curves < 1: parser.error('--curves must be >= 1')
    if args.rounds < 1: parser.error('--rounds must be >= 1')
    if args.b1 < 2: parser.error('--b1 must be >= 2')
    if args.seed is not None:
        random.seed(args.seed)

    try:
        n = int(args.number, BASE_PARSE[args.base])
    except ValueError:
        parser.error(f'{args.number!r} is not a valid number in base {args.base}')
    if n < 2: parser.error('--number must be >= 2')

    start = perf_counter()

    try:
        factors = factorize(n, b1=args.b1, curves=curves,
            rounds=args.rounds, verbose=args.verbose)
    except FactorizationIncomplete:
        message = (f'Could not factorize {bases_str[args.base](n)} with b1={args.b1} '
            f'and {curves} curves. Try larger values.')
        if args.json: print(json.dumps({'number': n, 'factored': False, 'error': message}))
        else: print(message)
        return 1

    elapsed = perf_counter() - start

    if args.json:
        print(json.dumps({
            'number': n,
            'prime': len(factors) == 1 and next(iter(factors.values())) == 1,
            'factors': {str(p): e for p, e in factors.items()},
            'b1': args.b1,
            'curves': curves,
            'seconds': round(elapsed, 6),
        }))
    else:
        print(format_result(n, factors, args.base))
        if args.verbose:
            print(f'Time: {elapsed:.4f} s. Methods tried: trial division, Pollard rho, ECM.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
