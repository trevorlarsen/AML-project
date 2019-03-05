# import itertools
# import pulp

# number of districts
n = 3

# number of strategies
m = 3

# t_i^(c-w); vote diffs; winners:[w, c, w]; goal: flip total vote to c
t = [-100, 50, -15]

# S: S_1 = {s_1, s_2, s_3}
S = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

# x_s: probability of defender choosing each strategy S.
x = [.5, .25, .25]

# max_attacks
k = 2
                        

import docplex.mp.model as cpx

model = cpx.Model(name="LP Model")

a = { i : model.binary_var(name="a_" + str(i)) for i in range(n) }

z = { j : model.binary_var(name="z_" + str(j)) for j in range(m) }

model.add_constraint( ct=model.sum( a[i] for i in range(n)) <= k )

for j in range(m):
    s = S[j]
    model.add_constraint( ct=model.sum( z[i] * t[i] * (1 - s[i]) * a[i] for i in range(n)) >= 0 ) 

objective = model.sum( (1 - z[j]) * x[j] for j in range(m))

model.minimize(objective)

model.print_information()

model.solve()

print("Objective value: ", model.objective_value, "\n")

print("Attack group(s):", end=' ')
for i in range(n):
    v = int(a[i])
    if v:
        print(i, end=' ')
    
print("\n")

for j in range(m):
    v = int(z[j])
    print(str(z[j]) + " = " + str(v))
    

print(model.sum( z[j] * t[i] * (1 - s[i]) * a[i] for i in range(n)))





