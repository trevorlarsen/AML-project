# Defense best response to randomized attack


# number of districts, i in range(n)
n = 3

# number of strategies, j in range(m)
m = 3

# t_i^(c-w); vote diffs; winners:[c, c, w]; goal: flip total vote to c
t = [100, 50, -1500]

# A: A[j] = attack strategy j; A[j][i] = whether district i is attacked under strategy j
A = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

# y: probability of attacker choosing each strategy a.
y = [.2, .2, .6]

# max defenses
l = 1
                        

import docplex.mp.model as cpx

model = cpx.Model(name="LP Model")



s = { i : model.binary_var(name="s_" + str(i)) for i in range(n) }

z = { j : model.binary_var(name="z_" + str(j)) for j in range(m) }

v = { (i,j) : model.binary_var(name="v_" + str(i) + "_" + str(j)) for i in range(n) for j in range(m) }



model.add_constraint( model.sum( s[i] for i in range(n)) <= l )

for j in range(m):
    a = A[j]
    model.add_constraint( model.sum( z[j] * t[i] * (1 - a[i]) + v[i,j] * t[i] * a[i] + z[j] for i in range(n) ) <= 0 )

for i in range(n):
    for j in range(m):
        model.add_constraint( v[i,j] <= z[j] )
        model.add_constraint( v[i,j] <= s[i] )
        model.add_constraint( v[i,j] >= z[j] + s[i] - 1 )
        
        

objective = model.sum( z[j] * y[j] for j in range(m) )




model.maximize(objective)

model.print_information()
print()

model.solve()

print("Objective value: ", model.objective_value, "\n")

print("Defend group(s):", end=' ')
for i in range(n):
    value = int(s[i])
    if value:
        print(i, end=' ')
    
print("\n")

for j in range(m):
    value = int(z[j])
    print(str(z[j]) + " = " + str(value))
    
for i in range(n):
    for j in range(m):
        value = int(v[i,j])
        print(str(v[i,j]) + " = " + str(value))