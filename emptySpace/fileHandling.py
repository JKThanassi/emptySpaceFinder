import numpy as np
from numpy import genfromtxt

data = genfromtxt("../datasets/cars.csv", delimiter=',', skip_header=1)

print(data.axes)
