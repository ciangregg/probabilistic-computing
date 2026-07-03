import numpy as np

# Build recombining tree for an optimal stopping problem

def build_recombining_tree(steps):
    nodes = [(t,j) for t in range(steps + 1) for j in range(t + 1)]
    edges = []
    
    for t in range(steps):
        for j in range(t + 1):
            edges.append(((t, j), (t + 1, j)))     # Down move
            edges.append(((t, j), (t + 1, j + 1))) # Up move
    return nodes, edges

t_steps = 2

nodes, edges = build_recombining_tree(t_steps)

u_vars = [("u", t, j) for (t, j) in nodes]
m_vars = [("m", t, j) for (t, j) in nodes if (t, j) != (0, 0)]
y_vars = [("y", t1, j1, t2, j2) for ((t1, j1), (t2, j2)) in edges]

var_all = u_vars + m_vars + y_vars
var_index = {var: i for i, var in enumerate(var_all)}

n = len(var_all)
Q = np.zeros((n, n))

print(f"number of variables: {n}")
print(f"Q matrix: {Q}")