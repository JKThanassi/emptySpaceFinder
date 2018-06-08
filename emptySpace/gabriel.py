#Class for generating a gabriel graph from a dataset or delaunay triangulation
#NOTE: this will apply only to 2d datasets and will eventually be extended to nd
from scipy.spatial import Delaunay
from math import sqrt
class Gabriel:

    def __init__(self, data):
        """Constructor for Gabriel class
        
        Arguments:
            data {array-like} -- the data to generate a gabriel graph from
        """
        self.data = data
        self.delaunay_graph = None
        self.visited_edges = dict()

    def generate_gabriel(self):
        self.delaunay_graph = Delaunay(self.data)

    
    def euclidian_distance(self, point1, point2):
        """This function provides the distance between two points
        
        Arguments:
            point1 {array-like} -- array of coordinates describing the first point
            point2 {array-like} -- array of coordinates describing the second point
        """
        sqr_diff_sum = 0
        for idx in range(len(point1)):
            sqr_diff_sum += (point1[idx] - point2[idx]) ** 2
        return sqrt(sqr_diff_sum)


    def is_valid_edge(self):
        pass