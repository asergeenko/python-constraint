from constraint import Problem
import time
import argparse

def solve(ac=False,pc=False):
    problem = Problem()
    # Countries
    countries = ['A','B','C']
    # Number of colors
    num_colors = 2
    # Neighbours on the map
    neighbours = ['AB','BC','CA']

    neighbours = [''.join(sorted(n)) for n in neighbours]
    problem.addVariables(countries,range(num_colors))
    for country1 in countries:
        for country2 in countries:
            if country1 != country2:
                constraint = lambda color1,color2,country1=country1,country2=country2: not any(''.join(sorted(country1+country2)) in s for s in neighbours) or color1!=color2
                problem.addConstraint(constraint, [country1, country2])
    solutions = problem.getSolutions(ac,pc)
    print ('Solutions:\n',solutions)
    return solutions


def main(ac=False,pc=False):
    time_start = time.time()
    solutions = solve(ac,pc)
    time_end = time.time()

    print("Found %d solution(s)! Time elapsed: %f sec" % (len(solutions),time_end-time_start))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='N-Queens Problem Solver')
    parser.add_argument('-s','--show',help='Show solutions',default=False, nargs='?',const=True)
    parser.add_argument('-ac','--arc_consistency',help='Use arc-consistency algorithm',default=False, nargs='?',const=True)
    parser.add_argument('-pc', '--path_consistency', help='Use arc-consistency algorithm',default=False, nargs='?',const=True)

    args = parser.parse_args()

    main(args.arc_consistency,args.path_consistency)

