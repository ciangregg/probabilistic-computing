<br><br>
 
<div align="center">

# QUBO and Ising Formulations of Optimisation Problems
 
### Simulated annealing from Combinatorial Optimisation to Optimal Control
 
</div>
<br><br>

## Overview

This repo has my code and graphs from my summer research project where we reformulated optimisation problems as the search for minimum-energy states of an **Ising** or **QUBO** energy landscape. We developed a Monte Carlo Markov Chain framework to find these low-energy states, building up from the Metropolis algorithm to simulated annealing.
 
With this annealing framework in place, we investigated a sequence of established combinatorial problems, working through their constructions in detail, teaching us the techniques needed to translate constraints and objectives into energy contributions. We then extended this to a continuous problem: a **mixed-integer optimal control formulation of a 1D rocket trajectory**, encoding continuous position and velocity variables as binary and enforcing the rocket's dynamics as constraint terms. Annealing the resulting Q matrix showed that optimal control problems of this kind can be expressed in a form that naturally extends to **probabilistic computing hardware**.
 
The project was supervised by **Professor Stefano Sanvito** and **Michael Mitchell**.


The Structure of the the project:
- [Ising/](Ising/) Implementing the Metropolis algorithm and simulated annealing for 2D Ising systems
- [example-problems/](example-problems/) Formulating classic NP-hard combinatorial problems as QUBOs and solving them via annealing
- [rocket_trajectory/](rocket_trajectory/) Extending these ideas to a mixed-integer optimal control problem (1D rocket trajectory) expressed as a QUBO
