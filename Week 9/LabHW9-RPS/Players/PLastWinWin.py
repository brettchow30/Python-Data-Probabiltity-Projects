# Choose action presuming opponent plays "LastWin" strategy
import random
def strategy(history): 
	if not history: return random.choice(['R','P','S'])
	else:
		# if I last played 'R', then LastWin would play 'P', so I play 'S'
		if history[-1][0] == 'R': return 'S'
		# if I last played 'P', then LastWin would play 'S', so I play 'R'
		elif history[-1][0] == 'P': return 'R'
		else: return 'P'