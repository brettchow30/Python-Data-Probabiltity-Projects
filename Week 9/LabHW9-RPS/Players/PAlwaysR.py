# Always rock 
# Bart: "Good old rock, nothing beats rock"
# Lisa: "Poor Bart, so predictable" 
import random

def strategy(history): 
    if not history:
        return random.choice(['R', 'P', 'S'])
    else:
        return history[-1][1]