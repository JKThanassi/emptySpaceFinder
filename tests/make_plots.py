import sys
sys.path.append('../')
from tests.es_vs_no_es import es_vs_no_es
import numpy as np

data_dict = dict()

for idx in range(5):
    data_dict['normal' + str(idx)] = np.random.normal(size=(100, 3))
    data_dict['gumbel' + str(idx)] = np.random.gumbel(size=(100, 3))
    data_dict['logistic' + str(idx)] = np.random.logistic(size=(100, 3))

make_plots = es_vs_no_es(data_dict, show_plots=False, save_plots=True, save_path='plots/3d_scaled/')
make_plots.generate_plots()