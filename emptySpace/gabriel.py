# Class for generating a gabriel graph from a dataset or delaunay triangulation
# NOTE: this will apply only to 2d datasets and will eventually be extended to nd
from matplotlib.patches import Circle
from scipy.spatial import Delaunay, distance
from math import sqrt


class Gabriel(object):
    class _point:

        def __init__(self, p_id, coordinates):
            """This is a helper class for the gabriel class that encapsulates point data
            
            Arguments:
                p_id {int} -- The name of the point
                coordinates {tuple} -- The coordinates of the point
            """

            self.p_id = p_id
            self.coordinates = coordinates
            self.edges = list()
            self.removed_edges = dict()


        def add_edge(self, point=None, point_list=None):
            """This function will add edges to a point
            
            Arguments:
                point {_point} -- a point to add to the edgelist
                point_list {list} -- A list of points that are connected to this one
            """
            if point_list is None and point != None:
                self.edges.append(point)
                self.removed_edges[point] = False
                
            elif point is None and point_list is not None:
                for point in point_list:
                    self.edges.append(point)
                    self.removed_edges[point] = False

        def remove_edge(self, toRemove):
            """this function removes an edge from the edge list
           
            Args:
                toRemove (_point): the point to be removed
            """   
            self.removed_edges[toRemove] = True

    def __init__(self, data):
        """Constructor for Gabriel Object
        
        Args:
            data (ndarray): numpy ndarray of data to be processed
        """

        self.data = data
        self.delaunay_graph = None
        self.visited_paths = dict()
        self.n_dim = self.data.shape[1]
        self.point_graph = list()

    def generate_gabriel(self, interactive=False):
        """This function will generate a gabriel graph from a set of data
            interactive (bool, optional): Defaults to False. Will prune edges interactivley if true
        """

        self.delaunay_graph = Delaunay(self.data)
        self.__generate_point_graph()
        self.__prune_edges()
        self.__remove_edges()

    def __generate_point_graph(self):
        """This function will generate a graph of points and their edges
        """
        # keys are the id of the point and the data is the _point object
        for p_id in range(len(self.data)):
            self.point_graph.append(self._point(p_id, tuple(self.data[p_id])))

        for coord_set in self.delaunay_graph.simplices:
            pos_in_set = 0
            for coord_idx in coord_set:
                for secondary_idx in coord_set[pos_in_set + 1:]:
                    # graph will be a one way directed graph
                    if self.point_graph[secondary_idx] in self.point_graph[coord_idx].edges or self.point_graph[coord_idx] in self.point_graph[secondary_idx].edges:
                        pass
                    elif coord_idx != secondary_idx:
                        self.point_graph[coord_idx].add_edge(point=self.point_graph[secondary_idx])
                pos_in_set += 1

    def get_center(self, point1, point2):
        """This function gets the center of the path between two points
        
        Args:
            point1 (_point): the first endpoint of the path
            point2 (_point): the second endpoint of the path

        
        """
        center_coord_list = list()
        for coord1, coord2 in zip(point1.coordinates, point2.coordinates):
            center_coord_list.append(((coord1 + coord2) / 2.0)) 
        return center_coord_list

    def __is_valid_edge(self, point1, point2):
        diameter = distance.euclidean(point1.coordinates, point2.coordinates)
        radius = diameter / 2.0
        center = self.get_center(point1, point2)
        for temp_point in self.point_graph:
            if temp_point is not point1 and temp_point is not point2:
                if distance.euclidean(center, temp_point.coordinates) <= radius:
                    return False
        return True

    def __prune_edges(self):
        for temp_point in self.point_graph:
            for point in temp_point.edges:
                if not self.__is_valid_edge(temp_point, point):
                    temp_point.remove_edge(point)


    def __remove_edges(self):
        """This function removes edges marked for removal
        """
        for point in self.point_graph:
            point.edges[:] = [edge for edge in point.edges if not point.removed_edges[edge]]

