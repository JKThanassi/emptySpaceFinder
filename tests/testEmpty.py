import sys
sys.path.append('../')
import numpy as np
from emptySpace.emptyspace import Empty_Space
from numpy import genfromtxt

random_gaussian = np.random.normal(size=(102,10))
es = Empty_Space(random_gaussian, 30, 2)
es.find_empty_space()
data, ghost = es.scale()
es.plot()
es.plot_scaled(data, ghost)
