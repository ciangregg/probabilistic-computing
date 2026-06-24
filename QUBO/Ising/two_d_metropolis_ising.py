import numpy as np
import matplotlib.pyplot as plt

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


# swapped from saving sample after every flip to saving sample after every sweep (N*N flips)

def two_d_metropolis_ising(N, J, h, T, sweeps):
    s = np.ones((N, N), dtype=int)
    samples = []

    for sweep in range(sweeps):

        for _ in range(N * N):
            x = np.random.randint(N)
            y = np.random.randint(N)

            nn = (
                s[(x+1)%N, y] +
                s[(x-1)%N, y] +
                s[x, (y+1)%N] +
                s[x, (y-1)%N]
            )

            dE = 2 * s[x, y] * (J * nn + h)

            if dE <= 0 or np.random.rand() < np.exp(-dE / T):
                s[x, y] *= -1

        samples.append(s.copy())

    return samples

def thermo(samples, J, h, T, N):
    Nspins = N * N

    energies = np.array([energy(s, J, h) for s in samples])
    mags     = np.array([s.sum() for s in samples])  # total magnetization

    E = energies.mean() / Nspins
    EJ= round(E/abs(J),0)
    cv = energies.var() / (T**2 * Nspins)

    m = mags.mean() / Nspins
    chi = mags.var() / (T * Nspins)

    Tc = 2 * abs(J) / np.log(1 + np.sqrt(2))

    return {
        "Tc": Tc,
        "E per spin": E,
        "E per spin wrt J": EJ,
        "cv": cv,
        "m": m,
        "chi": chi
    }


temperatures = [1.0, 9.0, 11.3459, 15.0]
for temp in temperatures:
    Nsize = 50
    samples = two_d_metropolis_ising(Nsize, J=-5.0, h=0.0, T=temp, sweeps=10000)
    results = thermo(samples, J=-5.0, h=0.0, T=temp, N=Nsize)
    print(f"Temperature: {temp}")
    for k, v in results.items():
        print(f"{k:>8s} = {float(v):.4f}")
   

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
