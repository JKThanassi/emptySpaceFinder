# Class for generating a gabriel graph from a dataset or delaunay triangulation
# NOTE: this will apply only to 2d datasets and will eventually be extended to nd
import matplotlib.pyplot as plt
import matplotlib.lines as lines
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
            self.lines = list()


        def add_edge(self, point=None, point_list=None):
            """This function will add edges to a point
            
            Arguments:
                point {_point} -- a point to add to the edgelist
                point_list {list} -- A list of points that are connected to this one
            """
            if point_list is None and point != None:
                self.edges.append(point)
                x1, y1 = self.coordinates
                x2, y2 = point.coordinates
                #TODO remove the line2D from this
                self.lines.append(lines.Line2D((x1, x2), (y1, y2), zorder=1))

            elif point is None and point_list is not None:
                for point in point_list:
                    self.edges.append(point)

        def remove_edge(self, toRemove, isInteractive=False):
            """this function removes an edge from the edge list
           
            Args:
                toRemove (_point): the point to be removed
                isInteractive (bool, optional): Defaults to False. flag stating whether or not to remove the edge interactivley
            """
            # TODO delete debug print statements
            self_x, self_y = self.coordinates
            toRemove_x, toRemove_y = toRemove.coordinates
            for line in self.lines:
                # TODO change so non 2d datasets are handled
                line_x, line_y = line.get_data()
                if (line_x[0] == self_x) and (line_x[1] == toRemove_x) and (line_y[0] == self_y) and (line_y[1] == toRemove_y):
                    print(f"line from ({self_x}, {self_y}) to ({toRemove_x}, {toRemove_y}) has been removed")
                    if isInteractive:
                        line.remove()
                    self.lines.remove(line)
                    del line
                
            self.edges.remove(toRemove)

    def __init__(self, data):
        """Constructor for Gabriel Object
        
        Args:
            data (ndarray): numpy ndarray of data to be processed
        """

        self.data = data
        self.delaunay_graph = None
        self.visited_paths = dict()
        self.point_graph = dict()
        self.n_dim = self.data.shape[1]

    def generate_gabriel(self, interactive=False):
        """This function will generate a gabriel graph from a set of data
            interactive (bool, optional): Defaults to False. Will prune edges interactivley if true
        """

        self.delaunay_graph = Delaunay(self.data)
        self.__generate_point_graph()
        if interactive:
            self.__prune_edges_interactive()
        else:
            self.__prune_edges()

    def __generate_point_graph(self):
        """This function will generate a graph of points and their edges
        """
        # keys are the id of the point and the data is the point object
        for p_id in range(len(self.data)):
            self.point_graph[p_id] = self._point(p_id, tuple(self.data[p_id]))

        for coord_set in self.delaunay_graph.simplices:
            pos_in_set = 0
            for coord_idx in coord_set:
                for secondary_idx in coord_set[pos_in_set + 1:]:
                    # graph will be a one way directed graph
                    if self.point_graph[secondary_idx] in self.point_graph[coord_idx].edges or self.point_graph[coord_idx] in self.point_graph[secondary_idx].edges:
                        print(f"edge from point {coord_idx} to {secondary_idx} already exists ... skipping")
                    elif coord_idx != secondary_idx:
                        self.point_graph[coord_idx].add_edge(point=self.point_graph[secondary_idx])
                pos_in_set += 1

    def __get_center(self, point1, point2):
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
        center = self.__get_center(point1, point2)

        for point_key in self.point_graph.keys():
            temp_point = self.point_graph[point_key]
            if temp_point is not point1 and temp_point is not point2:
                if distance.euclidean(center, temp_point.coordinates) < radius:
                    return False
        return True

    def __is_valid_edge_interactive(self, ax, point1, point2):
        diameter = distance.euclidean(point1.coordinates, point2.coordinates)
        radius = diameter / 2.0
        center = self.__get_center(point1, point2)
        for point_key in self.point_graph.keys():
            temp_point = self.point_graph[point_key]
            if temp_point is not point1 and temp_point is not point2:
                if distance.euclidean(center, temp_point.coordinates) < radius:
                    return False
        return True

    def __draw_circle(self, point1, point2, ax):
        diameter = distance.euclidean(point1.coordinates, point2.coordinates)
        radius = diameter / 2.0
        x1, y1 = point1.coordinates
        x2, y2 = point2.coordinates
        center = self.__get_center(point1, point2)
        circle = Circle(center, radius=radius, fill=False, linewidth=1, linestyle='solid')
        ax.add_artist(circle)
        plt.draw()
        return circle

    def __prune_edges(self):
        for key in self.point_graph.keys():
            temp_point = self.point_graph[key]
            for point in temp_point.edges:
                if not self.__is_valid_edge(temp_point, point):
                    temp_point.remove_edge(point)
                    print(
                        f"edge from point:{temp_point.p_id} to point:{point.p_id} is invalid")

    def __prune_edges_interactive(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        self.__plot_nodes(ax)
        self.__plot_edges(ax)
        plt.show(block=False)
        for key in self.point_graph.keys():
            temp_point = self.point_graph[key]
            for point in temp_point.edges:
                circle = self.__draw_circle(temp_point, point, ax)
                while plt.waitforbuttonpress() is False:
                    pass
                if not self.__is_valid_edge_interactive(ax, temp_point, point):
                    print(f"removing edge from point {temp_point.coordinates} to {point.coordinates}")
                    temp_point.remove_edge(point, isInteractive=True)
                circle.remove()
                plt.draw()

    def plot(self, editable_outside=False):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        self.__plot_nodes(ax)
        self.__plot_edges(ax)
        if editable_outside:
            return ax
        else:
            plt.show()
        
    def __plot_nodes(self, ax):
        for key in self.point_graph.keys():
            temp_point = self.point_graph[key]
            ax.scatter(temp_point.coordinates[0], temp_point.coordinates[1], zorder=2)

    def __plot_edges(self, ax):
        # first generate lines
        for key in self.point_graph.keys():
            temp = self.point_graph[key]
            for line in temp.lines:
                ax.add_line(line)
