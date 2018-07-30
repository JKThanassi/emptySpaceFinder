import sys
sys.path.append('../')
from emptySpace.emptyspace import Empty_Space
import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import MDS

class es_vs_no_es(object):
    """This class is to test how mds differs with and without the empty space points
    """
    
    def __init__(self, datasets, show_plots=True, save_plots=False, save_path='plots/'):
        """Constructor for es_vs_no_vs
        
        Args:
            datasets (dict): Dictionary where the key is the name of the dataset and the value is a ndarray containing the dataset
            show_plots (bool, optional): Defaults to True. Flag for showing plots
            save_plots (bool, optional): Defaults to False. Flag for saving plots
            save_path (str, optional): Defaults to plots/. The path to save the plots
        """

        self.datasets = datasets
        self.save_plots = save_plots
        self.show_plots = show_plots
        self.save_path = save_path
        self.colorList = ['red', 'yellow', 'green', 'orange', 'black']
        plt.style.use('ggplot')

    def generate_plots(self):
        """This function will generate plots with and without ghost points
        """
        for key in self.datasets.keys():
            fig = plt.figure()
            self.__plot_no_ghost(self.datasets[key], key, fig)
            self.__plot_ghost(self.datasets[key], key, fig)

    def __plot_no_ghost(self, data, name, fig):
        """Handles plotting without ghost points
        
        Args:
            data (List): A list of data to be
            name (string): the name of the distribution
            fig (plt.figure): the matplotlip figure
        """
        #plot before mds
        if data.shape[1] == 2:
            ax = fig.add_subplot(221)
            ax.set_title('non scaled no ghost ' + name)
            for coords in data:
                ax.scatter(coords[0], coords[1], marker='o', c='red')
        #now mds transform
        mds = MDS(n_components=2, n_jobs=-1)
        scaled_data = mds.fit_transform(data)
        ax_scaled = fig.add_subplot(222)
        ax_scaled.set_title('scaled no ghost ' + name)
        colorPickIdx = 0
        
        for idx, coords in enumerate(scaled_data):
            if idx % 20 == 0 and idx != 0:
                colorPickIdx += 1
            ax_scaled.scatter(coords[0], coords[1], marker='o', c=self.colorList[colorPickIdx])


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
        if data.shape == 2:
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
        colorPickIdx = 0
        for idx, coords in enumerate(s_data):
            if idx % 20 == 0 and idx != 0:
                colorPickIdx += 1
            ax_scaled.scatter(coords[0], coords[1], marker='o', c=self.colorList[colorPickIdx])
        for coords in s_ghost:
            ax_scaled.scatter(coords[0], coords[1], marker='x', c='blue')
        if self.show_plots:
            plt.show()
        if self.save_plots:
            print(name, " distribution saved as ", name, ".png")
            fig.set_size_inches(16,9)
            plt.savefig((self.save_path + name + ".png"), bbox_inches='tight', dpi=150)


    