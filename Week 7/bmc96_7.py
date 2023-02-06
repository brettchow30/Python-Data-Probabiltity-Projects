"""ECE 105: Programming for Engineers II
Lab 7: Sierpinski Gasket
May 16-17, Spring 2019

PLEASE rename this solution .py file as your <abc123>_7.py" before submission
"""


import random
import matplotlib.pyplot as plt
import numpy as np
from math import sqrt


def sierpinski(p0, vs, f, inum):
    """Generate points for the Sierpinski gasket
    
    Args:
        p0: 2-element numpy array [x, y] representing the initial point for
            generating the Sierpinksi Triangle
        vs: 3 vertices of the triangle, as a a list of numpy arrays
            [[x0, x1, x2], [y0, y1, y2]]
        f: parameter for constructing points 
           (To keep things simple, f = 1/2. You must use variable f instead
            of hard coding 1/2 in your code)
        inum: number of points to generate (number of iterations)

    Returns:
        np.ndarray of np.ndarrays: [[x0, y0], [x1, y1], ...]
    """
    
    points = [p0]
    for i in range(inum):
        a = random.choice([0,1,2])
        vertex = [vs[0][a], vs[1][a]]
        midx = (points[-1][0] + vertex[0]) * f
        midy = (points[-1][1] + vertex[1]) * f
        points.append(np.array([midx, midy]))
        
    return np.array(points)
        
    
    


    

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# Do not change anything below this comment.
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

def init_test_data():
    vs = [[-sqrt(3)/2, sqrt(3)/2, 0], [-1/2, -1/2, 1]]
    p0 = [0, 0]
    f = 1/2
    return f, np.array(p0), np.array(vs)


def test_1():
    """Purely graphical"""
    print('=========================')
    print("Graphical test, no points given")
    print('=========================')
    f, p0, vs = init_test_data()
    for n in 1000, 10000, 100000:
        xs, ys = sierpinski(p0, vs, f, n).transpose()
        fig = plt.figure()
        plt.plot(xs, ys, linestyle='', marker='.', markersize=0.5, figure=fig)
        fig.gca().set_title(f"Sierpinski Triangle - Chaos Game n={n}")
        fig.savefig(f"test-{n}.pdf")
        plt.show()
    return 0


def test_2():
    """Test if points exist in expected locations"""
    print('=========================')
    print("Value test, checking if points exist")
    print('=========================')
    f, p0, vs = init_test_data()
    n = 1000000
    random.seed(101)
    ps = np.around(sierpinski(p0, vs, f, n), decimals=3)
    # convert to string for more stable representation
    ps = [[str(x), str(y)] for [x, y] in ps]
    grade = 0
    if ['0.0', '0.0'] in ps:
        grade += 5
    if ['0.3', '-0.364'] in ps:
        grade += 5
    if ['-0.17', '0.321'] in ps:
        grade += 5
    if ['-0.783', '-0.358'] in ps:
        grade += 5
    return grade


def is_empty_function(func):
    # https://stackoverflow.com/a/24689937/1371191

    def empty_func():
        pass

    def empty_func_with_doc():
        """Empty function with docstring."""
        pass

    return func.__code__.co_code == empty_func.__code__.co_code \
        or func.__code__.co_code == empty_func_with_doc.__code__.co_code


def test_required(fns):
    for fnname in fns:
        if fnname not in globals():
            raise RuntimeError(f'missing function {fnname}')
        elif (is_empty_function(globals()[fnname])):
            raise RuntimeError(f'fill in {fnname}!')


def main(week, tests):
    import os
    import re

    f = os.path.basename(__file__)
    r = re.compile(f'^([a-z]+[0-9]+)_{week}\\.py$')
    m = r.match(f)
    if not m:
        raise RuntimeError(f"Expecting file to be named 'abc123_{week}.py'")
    uid = m.group(1)
    grade = 0
    for test, requirements in tests:
        try:
            test_required(requirements)
            grade += test()
        except Exception as exc:
            print(exc)
    print('======== Summary ========')
    print(f'Student : {uid}')
    print(f'Total   : {grade} / 20')


if __name__ == '__main__':
    tests = [(test_1, ['sierpinski']),
             (test_2, ['sierpinski'])]
    main(7, tests)
