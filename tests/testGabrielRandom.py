import sys
sys.path.append('../')
import numpy as np
from emptySpace.gabriel import Gabriel

random_gaussian = np.random.normal(size=(100,2))

gab = Gabriel(random_gaussian)
gab.generate_gabriel(interactive=True)


gumbel = np.random.gumbel(size=(100,2))
gab2 = Gabriel(gumbel)
gab2.generate_gabriel(interactive=True)
