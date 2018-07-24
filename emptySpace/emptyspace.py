import numpy as np
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
        self.ghost_point_avg_dist = list()
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

    def __get_avg_cluster_distance(self, best_km):
        self.ghost_point_avg_dist = [0] * best_km.n_clusters
        labels = best_km.labels_
        num_points_per_cluster = [0] * best_km.n_clusters

        for label in labels:
            num_points_per_cluster[label] += 1

        for idx in range(0, len(self.center_points)):
            self.ghost_point_avg_dist[labels[idx]] += self.center_point_distances[idx]
        
        for idx in range(0, len(self.ghost_point_avg_dist)):
            self.ghost_point_avg_dist[idx] = self.ghost_point_avg_dist[idx] / float(num_points_per_cluster[idx])


    def cluster_close_points(self):
        # find the optimal number of clusters
        km_list = [KMeans(n_clusters=i, n_jobs=-1).fit(self.center_points) for i in range(2,self.max_clusters)]
        scores = [silhouette_score(self.center_points, km.predict(self.center_points)) for km in km_list]
        best_km_idx = np.argmax(scores)
        self.ghost_points = km_list[best_km_idx].cluster_centers_
        self.__get_avg_cluster_distance(km_list[best_km_idx])

    def scale(self):
        mds = MDS(n_components=self.dim_to_scale)
        data = np.concatenate((np.copy(self.data), np.copy(self.ghost_points)))
        scaled_data = mds.fit_transform(data)

        scaled_ghost = scaled_data[len(self.data) : ]
        return_scaled_data = scaled_data[:len(self.data)]
        return return_scaled_data.tolist(), scaled_ghost.tolist()
