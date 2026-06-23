import numpy as np

#1 pick an initial state s^(0)=(1,1,...,1) and set t=0
#2 pick a new state s' by flipping a random bit of s^(t)
#3 calculate the energy difference ΔE=E(s')-E(s^(t))
#4 calculate the acceptance probability a=min(1,exp(-ΔE/T))
# 5 generate a random number u from the uniform distribution on [0,1]
#6 accept or reject, if u<a, then s^(t+1)=s', otherwise s^(t+1)=s^(t)
#7 repeat steps 2-6 for a fixed number of iterations or until convergence
#8 return the final configurations of the system s^(t)


def energy(s, J, h):
    return -0.5 * np.sum(J * np.outer(s, s)) - np.sum(h * s)

def metropolis_ising(J, h, T, steps=1000):
    seq=[]
    N = len(h)          # get size from h
    s = np.ones(N)      # initial state: all spins up
    
    for t in range(steps):  
        r=np.random.randint(0, N)  # pick a random spin to flip
        s_prime = s.copy()
        if s[r] == 1:
            s_prime[r] = -1  # flip the spin
            seq.append(s_prime)
        else:
            s_prime[r] = 1  # flip the spin
            seq.append(s_prime)
        
        deltaE=energy(s_prime, J, h) - energy(s, J, h)  # calculate the energy difference     
        a=min(1, np.exp(-deltaE/T))  # calculate the acceptance probability
        
        if np.random.rand() < a:  # accept or reject
            s = s_prime  # accept the new state 
        else:
            s = s  # reject the new state, keep the old state   
    # remove the first 100 samples as burn-in
    seq=seq[100:]
    return s , seq


T=1.0  # temperature
N=4   # number of spins
def J_random(N):
    J = np.random.randn(N, N)  # 10x10
    J = (J + J.T) / 2          # make it symmetric (Jij = Jji)
    np.fill_diagonal(J, 0)     # no self-interactions
    return J

def J_1(N):
    J = np.ones((N, N))  # 10x10
    J = (J + J.T) / 2          # make it symmetric (Jij = Jji)
    np.fill_diagonal(J, 0)     # no self-interactions
    return J

# length 10

#J=J_random(N)
J=J_1(N)
h = np.zeros(N)
#
print("J matrix:")
print(J)
#
print("h vector:")
print(h)
#
print("Final state:")   
print(metropolis_ising(J, h, T=1.0, steps=1000)[0])

#print("Sequence of states:")
#print(metropolis_ising(J, h, T=1.0, steps=1000)[1])