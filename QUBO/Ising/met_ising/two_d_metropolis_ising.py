import numpy as np
import math
import matplotlib.pyplot as plt
from numba import njit

def energy(s, J, h):
    #2D Ising energy with periodic boundary conditions.
    
    E = 0.0
    N = s.shape[0]

    for i in range(N):
        for j in range(N):
            E -= J * s[i, j] * (
                s[(i + 1) % N, j] +
                s[i, (j + 1) % N]
            )
            E -= h * s[i, j]

    return E

@njit
def sweep_once(s, N, J, h, T, E):
    for _ in range(N * N):
        x = np.random.randint(N)
        y = np.random.randint(N)

        nn = (
            s[(x + 1) % N, y] +
            s[(x - 1) % N, y] +
            s[x, (y + 1) % N] +
            s[x, (y - 1) % N]
        )

        dE = 2 * s[x, y] * (J * nn + h)

        if dE <= 0 or np.random.rand() < math.exp(-dE / T):
            s[x, y] *= -1
            E += dE

    return E

def two_d_metropolis_ising(N, J, h, T, sweeps, warmup=None):
    if warmup is None:
        warmup = sweeps // 10

    s = np.random.choice(np.array([-1, 1]), size=(N, N))

    E = energy(s, J, h)

    # warmup
    for _ in range(warmup):
        E = sweep_once(s, N, J, h, T, E)

    energies = []
    mags = []

    for _ in range(sweeps):
        E = sweep_once(s, N, J, h, T, E)
        energies.append(E)
        mags.append(s.sum())

    return np.array(energies), np.array(mags)

def thermo(energies, mags, J, h, T, N):
    Nspins = N * N

    E = np.mean(energies) / Nspins
    EJ = E / abs(J)

    cv = np.var(energies) / (T**2 * Nspins)

    m = np.mean(mags) / Nspins
    chi = np.var(mags) / (T * Nspins)

    Tc = 2 * abs(J) / np.log(1 + np.sqrt(2))

    return {
        "Tc": Tc,
        "E per spin": E,
        "E per spin wrt J": EJ,
        "cv": cv,
        "m": m,
        "chi": chi
    }


temperatures = [1, 9, 11.0, 11.3 , 100,100_000]
for temp in temperatures:
    print(f"       {temp}        ")
    Nsize = 50
    energies, mags = two_d_metropolis_ising(Nsize, J=-5.0, h=0.0, T=temp, sweeps=10000, warmup=1000)
    results = thermo(energies, mags, J=-5.0, h=0.0, T=temp, N=Nsize)
    print(f"Temperature: {temp}")
    for k, v in results.items():
        print(f"{k:>8s} = {float(v):.4f}")
        
   





'''
temperatures = [5.0]
#[1.0, 9.0, 11.3459, 15.0]
for temp in temperatures:
    Nsize = 50
    energies, mags = two_d_metropolis_ising(Nsize, J=-5.0, h=0.0, T=temp, sweeps=1000, warmup=500)
    results = thermo(energies, mags, J=-5.0, h=0.0, T=temp, N=Nsize)
    print(f"Temperature: {temp}")
    for k, v in results.items():
        print(f"{k:>8s} = {float(v):.4f}")
'''






'''
fig, ax = plt.subplots()

ax.matshow(final_state, cmap="coolwarm", vmin=-1, vmax=1)

for i in range(final_state.shape[0]):
    for j in range(final_state.shape[1]):
        ax.text(
            j, i,
            str(int(final_state[i, j])),
            va='center',
            ha='center'
        )

#plt.savefig('final_state.pdf')
plt.show()
'''
