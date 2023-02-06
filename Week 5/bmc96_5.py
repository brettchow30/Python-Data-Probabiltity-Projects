
# ECE 105: Programming for Engineers II (Spring, 2019)
# Lab 5: Recursion
# May 2-3, 2019
# PLEASE rename this solution .py file as your "username_5.py" (e.g. cl982_5.py) before submission

import time
import matplotlib.pyplot as plt


# ---------------------------------------------------------
# Problem 1: Collatz sequences and Collatz sequence lengths
# TODO: line 48 - 1. Please complete the lc() and _lc() functions inside lcall()
#       line 86 - 2. Please complete the r() function
# ---------------------------------------------------------
# PLEASE note that we may use different n and nmax to test the accuarcy of your code.
# ---------------------------------------------------------

# Collatz function
def c(n):
    """

    :param n: (type: int)  -- the input of Collatz fuction
    :return: ans: (type: int) -- the value calculated from Collatz function. (i.e. c(2) = 1; c(3) = 10)
    """
    if n % 2:
        return 3 * n + 1
    else:
        return n / 2

# Collatz sequence lengths for n from 1 to nmax WITHOUT cache
def lnall(nmin, nmax):
    """

    :param nmin: (type: int) -- the lower bound of the list
    :param nmax: (type: int) -- the upper bound of the list
    :return: None
    """

    # length of Collatz sequence WITHOUT cache
    def ln(n):
        if n == 1:
            return 1
        else:
            return 1 + ln(c(n))

    for n in range(nmin, nmax+1): ln(n)


# Collatz sequence lengths for n from nmin to nmax WITH cache
def lcall(nmin, nmax):
    """

    :param nmin: (type: int) -- the lower bound of the list
    :param nmax: (type: int) -- the upper bound of the list
    :return: ans: (type: list) -- a collection of Collatz sequence lengths for numbers in nmax list.
    """

    # length of Collatz sequence WITH cache
    def lc(n):
        """

        :param n (type: int) --  the input of Collatz sequence length
        :return: cache (type: dict) -- the memoization of Collatz sequence length
        """

        ## YOUR CODE START HERE
        if n not in cache: cache[n] = _lc(n)
        
        return cache[n]

        ## YOUR CODE END HERE

        pass

    def _lc(n):
        """

        :param n: (type: int) --  the input of Collatz sequence length
        :return: ans (type: int) -- the length of Collatz sequence. (i.e. _lc(1) = 1, _lc(16) = 5)
        """
        ## YOUR CODE START HERE
        if n == 1: 
            return 1
        else: 
            return 1 + lc(c(n))

        ## YOUR CODE END HERE

        pass

    cache = {}
    for n in range(nmin, nmax + 1): lc(n)

    return [cache[n] for n in range(nmin, nmax + 1)]


# compute the ratio of running times for n from 1 to nmax WITHOUT / WITH cache
def r(nmaxv):
    """

    :param nmaxv (type : int) -- max value for Collatz sequence length calculation
    :return: tn (type: float) -- time cost WITHOUT cache in recursion
             tc (type: float) -- time cost WITH cache in recursion
             tn/tc (type: float) -- time ratio WITHOUT / WITH cache
    """
    ## YOUR CODE START HERE
    nmin = 1
    
    s = time.clock()
    lnall(nmin, nmaxv)
    f = time.clock()
    
    s1 = time.clock()
    lcall(nmin, nmaxv)
    f1 = time.clock()
    
    tn = f - s
    tc = f1 - s1
    
    
    #PLEASE SET nmin = 1 when use both lnall(nmin, nmax) and lcall(nmin, nmax) function in this problem.


    ## YOUR CODE END HERE

    return tc, tn, tn/tc

pmin, pmax = 0, 6
nmax = [10**p for p in range(pmin, pmax+1)]

# Generate dictionaries saving Collatz sequence length computing time for tc, tn, tn/tc
tc, tn, rnc =  {}, {}, {}

print('\n PLEASE WAIT... It may take some time...\n')
for nmaxv in nmax:
	tcv, tnv, rv = r(nmaxv)
	tc[nmaxv] = tcv
	tn[nmaxv] = tnv
	rnc[nmaxv] = rv

# Plot for running time comparing.
plt.figure()
plt.loglog(nmax,list(tn.values()),marker='o',label='without cache')
plt.loglog(nmax,list(tc.values()),marker='x',label='with cache')
plt.loglog(nmax,list(rnc.values()),marker='*',label='ratio without / with cache')
plt.legend()
plt.xlabel("nmax")
plt.ylabel("running time (seconds)")
plt.title("Collatz time for all n from 1 to nmax")
plt.savefig("LabWeek5Problem1Output.pdf")
plt.show()


# ---------------------------------------------------------
# Problem 2: Empirical CDF(ECDF) for numerical data
# TODO: line 149 - 1. Please complete the cslecdf()
# HINT: You may use the lcall(nmin, nmax) from Problem1 to calcualte Collatz sequence length
# ---------------------------------------------------------
# PLEASE note that we may use different nmin, nmax or seqlen to test the accuarcy of your code.
# ---------------------------------------------------------


