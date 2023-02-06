import sys
import re
import matplotlib.pyplot as plt

######### HINT: These libraries are useful ########
from math import log, exp
from collections import Counter
from scipy import stats
import numpy as np


def ZipfLaw_coef(wfl):
    """
    wfl (list of int): word counts (the occurrence of words,
                                    sorted by frequency in descending order)

    Recall this becomes (pseudo-code): log_n(y) = log_n(b) + m * log_n(x)
    The above regression holds:        log_n(b) == intercept; m == slope
    Thus, the regression line has:     b == exp(intercept)
    """

    ############# CODE START ############
    # generate x, y from wfl
    x = range(1, len(wfl) + 1) # placeholder
    y = [i / sum(wfl) for i in wfl] # placeholder
    logx = [log(x[i]) for i in range(len(x))]
    logy = [log(y[i]) for i in range(len(y))]
    # calculate (1) the slope (m) and (2) the intercept
    # from the above equations by using stats.linregress from SciPy
    slope, intercept, r_value, p_value, std_err = stats.linregress(logx, logy)
    #############  CODE END  ############

    # return x, y, slope, b
    return x, y, slope, exp(intercept)


def ZipfLaw_plot(x, y, slope, intercept, outputFileName):
    """
    x (list of int):          1,...,len(y)
    y (list of float):        normalized frequencies
    slope (numpy.double):     slope of the linear regression line
    intercept (numpy.double): intercept of the linear regression line
    outputFileName (str):     the file name of the resultant figure
    """
    plt.figure()
    

    # REVIEW THE WIKI ON LOG-LOG PLOTS:
    # https://en.wikipedia.org/wiki/Log–log_plot

    ############# CODE START ############
    # Plot the data on the same graph
    
    plt.loglog(x, y, label = 'Original Values')
    plt.loglog(x, intercept*x**slope, label = 'Regression Line')
    
    # 1. log-log plot of the data
    # 2. the regression line, y = b * x**m
    #############  CODE END  ############

    plt.title("freq. of {} words, regresssion has intercept = {:.2f}, slope = {:.2f}".format(len(y),intercept,slope))
    plt.xlabel('word frequency index')
    plt.ylabel('normalized word frequency')
    plt.legend()
    plt.savefig(outputFileName)
    plt.show()


def Mandelbrot_model(sentence, minFreqForTop = 10):
    """
    sentence (str):      a single long string with letters and spaces
    minFreqForTop (int): only keep words with occurrence > minFreqForTop
    """

    ############# CODE START ############
    x = sentence.split()
    lista = [x.count(i) for i in list(set(x))]
    finallist = []
    
    for i in lista:
        if i > minFreqForTop:
            finallist.append(i)
            
    wordCounts = finallist
    wordCounts.sort()
    wordCounts.reverse()
    
     # placeholder
    #############  CODE END  ############

    # return the word counts (sorted from largest to smallest - descending order)
    return wordCounts


  ## ================== !!! DO NOT CHANGE ANYTHING BELOW THIS LINE !!! ================== ##
 ## ---------------------------------------------------------------------------------------##
## ANY change made below will be considered as INVALID submission and will receive 0 POINTS ##
 ## ---------------------------------------------------------------------------------------##
  ## ================== !!! DO NOT CHANGE ANYTHING BELOW THIS LINE !!! ================== ##

def Mandelbrot_write(wordCounts, outputFileName):
    file = open(outputFileName, "w")
    file.write('\n'.join(str(x) for x in wordCounts))
    file.close()


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else ''
    try:
        student_id = sys.argv[0].split('/')[-1]
        student_id = re.match('([a-z]+\d+)*_1', student_id)
        if not student_id:
            print("PLEASE CHANGE YOUR FILE NAME!")
            student_id = 'Anonymous'
    except:
        student_id = 'Anonymous'
    if mode != 'GX':
        c = 0
        print('======== Problem 1 Results ========')
        inputFileName = 'LabWeek3Problem1Input.txt'
        outputFileName = 'LabWeek3Problem1Plot.pdf'
        wfl = list(map(lambda x : int(str.split(x)[0]), open(inputFileName)))
        target_m, target_b = '-1.12', '0.24'
        x, y, slope, intercept = ZipfLaw_coef(wfl)
        m = "{0:.2f}".format(slope)
        b = "{0:.2f}".format(intercept)
        if m == target_m and b == target_b:
            print('Student_ID: ', student_id, '\nProblem 1 Grade: 10/10')
            c += 10
        else:
            print('Student_ID: ', student_id, '\nProblem 1 Grade: 0/10')
        ZipfLaw_plot(x, y, slope, intercept, outputFileName)
        print('======== Problem 2 Results ========')
        target_m, target_b = '-1.03', '0.16'
        with open('LabWeek3Problem2Input.txt') as f:
            sentence = f.readline().strip('\n')
        wordCounts = Mandelbrot_model(sentence)
        Mandelbrot_write(wordCounts, outputFileName = 'LabWeek3Problem2Output.txt')
        inputFileName = 'LabWeek3Problem2Output.txt'
        wfl = list(map(lambda x : int(str.split(x)[0]), open(inputFileName)))
        x, y, slope, intercept = ZipfLaw_coef(wfl)
        m = "{0:.2f}".format(slope)
        b = "{0:.2f}".format(intercept)
        if m == target_m and b == target_b:
            print('Student_ID: ', student_id, '\nProblem 2 Grade: 10/10')
            c += 10
        else:
            print('Student_ID: ', student_id, '\nProblem 2 Grade: 0/10')
        ZipfLaw_plot(x, y, slope, intercept, outputFileName = 'LabWeek3Problem2Output.pdf')
        print('======== Summary ========')
        print('Student_ID: ', student_id, '\nTotal Grade: ', str(c) + '/20')
    else:
        c = 0
        t = 20
        inputFileName = 'LabWeek3Problem2Output.txt'
        wfl = list(map(lambda x : int(str.split(x)[0]), open(inputFileName)))
        target_m, target_b = list(map(lambda x : str.split(x)[0], open('GX_%d.txt' % 0)))
        try:
            _, _, m, b = ZipfLaw_coef(wfl)
            m = "{0:.2f}".format(m)
            b = "{0:.2f}".format(b)
            if target_m == m and target_b == b:
                c += 10
        except:
            c += 0
        try:
            with open('LabWeek3Problem2Input.txt') as f:
                sentence = f.readline().strip('\n')
            wordCounts = Mandelbrot_model(sentence)
            inputFileName = 'LabWeek3Problem2Output.txt'
            wfl = list(map(lambda x : int(str.split(x)[0]), open(inputFileName)))
            for i in range(10):
                if wfl[i] == wordCounts[i]:
                    c += 1
        except:
            c += 0
        print('======== Summary ========')
        print('Student_ID: ', student_id, '\nGrade: ', c/t*20)


if __name__ == "__main__":
    main()
