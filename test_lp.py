from itertools import combinations
from functools import reduce
import numpy as np
import pandas as pd

from corelp import corelp
from aomilp import best_attack
from domilp import best_defense

def k_bits_on(k,n):
       one_at = lambda v,i:v[:i]+[1]+v[i+1:]
       list_ones = [list(reduce(one_at,c,[0]*n)) for c in combinations(range(n),k)]
       return np.array(list_ones)
      
districts_data = pd.read_csv('districts.csv')


state_chosen = districts_data[districts_data['State']=='GA']

diff_clinton_trump = np.array(state_chosen['Difference Clinton-Trump'])

t = diff_clinton_trump

n = t.shape[0]

print(t)


num_to_defend = 3

S = k_bits_on(num_to_defend, n)

num_to_attack = 5

A = k_bits_on(num_to_attack, n)

x, y = corelp(A, S, t)

best_attack(x, S, t, num_to_attack)

best_defense(y, A, t, num_to_defend)