# empirical CDF for numerical data (in a list)
def ecdf(data):
	# values: the set of distinct values found in the data
	vals = list(set(data))
	# tal: the tally of how many times each value occurs in data
	tal = {value : data.count(value) for value in vals}
	# pmf: the tally divided by the length of the data
	pmf = {value : tal[value]/len(data) for value in vals}
	# cum: the number of data points with value <= each value in data
	cum = {value : len([v for v in data if v <= value]) for value in vals}
	# cdf: the fraction of data points with value <= each value in data
	cdf = {value : cum[value]/len(data) for value in vals}
	# return all five objects
	return vals, tal, pmf, cum, cdf


def cslecdf(nmin, nmax, seqlen):
    """

    :param nmin: (type int) -- the begining of the query list for Collatz sequence length computation
    :param nmax: (type int) -- the end of the query list for Collatz sequence length computation
    :param seqlen: (type int) -- a specified point for ecdf observation. (i.e. in this case, we have 75, 139, 181)
    :return: cdf[preveseqlen]:(type float) --  cdf value with given seqlen.
    """

    ## YOUR CODE START HERE
    cum = len([v for v in lcall(nmin, nmax) if v <= seqlen])
    cdf = cum/len(lcall(nmin, nmax))
    return cdf

    ## YOUR CODE END HERE

    pass


# call ecdf method with the prime gaps list as the data
nmin, nmax = 1001, 2000
data = lcall(nmin, nmax)
vals, tal, pmf, cum, cdf = ecdf(data)

# print the empirical CDF using the above
print("empirical CDF\nval\ttal\tpmf\tcum\tcdf")
for value in sorted(vals):
    print("{:>2d}\t{:>2d}\t{:.3f}\t{:>3d}\t{:.3f}".format(value, tal[value], pmf[value], cum[value], cdf[value]))

# call the csl-ecdf
seqlentests = [75, 139, 181]
print("\noutput from the clsecdf function:")
print("csl-ecdf({},{},{}) = {}".format(nmin, nmax, seqlentests[0], cslecdf(nmin, nmax, seqlentests[0])))
print("csl-ecdf({},{},{}) = {}".format(nmin, nmax, seqlentests[1], cslecdf(nmin, nmax, seqlentests[1])))
print("csl-ecdf({},{},{}) = {}".format(nmin, nmax, seqlentests[2], cslecdf(nmin, nmax, seqlentests[2])))

# plot the empirical CDF
x = sorted(vals)  # the set of values in the data
y = sorted(list(cdf.values()))  # the set of CDF values for the data
plt.figure()
plt.plot(x, y, drawstyle='steps-post')
plt.xlabel("Collatz sequence lengths")
plt.ylabel("fraction of n with that sequence length or smaller")
plt.title("ECDF of the Collatz sequence lengths for n from {} to {}".format(nmin, nmax))
plt.savefig("LabWeek5Problem2Output.pdf")
plt.show()

#---------------------------------------
#  PLEASE DO NOT CHANGE THE CODE BELOW!
#---------------------------------------
import sys
import re
import os

def main():
    try:
        student_id = sys.argv[0].split('/')[-1]
        student_id = re.match('([a-z]+\d+)*_5', student_id)
        if not student_id:
            print("\n !! PLEASE CHANGE YOUR FILE NAME !!")
            student_id = 'Anonymous'
    except:
        student_id = 'Anonymous'

    if os.path.exists('LabWeek5Test.txt'):
        print("\n File Test!")
        with open('LabWeek5Test.txt') as file:
            line = file.read().split('\n')

        temp_list = []
        for l in line[0:3]:
            temp = l.split()
            temp_list.append([int(s) for s in temp])
        temp = line[-1].split()
        temp_list.append([float(s) for s in temp])
        pmin, pmax = 0, 3
        tar = temp_list[1]
        pre = lcall(temp_list[0][0], temp_list[0][1])
        seqlen1 = temp_list[2]
        tarlen = temp_list[3]
    else:
        print("\nLocal Test!")
        pmin, pmax = 0, 3
        tar = [1, 2, 8, 3, 6, 9, 17, 4, 20, 7]
        pre = lcall(1, 10)
        seqlen1 = [60, 149, 175]
        tarlen = [0.491, 0.959, 0.992]

    # Test for problem 1
    nmax = [10**p for p in range(pmin, pmax+1)]
    tn1, ts1, rns1 = r(nmax[0])
    print('\n PLEASE WAIT... It may take some time...\n')
    tn2, ts2, rns2 = r(nmax[-1])
    grade1 = 0
    if rns1<1 and rns2>1:
        grade1 = 5

    grade2 = 5
    for i in range(10):
        if tar[i] != pre[i]:
            grade2 = 0
            break
    # Test for problem 2
    grade3 = 10
    nmin, nmax = 1001, 2000
    for s in range(len(seqlen1)):
        if cslecdf(nmin, nmax, seqlen1[s]) != tarlen[s]:
            grade3 -= 3

    grade = grade1+grade2+grade3

    print('======== Summary ========')

    print('Problem 1 :\n ')
    print('Time test : ', str(grade1), ' / 5. Recursion WITH cache should run faster with more input data.')
    print('Accuracy test: ', str(grade2), ' / 5. Please check l(n) in Lab5 reading material.')
    print('Problem 2 :\n ')
    print('Accuracy test: ', str(grade3), ' / 10')
    print('Total : \n', str(grade), ' / 20')


if __name__ == "__main__":
	main()