import numpy as np
import random

# ECE 105: Programming for Engineers II (Spring, 2019)
# Lab 1: DNA Word Search
# April 4-5, 2019
# PLEASE rename this solution .py file as your "username_1.py" (e.g. cl982_1.py) before submission

#
# COMPLETE THE FIND FUNCTION BELOW
#
# return True if word in A, else False
A = np.array(list(map(str.split, open('LabWeek1InputArray.txt'))))

def find(word):
    Ar = A.tolist()
    Ac = np.transpose(A).tolist()
    Af = np.fliplr(A)
    
    word1 = ''.join(word)
    reverseword1 = reversed(word)
    word2 = ''.join(reverseword1)
    
    for row in Ar:
        if word1 in ''.join(row):
            return True
    
    for col in Ac:
        if word1 in ''.join(col):
            return True
    
    for rowback in Ar:
        if word2 in ''.join(rowback):
            return True
    
    for colback in Ac:
        if word2 in ''.join(colback):
            return True

    for x in range(len(A)):
        antid1 = ''.join(np.diagonal(Af, x))
        if word1 in antid1 or word1 in antid1[::-1]:
            return True
    
    for y in range(len(A)):
        d1 = ''.join(np.diagonal(A, y))
        if word1 in d1 or word1 in d1[::-1]:
            return True
        
    for y in range(len(A)):
        d1 = ''.join(np.diagonal(A, -y))
        if word1 in d1 or word1 in d1[::-1]:
            return True
        
    for x in range(len(A)):
        antid1 = ''.join(np.diagonal(Af, -x))
        if word1 in antid1 or word1 in antid1[::-1]:
            return True

	# YOUR CODE END HERE

	# default return False
    return False


#---------------------------------------
#  PLEASE DO NOT CHANGE THE CODE BELOW!
#---------------------------------------
def main():
	import sys
	import re
	try:
		student_id = sys.argv[0].split('/')[-1]
		student_id = re.match('([a-z]+\d+)*_1', student_id)
		if not student_id:
			print("PLEASE CHANGE YOUR FILE NAME!")
			student_id = 'Anonymous'
	except:
		student_id = 'Anonymous'

	# import the array (A) from file "LabWeek1InputArray.txt"
	# import the list (L) from file LabWeek1InputList.txt"
	L = np.array(list(map(str.split,open('LabWeek1InputList.txt'))))

	# import the list (T) of target outputs from file "LabWeek1TargetOutput.txt"
	T0 = np.array(list(map(str.split,open('LabWeek1TargetOutput.txt'))))

	# Convert the string "True" to the boolean True, and "False" to the boolean False
	T = list(map(lambda x : True if x == "True" else False, T0))

	# print the results:
	# i: index
	# tar: target
	# res: result
	# cor: correct or incorrect
	print('======== Results ========')
	print("i tar   res   cor")

	c = 0
	t = 0
	for i, test_case in enumerate(L):
		t += 1
		try:
			res = find(test_case)
			cor = "Correct" if T[i] == res else "Incorrect"
			print("{} {} {} {}".format(i, T[i], res, cor))
			if res == T[i]:
				c += 1
		except:
			continue
	print('======== Summary ========')
	print('Student_ID: ', student_id, '\nGrade: ', c/t*20)


if __name__ == "__main__":
	main()