import sys
sys.path.append('../')
from emptySpace.emptyspace import Empty_Space
import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import MDS

class es_vs_no_es(object):
    """This class is to test how mds differs with and without the empty space points
    """
    
    def __init__(self, datasets, show_plots=True, save_plots=False):
        """Constructor for es_vs_no_vs
        
        Args:
            datasets (dict): Dictionary where the key is the name of the dataset and the value is the dataset
            show_plots (bool, optional): Defaults to True. Flag for showing plots
            save_plots (bool, optional): Defaults to False. Flag for saving plots
        """

        self.datasets = datasets
        self.save_plots = save_plots
        self.show_plots = show_plots

    def generate_plots(self):
        """This function will generate plots with and without ghost points
        """
        for key in self.datasets.keys():
            fig = self.__plot_no_ghost(self.datasets[key], key)
            self.__plot_ghost(self.datasets[key], key, fig)

    def __plot_no_ghost(self, data, name):
        """Handles plotting without ghost points
        
        Args:
            data (List): A list of data to be
            name (string): the name of the distribution
        """
        #plot before mds 
        fig = plt.figure()
        ax = fig.add_subplot(221)
        ax.set_title('non scaled no ghost ' + name)
        for coords in data:
            ax.scatter(coords[0], coords[1], marker='o', c='red')
        #now mds transform
        mds = MDS(n_components=2, n_jobs=-1)
        scaled_data = mds.fit_transform(data)
        ax_scaled = fig.add_subplot(222)
        ax_scaled.set_title('scaled no ghost ' + name)
        for coords in scaled_data:
            ax_scaled.scatter(coords[0], coords[1], marker='o', c='red')
        return fig


    def __plot_ghost(self, data, name, fig):
        """Handles plotting with ghost points
        
        Args:
            data (List): A list of data to be processed
            name (string): the name of the distribution
        """
        es = Empty_Space(data, 10, 2)
        #plot non scaled data
        es.find_empty_space()
        us_ghost = es.ghost_points
        #plot before mds 
        ax = fig.add_subplot(223)
        ax.set_title('non scaled ghost ' + name)
        for coords in data:
            ax.scatter(coords[0], coords[1], marker='o', c='red')
        for coords in us_ghost:
            ax.scatter(coords[0], coords[1], marker='x', c='blue')

        #now mds transform
        s_data, s_ghost = es.scale()
        ax_scaled = fig.add_subplot(224)
        ax_scaled.set_title('scaled ghost ' + name)
        for coords in s_data:
            ax_scaled.scatter(coords[0], coords[1], marker='o', c='red')
        for coords in s_ghost:
            ax_scaled.scatter(coords[0], coords[1], marker='x', c='blue')
        if self.show_plots:
            plt.show()
        if self.save_plots:
            print(name, " distribution saved as ", name, ".png")
            fig.set_size_inches(16,9)
            plt.savefig(("plots/" + name + ".png"), bbox_inches='tight', dpi=150)


    