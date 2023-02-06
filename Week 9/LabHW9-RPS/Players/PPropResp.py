# Choose action based upon frequency of play of each action by opponent
import random
def strategy(history): 
	if not history: return random.choice(['R','P','S'])
	else:
		# list of opponent responses
		opp = [game[1] for game in history]
		# count the number of times opponent played each of R, P, S
		nR, nP, nS = opp.count('R'),  opp.count('P'), opp.count('S')
		# divide by number of games to get frequency of playing R, P, S
		fR, fP, fS = nR/len(opp), nP/len(opp), nS/len(opp)
		# make random choice using weights / probabilities (fR, fP, fS)
		# choose R based upon fraction of time opponent played S
		# choose P based upon fraction of time opponent played R
		# choose S based upon fraction of time opponent played P
		return random.choices(['R', 'P', 'S'], weights=[fS, fR, fP])[0]