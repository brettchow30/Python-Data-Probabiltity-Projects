import numpy as np
from scipy.special import comb
import matplotlib.pyplot as plt
import math

# ECE 105: Programming for Engineers II (Spring, 2019)
# Lab 2, Problem 1, Part 1
# April 11-12, 2019

outputFileName = 'LabWeek2Problem1Part1Plot.pdf'
n = 100
x = range(n)
a = [np.math.factorial(k) for k in x]
b = [comb(2*n, k) for k in x]
c = [2**k for k in x]

plt.figure()
plt.yscale('log')
plt.plot(x,a,label='factorial')
plt.plot(x,b,label='central binomial coefficient')
plt.plot(x,c,label='power of two')
plt.title('factorial, central binomial coefficient, and power of two sequences')
plt.xlabel('sequence index k')
plt.ylabel('sequence value')
plt.legend()
plt.savefig(outputFileName)
plt.show()
