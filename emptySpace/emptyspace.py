import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial import distance
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.manifold import MDS
from emptySpace.gabriel import Gabriel

class Empty_Space(object):
    def __init__(self, data, max_clusters, dim_to_scale):
        """constructor for Empty_Space object
        
        Args:
            data (ndarray): a numpy ndarray of data to be analyzed
        """

        self.gabriel = Gabriel(data)
        self.gabriel.generate_gabriel()
        self.data = data
        self.center_points = list()
        self.center_point_distances = list()
        self.ghost_points = list()
        self.max_clusters = max_clusters
        self.dim_to_scale = dim_to_scale
    
    def find_empty_space(self):
        for temp_point in self.gabriel.point_graph:
            for edge_point in temp_point.edges:
                dist = distance.euclidean(temp_point.coordinates, edge_point.coordinates)
                center = self.gabriel.get_center(temp_point, edge_point)
                self.center_points.append(center)
                self.center_point_distances.append(dist)
        self.cluster_close_points()

    def cluster_close_points(self):
        # find the optimal number of clusters
        # TODO have some function of number of center points to determine max num of test points
        km_list = [KMeans(n_clusters=i).fit(self.center_points) for i in range(2,self.max_clusters)]
        scores = [silhouette_score(self.center_points, km.predict(self.center_points)) for km in km_list]
        best_km_idx = np.argmax(scores)
        self.ghost_points = km_list[best_km_idx].cluster_centers_


    def scale(self):
        mds = MDS(n_components=self.dim_to_scale)
        data = np.copy(self.data)
        data.append(np.copy(self.ghost_points))
        scaled_data = mds.fit_transform(data)

        scaled_ghost = scaled_data[len(self.data) : ]
        return_scaled_data = scaled_data[:len(self.data)]
        return return_scaled_data, scaled_ghost


    def plot(self):
        if self.data.shape[1] == 2: 
            ax = self.gabriel.plot(editable_outside=True)
            for coord_pair in self.ghost_points:
                ax.scatter(coord_pair[0], coord_pair[1], marker="*")
            plt.show()
        elif self.data.shape[1] == 3:
            ax = self.gabriel.plot(editable_outside=True)
            for coords in self.ghost_points:
                ax.scatter(coords[0], coords[1], coords[2], marker="*")
            plt.show()