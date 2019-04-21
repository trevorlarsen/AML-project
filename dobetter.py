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
        
        strategies = initial_attacks[array_inds,:]
        print(strategies)
        