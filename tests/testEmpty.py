import sys
sys.path.append('../')
import numpy as np
from emptySpace.emptyspace import Empty_Space
from numpy import genfromtxt

random_gaussian = np.random.normal(size=(300,2))
es = Empty_Space(random_gaussian)
es.find_empty_space()
es.plot()

