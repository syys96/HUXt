import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

fig, ax = plt.subplots(figsize=(10, 10), subplot_kw={"projection": "polar"})
lon = np.linspace(0,360,100)
rad = np.linspace(30,215,100)
lon, rad = np.meshgrid(lon, rad)
v = np.zeros([100,100])
levels = [0]
mymap = mpl.cm.viridis
mymap.set_over('lightgrey')
mymap.set_under([0, 0, 0])
print(lon.shape, v.shape)
ax.contour(lon, rad, v, levels=levels, cmap=mymap, extend='both')
plt.show()