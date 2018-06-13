import sys
sys.path.append('../')
import numpy as np
from sklearn.manifold import MDS
from sklearn.datasets import load_wine
from emptySpace.gabriel import Gabriel
from numpy import genfromtxt

cars_data = genfromtxt("/home/joseph/Documents/emptySpaceFinder/datasets/cars.csv", delimiter=',', skip_header=1)
cars_data = cars_data[1:140, 3:5]
print(cars_data)


def print_edges(gabriel):
    for key in gabriel.point_graph.keys():
        print(f"edges for {key} are :", end="")
        for edge in gabriel.point_graph[key].edges:
            print(f" {edge.p_id},", end="")
        print(" ")


# wine = load_wine()
# wine_data = wine.data
# #wine_data = wine_data[0:5]


# mds = MDS(n_components=2)
# data_scaled = mds.fit_transform(wine_data)
# data_scaled = list(data_scaled)

gab = Gabriel(cars_data)
gab.generate_gabriel(interactive=True)
print(gab.delaunay_graph.simplices)
print_edges(gab)
gab.plot()

