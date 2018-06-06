import numpy as np
from numpy import genfromtxt

data = genfromtxt("../datasets/cars.csv", delimiter=',')

print(data)
