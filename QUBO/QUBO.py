import numpy as np


#tweakable parameters
a=100
alpha ,  beta ,gamma ,sigma = a, a , a, a



# build our none combining tree for an optimal stopping problem
'''     
           (0,0)
      (1,0)      (1,1)
  (2,0) (2,1) (2,2) (2,3)
  
(t,0)      (t,j)    (t,2^t-1)
'''
def build_tree(steps):
    nodes=[]
    edges=[]
    
    for t in range(steps + 1):
        for j in range(2**t):
            nodes.append((t,j))
    
    for t in range(steps):
        for j in range(2**t):
            left_child = (t + 1, 2 * j)
            right_child = (t + 1, 2 * j + 1)
            
            edges.append(((t, j), left_child))   # Left move
            edges.append(((t, j), right_child))  # Right move
    return nodes, edges 

nodes, edges = build_tree(1)

print("Nodes:", nodes)

for edge in edges:
    print("Edge:", edge)


vars_index={}
k=0
#sell variables
for node in nodes:
    vars_index[("s", node)]=k
    k+=1
#memory variables

for node in nodes:
    vars_index[("m", node)]=k
    k+=1 

for edge in edges:
    vars_index[("y", edge)] = k
    k += 1
    
print (f"vars_index: {vars_index}")

var_all = list(vars_index.keys())
n = len(var_all)
Q = np.zeros((n, n))
print(f"Q matrix shape: {Q.shape}")

#reward for selling at node (t,j)  
prices = {
    (0,0): 5,
    (1,0): 12,   # U
    (1,1): 2,    # D
    (2,0): 25,   # UU
    (2,1): 8,    # UD
    (2,2): 8,    # DU
    (2,3): 0     # DD
}


# make Q_{i,i} 
Ns = len(nodes)
Nm = len(nodes)
Ny = len(edges)

Q11 = np.zeros((Ns,Ns))
Q12 = np.zeros((Ns,Nm))
Q13 = np.zeros((Ns,Ny))

Q22 = np.zeros((Nm,Nm))
Q23 = np.zeros((Nm,Ny))

Q33 = np.zeros((Ny,Ny))

for k,node in enumerate(nodes):
    p = prices[node]

    Q11[k,k] += -p
    Q12[k,k] += p + alpha
    
#print(f"Q11: {Q11}")
#print(f"Q12: {Q12}")

# now build the QUBO matrix Q
# E_\text{payyoff}= -\sum_{t,j}s_{t,j}(1-m_{t,j}) P_{t,j}
# E_payyoff + E_stopeed = -sp +ms(p+alpha)

for node in nodes:

    p = prices[node]

    s = vars_index[("s", node)]
    m = vars_index[("m", node)]

    # -P*s
    Q[s, s] += -p

    # +(P+alpha)*s*m
    Q[s, m] += p/2 + alpha/2
    Q[m, s] += p/2 + alpha/2
    

#E OR  -- gamma * (2*y*s_p - 2*y - 2*m_c*s_p - m_p*s_p + m_c + m_p + s_p)
for (parent, child) in edges:

    s_parent = vars_index[("s", parent)]
    m_parent = vars_index[("m", parent)]
    m_child  = vars_index[("m", child)]
    y_edge   = vars_index[("y", (parent, child))]

    # linear terms: +s_p +m_p +m_c -2y
    Q[s_parent,s_parent] += beta
    Q[m_parent,m_parent] += beta
    Q[m_child,m_child]   += beta
    Q[y_edge,y_edge]     += -2*beta

    # +2*y*s_p
    Q[y_edge,s_parent] += beta
    Q[s_parent,y_edge] += beta

    # -2*m_c*s_p
    Q[m_child,s_parent] += -beta
    Q[s_parent,m_child] += -beta

    # -m_p*s_p
    Q[m_parent,s_parent] += -beta/2
    Q[s_parent,m_parent] += -beta/2

# E Rosenberg 

for (parent, child) in edges:

    m_parent = vars_index[("m", parent)]
    m_child  = vars_index[("m", child)]
    y_edge   = vars_index[("y", (parent, child))]

    Q[m_parent,m_child] += gamma/2
    Q[m_child,m_parent] += gamma/2

    Q[m_child,y_edge] += -gamma
    Q[y_edge,m_child] += -gamma

    Q[m_parent,y_edge] += -gamma
    Q[y_edge,m_parent] += -gamma

    Q[y_edge,y_edge] += 3*gamma


#E Bc
m00 = vars_index[("m",(0,0))]
Q[m00,m00] += sigma


print(f"Q matrix: {Q}")
