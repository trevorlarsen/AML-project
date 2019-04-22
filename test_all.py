from itertools import combinations
from functools import reduce
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt
import sys

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

n = t.shape[0]

sorted_t_inds = np.argsort(t)
# sorted_t = t[sorted_t_inds]
#
# barchart = plt.bar(range(n), sorted_t)
# plt.title("Clinton Advantage by Congressional District in Georgia")
# for i in range(n):
#     if sorted_t[i] < 0:
#         barchart[i].set_color('r')
# plt.savefig('Georgia_Districts.png')

num_to_defend = 4

S = k_bits_on(num_to_defend, n)

num_to_attack = 7

A = k_bits_on(num_to_attack, n)

# Test core lp

corelp_start = time.time()
x, y, p, w_s = corelp(A, S, t)
print("corelp time", time.time() - corelp_start)
#
# a = best_attack(x, S, t, num_to_attack)[0,:]
#
# sorted_w_s = w_s[sorted_t_inds]
# sorted_a = a[sorted_t_inds]
#
# print(p)
# print(sorted_w_s)
# print(sorted_a)

initial_sizes = [1, 4, 10, 20, 50, 100]
oracle_times = []
num_iterations = []

num_defenses = S.shape[0]
print("num defenses:", num_defenses)

num_attacks = A.shape[0]
print("num_attacks:", num_attacks)

# for initial_size in initial_sizes:
#     num_random_defenses = initial_size
#     random_defenses_inds = np.random.choice(num_defenses, num_random_defenses, replace=False)
#     initial_defenses = S[random_defenses_inds, :]
#
#
#     num_random_attacks = initial_size
#     random_attacks_inds = np.random.choice(num_attacks, num_random_attacks, replace=False)
#     initial_attacks = A[random_attacks_inds,:]
#
#     oracle_start = time.time()
#     x_oracle, a, p_oracle, num_its = double_oracle(initial_attacks, initial_defenses, t, num_to_attack, num_to_defend)
#
#     num_iterations.append(num_its)
#
#     oracle_time = time.time() - oracle_start
#     oracle_times.append(oracle_time)
#
#     print("num_its:", num_its)
#     print("oracle time", oracle_time)
#     print("p=", p_oracle)
#
#
# plt.plot(initial_sizes, oracle_times, marker="o")
# plt.title("Double Oracle Efficiency by Initial Size")
# plt.ylabel("Run Time")
# plt.xlabel("Initial Sizes")
# plt.savefig("oracle_times.png")
#
# plt.figure()
# plt.plot(initial_sizes, num_iterations, marker="o")
# plt.title("Double Oracle Iterations by Initial Size")
# plt.ylabel("Number of Iterations")
# plt.xlabel("Initial Sizes")
# plt.savefig("oracle_its.png")

# np.random.seed(99)
#
# num_random_defenses = 4
# random_defenses_inds = np.random.choice(num_defenses, num_random_defenses, replace=False)
# initial_defenses = S[random_defenses_inds, :]
#
#
# num_random_attacks = 4
# random_attacks_inds = np.random.choice(num_attacks, num_random_attacks, replace=False)
# initial_attacks = A[random_attacks_inds,:]
#
# oracle_start = time.time()
# x_oracle, a, p_oracle, num_its = double_oracle(initial_attacks, initial_defenses, t, num_to_attack, num_to_defend)
# oracle_time = time.time() - oracle_start
# print(oracle_time)
