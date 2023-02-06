import sys
import re
import math
import time
import numpy as np
import matplotlib.pyplot as plt


# -----------------------------------------------------------
# Lab 4, Problem 1
# Fill in the function below
# -----------------------------------------------------------
def sawtooth(t, T, smin, smax):
    """Generates discrete values for a sawtooth waveform.
    
    Args:
        t (np.ndarray of np.double): time samples
        T (int):                     period of the sawtooth
        smin (int):                  minimum value of the sawtooth
        smax (int):                  maximum value of the sawtooth

    Returns:
        np.ndarray of np.double: resultant values of the sawtooth signal

    """
    # Please start your code here
    st = smin + (((t/T) - np.floor(t/T)) * (smax - smin))
    
    # filler code, please delete it
    # Please end your code here

    return st


# -----------------------------------------------------------
# Lab 4, Problem 2
# Fill in the function below
# HINT: (Don't be afraid to make additional helper functions)
# -----------------------------------------------------------

def sk(t, k, T):
    """
    Args:
        t (np.ndarray of np.double): time samples
        k (int):                     calculate the kth term
        T (int):                     period of the sawtooth

    Return:
        sktemp (np.ndarray of np.double): kth term approximation

    """

    # Please start your code here
    
    sktemp = (((-1)**k)*(1/k)*np.sin((2*np.pi/T)*k*(t - T/2))) # filler code, please delete it
    # Please end your code here
    return sktemp

def sawtoothapprox(t, kmax, T, smin, smax):
    """Approximates a sawtooth waveform with a Fourier series.

    Args:
        t (np.ndarray of np.double): time samples
        kmax (int):                  calculate the first kmax terms
        T (int):                     period of the sawtooth
        smin (int):                  minimum value of the sawtooth
        smax (int):                  maximum value of the sawtooth

    Returns:
        np.ndarray of np.double: resultant values of the sawtooth signal

    """
    # Please start your code here
    sigma = 0
    for k in range(1, kmax + 1):
        sigma += sk(t, k, T)
    stapp = .5*(smin + smax) - (1/np.pi * (smax - smin)) * sigma    # filler code, please delete it
    # Please end your code here

    return stapp


# -----------------------------------------------------------
# Helper plot functions
# -----------------------------------------------------------
def plot_sawtooth(t, s, T, smin, smax, filename):
    """Plots a sawtooth signal, given its dependent and independent variables

    Args:
        t (np.ndarray of np.double): time samples
        s (np.ndarray of np.double): corresponsing sawtooth signal
        T (int):                     period of the sawtooth
        smin (int):                  minimum value of the sawtooth
        smax (int):                  maximum value of the sawtooth

    """
    plt.figure()
    plt.plot(t, s)
    plt.title('periodic sawtooth waveform s(t) with '
              'T = {}, smin = {}, smax = {}'.format(T, smin, smax))
    plt.xlabel('time (t)')
    plt.ylabel('s (t)')
    plt.savefig(filename)
    plt.show()


def plot_sawtooth_approx(t, s, a, kmax, T, smin, smax, filename):
    """Plots a sawtooth signal and its Fourier series, given its dependent and
    independent variables

    Args:
        t (np.ndarray of np.double): time samples
        s (np.ndarray of np.double): corresponsing sawtooth signal
        a (np.ndarray of np.double): fourier approximation of sawtooth signal
        kmax (int):                  calculate the first kmax terms
        T (int):                     period of the sawtooth
        smin (int):                  minimum value of the sawtooth
        smin (int):                  maximum value of the sawtooth

    """
    plt.figure()
    plt.plot(t, s)
    plt.plot(t, a)
    plt.title('{}-term approx. to periodic sawtooth '
              '(T = {}, smin = {}, smax = {})'.format(kmax, T, smin, smax))
    plt.xlabel('time (t)')
    plt.ylabel('s (t)')
    plt.savefig(filename)
    plt.show()


## ================== !!! DO NOT CHANGE ANYTHING BELOW THIS LINE !!! ================== ##
## ---------------------------------------------------------------------------------------##
## ANY change made below will be considered as INVALID submission and will receive 0 POINTS ##
## ---------------------------------------------------------------------------------------##
## ================== !!! DO NOT CHANGE ANYTHING BELOW THIS LINE !!! ================== ##


