import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from emptySpace.gabriel import Gabriel

class Empty_Space(object):
    def __init__(self, data):
        """constructor for Empty_Space object
        
        Args:
            data (ndarray): a numpy ndarray of data to be analyzed
        """

        self.gabriel = Gabriel(data)
        self.gabriel.generate_gabriel()
        self.data = data
        self.ghost_points = list()
    
    def find_empty_space(self):
        for temp_point in self.gabriel.point_graph:
            for edge_point in temp_point.edges:
                center = self.gabriel.get_center(temp_point, edge_point)
                self.ghost_points.append(center)

    def plot(self):
        if self.data.shape[1] == 2: 
            ax = self.gabriel.plot(editable_outside=True)
            for coord_pair in self.ghost_points:
                ax.scatter(coord_pair[0], coord_pair[1], marker="*")
            plt.show()
        elif self.data.shape[1] == 3:
            ax = self.gabriel.plot(editable_outside=True)
            for coords in self.ghost_points:
                ax.scatter(coords[0], coords[1], coords[2])