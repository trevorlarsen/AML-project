import numpy as np
from itertools import chain, combinations

def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def heuristic_defense(initial_attacks, y, p, t, num_to_defend):
    non_zero = np.where(y>0)[0]
    all_subsets = powerset(non_zero)
    for inds in all_subsets:
        if inds==(): continue
        array_inds = np.array(inds)
        A_pp = y[array_inds]
        if np.sum(A_pp) <= p: continue
                
        attacks = initial_attacks[array_inds,:]
        # if you are able to defend against all of these attacks, with a strategy s, then that is a better strategy

        attack_any = np.any(attacks, axis=0)
        
        t_sorted_inds = np.argsort(t)
        t_sorted = t[t_sorted_inds]
        
        attack_any_sorted = attack_any[t_sorted_inds]
        
        inds_to_delete = []
        for i in range(t_sorted.shape[0]):
            
            a_i = attack_any_sorted[i]
            if a_i:
                inds_to_delete.append(i)
                
            if len(inds_to_delete) == num_to_defend:
                break
        
        t_sorted[inds_to_delete] = 0
        if np.sum(t_sorted) < 0:
            original_inds = t_sorted_inds[inds_to_delete]
            
            s = np.zeros(initial_attacks.shape[1])
            s[original_inds] = 1
            return s
    
    return None
        
        