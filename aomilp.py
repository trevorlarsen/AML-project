# # Attack best response to randomized defense
import time
import numpy as np
#
#
# # number of districts, i in range(n)
# n = 3
#
# # number of strategies, j in range(m)
# m = 3
#
# # t_i^(c-w); vote diffs; winners:[c, c, w]; goal: flip total vote to c
# t = [100, 50, -1500]
#
# # S: S[j] = defense strategy j; S[j][i] = whether district i is defended under strategy j
# S = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
#
# # x: probability of defender choosing each strategy s.
# x = [.2, .2, .6]
#
# # max_attacks
# k = 1
                        

import docplex.mp.model as cpx

def best_attack(x, S, t, k):
    start_program = time.time()

    m, n = S.shape
    
    model = cpx.Model(name="LP Model")

    a = { i : model.binary_var(name="a_" + str(i)) for i in range(n) }

    z = { j : model.binary_var(name="z_" + str(j)) for j in range(m) }

    v = { (i,j) : model.binary_var(name="v_" + str(i) + "_" + str(j)) for i in range(n) for j in range(m) }

    model.add_constraint( model.sum( a[i] for i in range(n)) <= k )

    # for j in range(m):
    #     s = S[j]
    #     model.add_constraint( model.sum( z[j] * t[i] * (1 - s[i]) * a[i] for i in range(n)) >= 0 )

    for j in range(m):
        s = S[j]
        model.add_constraint( model.sum( z[j] * t[i] - (1 - s[i]) * v[i,j] * t[i] for i in range(n) ) >= 0 )

    for i in range(n):
        for j in range(m):
            model.add_constraint( v[i,j] <= z[j] )
            model.add_constraint( v[i,j] <= a[i] )
            model.add_constraint( v[i,j] >= z[j] + a[i] - 1 )

    objective = model.sum( (1 - z[j]) * x[j] for j in range(m) )

    model.minimize(objective)

    # model.print_information()
    # print()

    model.solve()
        
    a_return = []
    for i in range(n):
        value = int(a[i])
        a_return.append(value)

    return np.array(a_return).reshape((1, np.array(a_return).shape[0]))

    # print("Objective value: ", model.objective_value, "\n")
    #
    # print("Attack group(s):", end=' ')
    # for i in range(n):
    #     value = int(a[i])
    #     if value:
    #         print(i, end=' ')
    
    # print("\n")
    #
    # print("aomilp took", time.time() - start_program)

    # for j in range(m):
    #     value = int(z[j])
    #     print(str(z[j]) + " = " + str(value))
    #
    # for i in range(n):
    #     for j in range(m):
    #         value = int(v[i,j])
    #         print(str(v[i,j]) + " = " + str(value))
#
#
# print(model.sum( z[j] * t[i] * (1 - s[i]) * a[i] for i in range(n)))





