from z3 import *
from itertools import *

## RULES ##
# Synthesize a simple function using Z3!
# The function will take two ORDERED inputs, and produces an output.
# Based on magic intuition, we know the following about the function:
# 1. It only uses the operations * and <<
# 2. It returns the result of a single statement of the form
#    [Input_x] [op] [Input_y]
# 3. It uses both inputs, but you do not know in what order.
#
# IO Pairs:
#   IN: (3, 5)    OUT: 40
#   IN: (6, 9)    OUT: 576
#   IN: (23, 44)  OUT: 369098752
#   IN: (16, 22)  OUT: 1441792
#   IN: (8, 9)    OUT: 2304

io_pairs = [
    ((3, 5), 40),
    ((6, 9), 576),
    ((23, 44), 369098752),
    ((16, 22), 1441792),
    ((8, 9), 2304),
]

# Convenience functions for creating a constraint using a flag with identifier
# 'i' that toggles whether the operator is used for operands x1 and x2.
# Use is OPTIONAL.
def mul(i, x1, x2):
    return (BitVec(f'B{i}', 16) & 0x0001) * (x1 * x2)

def shl(i, x1, x2):
    return (BitVec(f'B{i}', 16) & 0x0001) * (x1 << x2)

# Your Synthesizer: construct a Z3 formula using input/output pairs.
def formula(pairs):
    constraint = True
    for (x, y), ans in io_pairs:
        this_constraint = mul(0, x, y) + mul(1, y, x) + shl(2, x, y) + shl(3, y, x) == ans
        constraint = And(constraint, this_constraint)
    return constraint


if __name__ == '__main__':
    s = formula(io_pairs)
    print(f'Z3 formula: {s}')
    print('Z3 Solution:')
    solve(s)
