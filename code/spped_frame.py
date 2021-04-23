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
glat,gr,glon = np.meshgrid(lat,r,lon)
gz = gr * np.cos(glat)
gx = gr * np.sin(glat) * np.cos(glon)
gy = gr * np.sin(glat) * np.sin(glon)
print(gz.min(), gz.max())
print(gx.min(), gx.max())
print(gy.min(), gy.max())
grid = pv.UniformGrid()
grid.origin = (-256, -256, -256)
grid.spacing = (3, 3, 3)
grid.dimensions = (128*2, 128*2, 128*2)
print(grid.points[0])
dargs = dict(cmap="coolwarm", clim=[v.min(),v.max()], scalars="solar wind speed")
print('v: ', v.min(),v.max())

point_corr = np.zeros([lat.shape[0] * r.shape[0] * lon.shape[0], 3])
v_corr = np.zeros([lat.shape[0] * r.shape[0] * lon.shape[0]])


# p.show(auto_close=False)
# p.open_movie('sw.mp4')
for tid in range(0, v.shape[0], 10):
    id = 0
    for id_lat in range(lat.shape[0]):
        # print('id lat: ', id_lat)
        for id_r in range(r.shape[0]):
            for id_lon in range(lon.shape[0]):
                point_corr[id] = np.array([gx[id_r, id_lat, id_lon],
                                           gy[id_r, id_lat, id_lon],
                                           gz[id_r, id_lat, id_lon]])
                v_corr[id] = v[tid, id_lat, id_r, id_lon]
                id += 1
    assert id == lat.shape[0] * r.shape[0] * lon.shape[0]
    # p = pv.Plotter()
    # p.enable_depth_peeling()
    my_mesh = pv.PolyData(point_corr)
    my_mesh.point_arrays['solar wind speed'] = v_corr
    interp = grid.interpolate(my_mesh, radius=7, sharpness=5, strategy='mask_points')
    print(type(interp))
    vol_opac = [0, 0, .2, 0.2, 0.5, 0.5]
    p = pv.Plotter()
    p.enable_depth_peeling()
    # p.clear()
    p.add_volume(interp, opacity=vol_opac, **dargs)
    p.add_text("Iteration: {:.3f}".format(time[tid]), name='time-label')
    # p.write_frame()
    # p.save_graphic(filename='./fig/' + "{:0>3d}".format(tid)+'.eps')
    p.show(screenshot='./fig/' + "{:0>4d}".format(tid)+'.png', auto_close=True)
    p.close()
# p.close()




