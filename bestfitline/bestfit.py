import sys
import re
import numpy as np


def parse_input(datafile):
    points = re.findall(r'\((-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?)\)', datafile.read())
    x_val = []
    y_val = []
    for i in points:
        x_val.append(float(i[0]))
        y_val.append(float(i[1]))
    return x_val, y_val


def func(x, y):
    one = []
    neg_one = []
    for i in range(len(x)):
        one.append(1)
        neg_one.append(-1)
    neg_x = []
    for i in x:
        neg_x.append(-i)
    neg_y = []
    for i in y:
        neg_y.append(-i)

    x_neg_x = x + neg_x
    y_neg_y = np.array([y + neg_y])
    one_neg_one = one + neg_one
    neg_one_neg_one = [-1 for i in range(2 * len(x))]
    coefficient_matrix = np.array([x_neg_x, one_neg_one, neg_one_neg_one]).T  # 2n by 4 matrix

    bound1 = (-np.inf, np.inf)
    bound2 = (-np.inf, np.inf)
    bound3 = (0, np.inf)

    from scipy import optimize
    result = optimize.linprog(
        c=np.array([0, 0, 1]),  # a, b, z
        A_ub=coefficient_matrix,
        b_ub=y_neg_y,
        bounds = [bound1, bound2, bound3]
    )
    return result


if __name__ == '__main__':
    if len(sys.argv) == 2:
        datafile = open(sys.argv[1], 'r')
        x, y = parse_input(datafile)
        result = func(x, y)
        print("%2.6f,%2.6f" % (result.x[0],result.x[1]))
