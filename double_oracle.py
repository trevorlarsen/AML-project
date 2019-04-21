import numpy as np

from corelp import corelp
from aomilp import best_attack
from domilp import best_defense
from aobetter import heuristic_attack
from dobetter import heuristic_defense

def double_oracle(A_p, S_p, t, num_to_attack, num_to_defend):
    
    while True:
        
        x, y, p = corelp(A_p, S_p, t)
        
        a = heuristic_attack(S_p, x, p, t, num_to_attack)
        if a is None:
            print("exact attack")
            a = best_attack(x, S_p, t, num_to_attack)
        else:
            print("heurisic attack")

        s = best_defense(y, A_p, t, num_to_defend)
        
        a_in = False
        for i in range(A_p.shape[0]):
            if (a == A_p[i,:]).all():
                a_in = True
                break
        
        s_in = False
        for i in range(S_p.shape[0]):
            if (s == S_p[i,:]).all():
                s_in = True
                break
                
        if a_in and s_in:
            return x, a, p
        
        A_p = np.vstack((A_p, a))
        S_p = np.vstack((S_p, s))
        