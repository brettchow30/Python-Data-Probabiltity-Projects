# Choose action to beat opponent's last play
import random
def strategy(history): 
	if not history: return random.choice(['R','P','S'])
	else:
		if history[-1][1] == 'R': return 'P'
		elif history[-1][1] == 'P': return 'S'
		else: return 'R'