from sklearn.datasets import load_wine
from sklearn.manifold import MDS
from scipy.spatial import Delaunay
import matplotlib.pyplot as plt

wine = load_wine()
wine_data = wine.data

print(wine_data.shape)

mds = MDS(n_components=2)

print("data after mds scaling to 2d")
data_scaled = mds.fit_transform(wine_data)
print(data_scaled.shape)

triangulated = Delaunay(data_scaled)

fig = plt.figure()
ax = fig.add_subplot(121)
ax.triplot(data_scaled[:,0], data_scaled[:,1], triangulated.simplices)
plt.show()