import math
import sys
from decimal import *


def fibonacci(n, precision):
    terms = 3
    getcontext().prec = precision
    last_two_terms = 1
    last_term = 1
    sum = Decimal(2)
    shifter = 0
    while (terms <= n):
        current = last_term + last_two_terms
        current_term = Decimal(10 ** shifter) / Decimal(current)
        sum += current_term
        if (terms % 6 == 0):
            digit = math.floor(sum)
            print(digit, flush=True)
            sum -= digit
            sum *= 10
            shifter += 1
        terms += 1
        last_two_terms = last_term
        last_term = current

def func(n):
    num_terms = n * 6
    fibonacci(num_terms, n + 10)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        n = int(sys.argv[1])
        func(n)
