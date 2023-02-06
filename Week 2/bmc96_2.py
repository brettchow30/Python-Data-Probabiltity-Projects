from math import log10
from math import log10,floor
import numpy as np
import matplotlib.pyplot as plt

# ECE 105: Programming for Engineers II (Spring, 2019)
# Lab 2, Problem 2, Part 1
# April 11-12, 2019
# PLEASE rename this solution .py file as your "username_2.py" (e.g. spw26_2.py) before submission

# generate the sequence of factorials (a1,...,an) where ak = k!
def factSeq(n):
    return [np.math.factorial(k) for k in range(1,n+1)]

# given any array (a1,...,an), return (f1,...,f9)
# where fd is the fraction of numbers in array with first digit d
def benford(a): 
  # TODO Return the correct array (f1,...,f9)
  b = [(int(str(i)[0])) for i in a]
  c = [b.count(d) / n for d in range(1,10)]
# expected number of each leading digit per Benford's law
  return c

# aggregate relative error between f and p  
def error(f,p): 
  return sum([abs(f[d]-p[d])/p[d] for d in range(9)])
  
# print a summary of the results
def benTable(f,p):
  print("dig\temp\tpred\terr")
  print("----\t----\t----\t----")
  for d in range(9):
    print("{}\t{:.2f}\t{:.2f}\t{:.2f}\t".format(d+1,f[d],p[d],abs(f[d]-p[d])/p[d]))
  print("----\t----\t----\t----")
  ret = error(f,p)
  print("tot\t{:.2f}\t{:.2f}\t{:.2f}".format(sum(f),sum(p),ret))
  return ret
  
# Create two bar plots 
# f holds the empirical frequencies
# p holds the frequencies predicted by Benford's Law
def benPlot(f,p,outputFileName):
  plt.figure()
  barwidth = 0.15
  pb_xvals = [d + barwidth for d in range(1,10)]
  # TODO Fill in XVAL and YVAL
  fb = plt.bar(range(1,10), f, barwidth, color='r') # empirical bars
  pb = plt.bar(pb_xvals, p, barwidth, color='b') # predicted bars
  plt.title('Benford Law for first digits in factorials')
  plt.xlabel('first digit')
  plt.xticks(np.arange(1, 10, step=1))
  plt.ylabel('fraction of factorials starting with digit')
  plt.legend((fb[0],pb[0]),('empirical', 'predicted')) # legend
  plt.savefig(outputFileName)
  plt.show()

#---------------------------------------
#  PLEASE DO NOT CHANGE THE CODE BELOW!
#---------------------------------------
n = 1000 # sequence length
def main():
  import sys
  import re
  try:
    student_id = sys.argv[0].split('/')[-1]
    student_id = re.match('([a-z]+\d+)*_2', student_id)
    if not student_id:
      print("PLEASE CHANGE YOUR FILE NAME!")
      student_id = "None"
  except:
    student_id = "None"
  a = factSeq(n) # factorials (a1,...,an) with ak = k!
  f = benford(a) # empirical data (f1,...,f9), fd is fraction starting with d
  p = [log10(1+1/d) for d in range(1,10)] # Benford's Law prediction (p1,...,p9)
  e = benTable(f,p) # print the results in a text table
  try:
    outputFileName = 'LabWeek2Problem2Plot.pdf' # plot will be saved here
    benPlot(f,p,outputFileName) # plot (f,p) using matplotlib as pair of bar charts
  except:
    print("THE ERROR HERE IS BECAUSE YOU NEED TO FILL OUT benPlot!\n")
  grade = floor(20-(e-0.67)/9.0*20)
  print('======== Summary ========')
  print('Student_ID: {}\nGrade: {}'.format(student_id, grade))

if __name__ == "__main__":
  main()
