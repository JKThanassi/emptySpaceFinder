import numpy as np
import matplotlib.pyplot as plt
from emptySpace.gabriel import Gabriel

class Empty_Space(object):
    def __init__(self, data):
        self.gabriel = Gabriel(data)
        self.gabriel.generate_gabriel()
        self.data = data
        self.ghost_points = list()
    
    def find_empty_space(self):
        for key in self.gabriel.point_graph.keys():
            temp_point = self.gabriel.point_graph[key]
            for edge_point in temp_point.edges:
                
                center = self.__find_center(temp_point, edge_point)
                self.ghost_points.append(center)
                

    def __find_center(self, point1, point2):
        x1, y1 = point1.coordinates
        x2, y2 = point2.coordinates
        return (((x1 + x2) / 2.0), ((y1 + y2) / 2.0))

    def plot(self):
        ax = self.gabriel.plot(editable_outside=True)
        for coord_pair in self.ghost_points:
            ax.scatter(coord_pair[0], coord_pair[1], marker="*")
        plt.show()