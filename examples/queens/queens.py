#!/usr/bin/python
#
# http://mathworld.wolfram.com/QueensProblem.html
#
from constraint import Problem
import sys

import argparse


def solve(ac=False,pc=False):
    problem = Problem()
    size = 8
    cols = range(size)
    rows = range(size)
    problem.addVariables(cols, rows)
    for col1 in cols:
        for col2 in cols:
            if col1 < col2:
                problem.addConstraint(
                    lambda row1, row2, col1=col1,
                    col2=col2: abs(row1 - row2) !=
                    abs(col1 - col2) and row1 != row2,
                    (col1, col2),
                )
                problem.addConstraint(
                    lambda row2, row1, col2=col2,
                    col1=col1: abs(row1 - row2) !=
                    abs(col1 - col2) and row1 != row2,
                    (col2, col1),
                )
    solutions = problem.getSolutions(ac,pc)
    return solutions, size


def showSolution(solution, size):
    sys.stdout.write("   %s \n" % ("-" * ((size * 4) - 1)))
    for i in range(size):
        sys.stdout.write("  |")
        for j in range(size):
            if solution[j] == i:
                sys.stdout.write(" %d |" % j)
            else:
                sys.stdout.write("   |")
        sys.stdout.write("\n")
        if i != size - 1:
            sys.stdout.write("  |%s|\n" % ("-" * ((size * 4) - 1)))
    sys.stdout.write("   %s \n" % ("-" * ((size * 4) - 1)))


def main(show=False,ac=False,pc=False):
    solutions, size = solve(ac=ac,pc=pc)
    print("Found %d solution(s)!" % len(solutions))
    if show:
        for solution in solutions:
            showSolution(solution, size)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='N-Queens Problem Solver')
    parser.add_argument('-s','--show',help='Show solutions',default=False, nargs='?',const=True)
    parser.add_argument('-ac','--arc_consistency',help='Use arc-consistency algorithm',default=False, nargs='?',const=True)
    parser.add_argument('-pc', '--path_consistency', help='Use path-consistency algorithm',default=False, nargs='?',const=True)

    args = parser.parse_args()

    main(args.show,args.arc_consistency,args.path_consistency)
