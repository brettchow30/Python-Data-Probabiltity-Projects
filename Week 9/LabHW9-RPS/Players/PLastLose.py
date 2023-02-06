# Choose action to lose to opponent's last play
import random
def strategy(history): 
	if not history: return random.choice(['R','P','S'])
	else:
		if history[-1][1] == 'R': return 'S'
		elif history[-1][1] == 'P': return 'R'
		else: return 'P'