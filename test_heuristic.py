from itertools import combinations
from functools import reduce
import numpy as np
import pandas as pd
import time

from corelp import corelp
from aomilp import best_attack
from domilp import best_defense
from aobetter import heuristic_attack
from dobetter import heuristic_defense
from double_oracle import double_oracle

#np.random.seed(100)

def k_bits_on(k,n):
       one_at = lambda v,i:v[:i]+[1]+v[i+1:]
       list_ones = [list(reduce(one_at,c,[0]*n)) for c in combinations(range(n),k)]
       return np.array(list_ones)
      
districts_data = pd.read_csv('districts.csv')


state_chosen = districts_data[districts_data['State']=='GA']

diff_clinton_trump = np.array(state_chosen['Difference Clinton-Trump'])

t = diff_clinton_trump

print(t.shape[0])

n = t.shape[0]

num_to_defend = 2

S = k_bits_on(num_to_defend, n)

num_to_attack = 3

A = k_bits_on(num_to_attack, n)

corelp_start = time.time()
x, y, p = corelp(A, S, t)
print("corelp time", time.time() - corelp_start)
print(p)

num_defenses = S.shape[0]
num_random_defenses = 10
random_defenses_inds = np.random.choice(num_defenses, num_random_defenses, replace=False)
initial_defenses = S[random_defenses_inds, :]

num_attacks = A.shape[0]
num_random_attacks = 10
random_attacks_inds = np.random.choice(num_attacks, num_random_attacks, replace=False)
initial_attacks = A[random_attacks_inds,:]

initial_x, initial_y, initial_p = corelp(initial_attacks, initial_defenses, t)

oracle_start = time.time()
x_oracle, a, p_oracle = double_oracle(initial_attacks, initial_defenses, t, num_to_attack, num_to_defend)
print("oracle time", time.time() - oracle_start)
print(p_oracle)

a = heuristic_attack(initial_defenses, initial_x, p, t, num_to_attack)

for i in range(initial_attacks.shape[0]):
    if (a == initial_attacks[i,:]).all():
        print(initial_attacks[i,:])
        print("equal")
        break

print(a)

if a is not None:
    new_initial_attacks = np.vstack((initial_attacks, a))

    new_x, new_y, new_p = corelp(new_initial_attacks, initial_defenses, t)
    print(new_p)

#s = heuristic_defense(initial_attacks, initial_y, p, t, num_to_defend)