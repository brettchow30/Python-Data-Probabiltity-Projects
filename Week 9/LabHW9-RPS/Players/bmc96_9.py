import random
def strategy(history):
    if not history:
        return random.choice(['R', 'S', 'P'])
    
    else:
        opp = [game[1] for game in history]
        myop = [b[0] for b in history]
        nR, nP, nS = opp.count('R'), opp.count('P'), opp.count('S')
        mR, mP, mS = myop.count('R'), opp.count('P'), opp.count('S')
        fR, fP, fS = nR/len(opp), nP/len(opp), nS/len(opp)
        pR, pP, pS = mR/len(myop), mP/len(myop), mS/len(myop)
        
        if max(fR, fP, fS) == fR:
            if max(pR, pP, pS) == pR:
                return 'P'
            elif history[-1][1] == 'R':
                    return 'R'
            elif history[-1][0] == 'R': return 'S'
            
            else: return 'P'
            
        elif max(fR, fP, fS) == fP:
            if max(pR, pP, pS) == pP:
                return 'S'
            if history[-1][1] == 'R':
                return 'R'
            elif history[-1][0] == 'P': return 'R'
            
            else: return 'S'
            
        else:
            if max(pR, pP, pS) == pS:
                return 'R'
            elif history[-1][1] == 'P':
                    return 'P'
            elif history[-1][0] == 'S': return 'P'
            
            else: return 'R'
        
        
            
       
        