import numpy as np

# simple Monte Carlo simulation to estimate the value of pi

#Plot a circle and a square
circle_x = np.linspace(0, 1, 100)
circle_y = np.sqrt(1-circle_x**2)

#Plot the random points
times = 1000
x = np.random.rand(times)
y = np.random.rand(times)

#Calculate the distance from the origin
dist = np.sqrt(x ** 2 + y ** 2)
incircle = dist <= 1

#Calculate Pie
incircle_ratio=float(np.sum(incircle))/float(len(incircle))
pi = incircle_ratio * 4
print ("The estimated value of pi is:", pi)