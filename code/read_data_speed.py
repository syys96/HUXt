import numpy as np
from pyvista import examples
import pyvista as pv
import numpy as np

# mesh = examples.download_bunny_coarse()
# print(mesh.points.shape)
# exit(0)

r = np.load('full_r.npy')
lon = np.load('full_lon.npy') / 180 * np.pi
lat = np.load('full_lat.npy')
lat = (90 - lat) / 180 * np.pi
time = np.load('full_time.npy')
# time lat r lon
v = np.load('full_speed.npy')
print(lat.shape,r.shape,lon.shape)
print(v.shape)
glat,gr,glon = np.meshgrid(lat,r,lon)
gz = gr * np.cos(glat)
gx = gr * np.sin(glat) * np.cos(glon)
gy = gr * np.sin(glat) * np.sin(glon)

print(np.max(gz), np.max(gx), np.max(gy))

point_corr = np.zeros([lat.shape[0]*r.shape[0]*lon.shape[0], 3])
v_corr = np.zeros([lat.shape[0]*r.shape[0]*lon.shape[0]])
idea_x,idea_y,idea_z = np.meshgrid(np.linspace(np.min(gx),np.mat(gx),64),
                        np.linspace(np.min(gy),np.mat(gy),64),
                        np.linspace(np.min(gz),np.mat(gz),64))
grid_corr = np.zeros([64*64*64,3])
id_idel = 0
for i in range(64):
    for j in range(64):
        for k in range(64):
            grid_corr[id_idel] = np.array([idea_x[j,i,k],
                                           idea_y[j,i,k],
                                           idea_z[j,i,k]])
            id_idel += 1
assert id_idel == 64**3

print('1: ', point_corr.shape)
print('2: ', gx.shape)

id = 0
for id_lat in range(lat.shape[0]):
    print('id lat: ', id_lat)
    for id_r in range(r.shape[0]):
        for id_lon in range(lon.shape[0]):
            point_corr[id] = np.array([gx[id_r, id_lat, id_lon],
                                       gy[id_r, id_lat, id_lon],
                                       gz[id_r, id_lat, id_lon]])
            v_corr[id] = v[0,id_lat,id_r,id_lon]
            id += 1
assert id == lat.shape[0]*r.shape[0]*lon.shape[0]
np.save('point_arr.npy', point_corr)
mesh = pv.PolyData(point_corr)
print(mesh.points.shape)



# plt = pv.Plotter()
# plt.add_mesh(mesh, show_edges=True)
# camera_position = [(6.20, 3.00, 7.50),
#                  (0.16, 0.13, 2.65),
#                  (-0.28, 0.94, -0.21)]
mesh.point_arrays['my point values'] = v_corr

contours = mesh.contour(np.linspace(50, 200, 5))
p = pv.Plotter()
p.add_mesh(mesh.outline())
p.add_mesh(mesh,scalars='my point values', color="k")
# p.add_mesh(contours, opacity=0.25, clim=[0, 200])
p.show()
# mesh.plot(scalars='my point values',
#           show_edges=True, screenshot='beam_point_data.png')