# sphinx_gallery_thumbnail_number = 4
import pyvista as pv
from pyvista import examples
import numpy as np
v = np.load('full_speed.npy')

r = np.load('full_r.npy')
lon = np.load('full_lon.npy') / 180 * np.pi
lat = np.load('full_lat.npy')
lat = (90 - lat) / 180 * np.pi
time = np.load('full_time.npy')
point_corr = np.zeros([lat.shape[0]*r.shape[0]*lon.shape[0], 3])
v_corr = np.zeros([lat.shape[0]*r.shape[0]*lon.shape[0]])
glat,gr,glon = np.meshgrid(lat,r,lon)
gz = gr * np.cos(glat)
gx = gr * np.sin(glat) * np.cos(glon)
gy = gr * np.sin(glat) * np.sin(glon)
print(gz.min(), gz.max())
print(gx.min(), gx.max())
print(gy.min(), gy.max())

id = 0
for id_lat in range(lat.shape[0]):
    # print('id lat: ', id_lat)
    for id_r in range(r.shape[0]):
        for id_lon in range(lon.shape[0]):
            point_corr[id] = np.array([gx[id_r, id_lat, id_lon],
                                       gy[id_r, id_lat, id_lon],
                                       gz[id_r, id_lat, id_lon]])
            v_corr[id] = v[0,id_lat,id_r,id_lon]
            id += 1
assert id == lat.shape[0]*r.shape[0]*lon.shape[0]

# Download the sparse data
# probes = examples.download_thermal_probes()
# print(probes.points.shape)


grid = pv.UniformGrid()
grid.origin = (-256, -256, -256)
grid.spacing = (3, 3, 3)
grid.dimensions = (128*2, 128*2, 128*2)
print(grid.points[0])


dargs = dict(cmap="coolwarm", clim=[v.min(),v.max()], scalars="solar wind speed")
# cpos = [(364280.5723737897, 4285326.164400684, 14093.431895014139),
#  (337748.7217949739, 4261154.45054595, -637.1092549935128),
#  (-0.29629216102673206, -0.23840196609932093, 0.9248651025279784)]
my_mesh = pv.PolyData(point_corr)
my_mesh.point_arrays['solar wind speed'] = v_corr

print('v: ', v.min(),v.max())

# p = pv.Plotter()
# p.add_mesh(grid.outline(), color='k')
# p.add_mesh(probes, render_points_as_spheres=True, **dargs)
# p.show(cpos=cpos)

interp = grid.interpolate(my_mesh, radius=7, sharpness=5, strategy='mask_points')
print(type(interp))
vol_opac = [0, 0, .2, 0.2, 0.5, 0.5]

# p = pv.Plotter(shape=(1,2), window_size=[1024*3, 768*2])
p = pv.Plotter()
p.enable_depth_peeling()
p.add_volume(interp, opacity=vol_opac, **dargs)
# p.add_mesh(my_mesh, render_points_as_spheres=True, point_size=10, **dargs)
# p.subplot(0,1)
# p.add_mesh(interp.contour(np.linspace(v.min(),v.max(),2)), opacity=0.2, **dargs)
# p.add_mesh(my_mesh, render_points_as_spheres=True, point_size=10, **dargs)
# p.link_views()
p.show()
# p.show(cpos=cpos)