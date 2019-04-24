import numpy as np

import docplex.mp.model as cpx
import time


def corelp(A, S, t):
    start_program = time.time()
    
    # number of defense strategies, j in range(m)
    m = S.shape[0]

    # number of attack strategies, k in range(l)
    l = A.shape[0]
    
    def election_winner(attack, defense):
        successful_attacks = attack * np.logical_not(defense)
        vote_happens = np.logical_not(successful_attacks)
        completed_votes = t[vote_happens]
        total_vote = np.sum(completed_votes)
        return total_vote < 0

    start_e = time.time()
    # E: If w wins election under attack A[k] and defense S[j]
    E = np.zeros((l,m))

    for k in range(l):
        for j in range(m):
            E[k,j] = election_winner(A[k], S[j])
            
    time_e = time.time() - start_e
    
    start_lp = time.time()
    
    model = cpx.Model(name="LP Model")
    

    x = { j : model.continuous_var(lb=0, ub=1, name="x_" + str(j)) for j in range(m) }

    p = model.continuous_var(name="p")


    constraints = {}
    
    model.add_constraint( model.sum( x[j] for j in range(m)) <= 1 )

    for k in range(l):
        constraints[k] = model.add_constraint( p <= model.sum( x[j] * E[k,j] for j in range(m) ) )
    



    model.maximize(p)

    # model.print_information()
    # print()

    model.solve()
    
    p = model.objective_value
    # print("Objective value: ", p)
    
    # print()
    # print("Defense values")
    # print()

    weighted_defense_array = np.zeros(S.shape)
    
    x_vector = np.zeros(m)
    
    for j in range(m):
        value = float(x[j])
        x_vector[j] = value
        weighted_defense_array[j,:] = S[j,:] * value
        #print(S[j,:] * value)
        
        #print(str(value) + ": " + str(S[j,:]))
    
    
    # print()
    # print("Attack values")
    # print()
    
    weighted_attack_array = np.zeros(A.shape)
    
    y_vector = np.zeros(l)
    y = model.dual_values(constraints.values())
    for k, y_value in enumerate(y):
        y_vector[k] = y_value
        weighted_attack_array[k,:] = A[k,:] * y_value
        #print(y_value, ":", A[k,:])
    
    weighted_defense_vector = np.sum(weighted_defense_array, axis=0)
    weighted_attack_vector = np.sum(weighted_attack_array, axis=0)
    #
    #
    # print(weighted_defense_vector)
    # print(weighted_attack_vector)
    
    # print("building E took", time_e)
    #
    # print("lp took", time.time() - start_lp)
    
    # print("full lp took", time.time() - start_program)
    
    return x_vector, y_vector, p, weighted_defense_vector


# def corelpsimp(A, t, m):
#
#         # m = number of defense resources
#
#         # number of attack strategies, k in range(l)
#         l = A.shape[0]
#
#         # number of districts, i in range(n)
#         n = A.shape[1]
#
#
#         model = cpx.Model(name="LP Model")
#
#
#         y = { i : model.continuous_var(lb=0, ub=1, name="y_" + str(i)) for i in range(n) }
#
#         p = model.continuous_var(name="p")
#
#
#
#         model.add_constraint( model.sum( y[i] for i in range(n)) <= m )
#
#
#         for k in range(l):
#             model.add_constraint( p <= model.sum( -t[i] * (1 - y[i] * A[k,i]) for i in range(n) ) )
#
#
#
#         model.maximize(p)
#
#         model.print_information()
#         print()
#
#         model.solve()
#
#         print("Objective value: ", model.objective_value, "\n")
#
#         for i in range(n):
#             value = float(y[i])
#             print(y[i], "=", str(value))