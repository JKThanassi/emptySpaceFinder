# Class for generating a gabriel graph from a dataset or delaunay triangulation
# NOTE: this will apply only to 2d datasets and will eventually be extended to nd
import matplotlib.pyplot as plt
import matplotlib.lines as lines
from matplotlib.patches import Circle
from scipy.spatial import Delaunay
from math import sqrt


class Gabriel:
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
                self.lines.append(lines.Line2D((x1, x2), (y1, y2), zorder=1))

            elif point is None and point_list is not None:
                for point in point_list:
                    self.edges.append(point)

            else:
                pass

        def remove_edge(self, toRemove):
            """
            This function will remove an edge from the two specified points
            :param toRemove: the point to remove
            :return: None
            """
            self.lines[self.edges.index(toRemove)].remove()
            self.edges.remove(toRemove)

    def __init__(self, data):
        """Constructor for Gabriel class
        
        Arguments:
            data {array-like} -- the data to generate a gabriel graph from
        """
        self.data = data
        self.delaunay_graph = None
        self.visited_paths = dict()
        self.point_graph = dict()

    def generate_gabriel(self, interactive=False):
        """This function will generate a gabriel graph from a set of data
            interactive (bool, optional): Defaults to False. Will prune edges interactivley if true
        """

        self.delaunay_graph = Delaunay(self.data)
        self.__generate_point_graph()
        if interactive:
            self.__prune_edges_interactive()
        else:
            # self.__prune_edges()
            pass

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

    def euclidian_distance(self, point1, point2):
        """This function provides the distance between two points
        
        Arguments:
            point1 {array-like} -- array of coordinates describing the first point
            point2 {array-like} -- array of coordinates describing the second point
        """
        sqr_diff_sum = 0
        for idx in range(len(point1.coordinates)):
            # TODO fix
            sqr_diff_sum += (point1.coordinates[idx] - point2.coordinates[idx]) ** 2
        return sqrt(sqr_diff_sum)

    def __is_valid_edge(self, point1, point2):
        diameter = self.euclidian_distance(point1, point2)
        radius = diameter / 2.0
        x1, y1 = point1.coordinates
        x2, y2 = point2.coordinates
        center = self._point(-1, (((x1 + x2) / 2.0), ((y1 + y2) / 2.0)))

        for point_key in self.point_graph.keys():
            temp_point = self.point_graph[point_key]
            if temp_point is not point1 and temp_point is not point2:
                if self.euclidian_distance(center, temp_point) > radius:
                    return False

    def __is_valid_edge_interactive(self, ax, point1, point2):
        diameter = self.euclidian_distance(point1, point2)
        radius = diameter / 2.0
        x1, y1 = point1.coordinates
        x2, y2 = point2.coordinates
        center = self._point(-1, (((x1 + x2) / 2.0), ((y1 + y2) / 2.0)))
        circle = Circle(center.coordinates, radius=radius, fill=False, linewidth=1, linestyle='solid')
        ax.add_artist(circle)
        plt.draw()
        for point_key in self.point_graph.keys():
            temp_point = self.point_graph[point_key]
            if temp_point is not point1 and temp_point is not point2:
                input("hit enter to move on")
                if self.euclidian_distance(center, temp_point) > radius:
                    circle.remove()
                    plt.draw()
                    return False

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
                x1, y1 = temp_point.coordinates
                x2, y2 = point.coordinates
                if not self.__is_valid_edge_interactive(ax, temp_point, point):
                    temp_point.remove_edge(point)
                    plt.draw()

    def plot(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        self.__plot_nodes(ax)
        self.__plot_edges(ax)
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
