from constraint import Problem
import time

def solve():
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
    solutions = problem.getSolutions()
    print ('Solutions:\n',solutions)
    return solutions


def main():
    time_start = time.time()
    solutions = solve()
    time_end = time.time()

    print("Found %d solution(s)! Time elapsed: %f sec" % (len(solutions),time_end-time_start))

if __name__ == "__main__":
    main()