def sawtoothnv(t, T, smin, smax):
    stnv = np.asarray([smin + (p / T - math.floor(p / T)) * (smax - smin) for p in t])
    return stnv


def sknv(t, k, T):
    sktempnv = np.asarray([-1**k * math.sin(2 * math.pi * k * (p - T / 2) / T) / (math.pi * k) for p in t])
    return sktempnv


def sawtoothapproxnv(t, kmax, T, smin, smax):
    tot = sum([sknv(t, k, T) for k in range(1, kmax + 1)])
    stappnv = -(smax - smin) * tot + (smin + smax) / 2
    return stappnv


def test1():
    tmin, tmax, tnum = 0, 7, 71
    t = np.linspace(tmin, tmax, tnum)
    T, smin, smax = 2, 3, 6
    return t, T, smin, smax


def test2():
    tmin, tmax, tnum = -3, +3, 601
    t = np.linspace(tmin, tmax, tnum)
    T, smin, smax = 1,1,+3
    return t, T, smin, smax


def main():
    try:
        student_id = sys.argv[0].split('/')[-1]
        student_id = re.match('([a-z]+[0-9]+)*_1', student_id)
        if not student_id:
            print("PLEASE CHANGE YOUR FILE NAME!")
            student_id = 'Anonymous'
    except:
        student_id = 'Anonymous'

    t, T, smin, smax = test1()
    s = sawtooth(t, T, smin, smax)
    plot_sawtooth(t, s, T, smin, smax, 'LabWeek4Test1Output.pdf')

    t, T, smin, smax = test2()
    kmax = 10
    s = sawtooth(t, T, smin, smax)
    a = sawtoothapprox(t, kmax, T, smin, smax)
    plot_sawtooth_approx(t, s, a, kmax, T, smin, smax, 'LabWeek4Test2Output.pdf')

    c = 0
    print('======== Problem 1 Results ========')
    tmin, tmax, tnum = 0, 7, 100000
    t1 = np.linspace(tmin, tmax, tnum)
    T, smin, smax = 2, 3, 6

    start_time1 = time.perf_counter()
    s = sawtooth(t1, T, smin, smax)
    time1 = time.perf_counter() - start_time1

    start_time2 = time.perf_counter()
    s1 = sawtoothnv(t1, T, smin, smax)
    time2 = time.perf_counter() - start_time2

    sdiff = np.std(s1 - s)
    print('Standard Deviation from the solution: ', sdiff)
    print('Running time of your code:        ', time1, 's')
    print('Running time of for-loop solution:', time2, 's')
    if sdiff < 0.01 and time1 < 0.1 * time2:
        print('Student_ID: ', student_id, '\nProblem 1 Grade: 10/10')
        c += 10
    else:
        print('Student_ID: ', student_id, '\nProblem 1 Grade: 0/10')
    print('======== Problem 2 Results ========')

    tmin, tmax, tnum = -3, +3, 1001
    t = np.linspace(tmin, tmax, tnum)
    T, smin, smax = 1, 1, 3
    s = sawtoothnv(t, T, smin, smax)
    kmax = 10

    start_time1 = time.perf_counter()
    a = sawtoothapprox(t, kmax, T, smin, smax)
    time1 = time.perf_counter() - start_time1

    start_time2 = time.perf_counter()
    sawtoothapproxnv(t, kmax, T, smin, smax)
    time2 = time.perf_counter() - start_time2

    sappdiff = np.std(a-s)
    print('Standard Deviation of the approximation function: ', sappdiff)
    print('Running time of your code:        ', time1, 's')
    print('Running time of for-loop solution:', time2, 's')
    if sappdiff < 0.18 and time1 < 0.1 * time2:
        print('Student_ID: ', student_id, '\nProblem 2 Grade: 10/10')
        c += 10
    else:
        print('Student_ID: ', student_id, '\nProblem 2 Grade: 0/10')

    print('======== Summary ========')
    print('Student_ID: ', student_id, '\nTotal Grade: ', str(c) + '/20')


if __name__ == "__main__":
    main()
