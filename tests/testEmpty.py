import sys
sys.path.append('../')
import numpy as np
from emptySpace.emptyspace import Empty_Space
from numpy import genfromtxt

cars_data = genfromtxt("../datasets/cars.csv", delimiter=',', skip_header=1)
cars_data = cars_data[1:140, 3:5]
print(cars_data)

es = Empty_Space(cars_data)
es.find_empty_space()
es.plot()

