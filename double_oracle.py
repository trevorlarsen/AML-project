import numpy as np

from corelp import corelp
from aomilp import best_attack
from domilp import best_defense
from aobetter import heuristic_attack
from dobetter import heuristic_defense

def double_oracle(A_p, S_p, t, num_to_attack, num_to_defend):
    
    heuristic_attacks = 0
    exact_attacks = 0
    
    heuristic_defenses = 0
    exact_defenses = 0
    
    num_its = 0
    
    while True:
        
        x, y, p, _ = corelp(A_p, S_p, t)
        
        a = heuristic_attack(S_p, x, p, t, num_to_attack)
        #a = None
        if a is None:
            exact_attacks += 1
            a = best_attack(x, S_p, t, num_to_attack)
        else:
            heuristic_attacks += 1

        s = heuristic_defense(A_p, y, p, t, num_to_defend)
        #s = None
        if s is None:
            exact_defenses += 1
            s = best_defense(y, A_p, t, num_to_defend)
        else:
            heuristic_defenses += 1
        
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
            print("Heuristic defenses:", heuristic_defenses)
            print("Exact defenses:", exact_defenses)
            
            print("Heuristic attacks:", heuristic_attacks)
            print("Exact attacks:", exact_attacks)
            
            return x, a, p, num_its
        
        A_p = np.vstack((A_p, a))
        S_p = np.vstack((S_p, s))
        
        num_its += 1
        