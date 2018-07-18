import sys
sys.path.append('../')
import numpy as np
from emptySpace.emptyspace import Empty_Space
from numpy import genfromtxt

random_gaussian = np.random.normal(size=(100,2))
es = Empty_Space(random_gaussian, 30, 2)
es.find_empty_space()
es.scale()
es.plot()
