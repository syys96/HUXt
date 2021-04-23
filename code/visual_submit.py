import numpy as np
import astropy.units as u
from astropy.time import Time
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import huxt as H
import huxt_analysis as HA
import huxt_inputs as Hin
import pyvista as pv
import os

if not os.path.exists('./fig/'):
    print('create directory to save screenshots')
    os.mkdir('./fig/')
else:
    print('fig directory already exists')

# set up a meridional cut run.
cr = 2210
vmap, vlats, vlongs = Hin.get_MAS_maps(cr)

model3d = H.HUXt3d(cr_num=cr, v_map=vmap, v_map_lat=vlats, v_map_long=vlongs,
                   latitude_max=20 * u.deg, latitude_min=-20 * u.deg,
                   lon_start=-180.0 * u.deg, lon_stop=179.0 * u.deg,
                   simtime=28 * u.day, r_min=30 * u.solRad)

cme = H.ConeCME(t_launch=10 * u.day, longitude=0.0 * u.deg, latitude=0.0 * u.deg,
                width=30 * u.deg, v=1000 * (u.km / u.s), thickness=5 * u.solRad)

# run the model
cme_list = [cme]
model3d.solve(cme_list)

# get the metadata from one of the individual HUXt elements
model = model3d.HUXtlat[0]
# save full data of shape: (time, lat, r, lon)
v = np.zeros([model.time_out.size, model3d.nlat,
              len(model.r), model.lon.size])
print(v.shape)
for num_lat in range(0, model3d.nlat):
    tmp_model = model3d.HUXtlat[num_lat]
    v[:, num_lat, :, :] = tmp_model.v_grid
lon = model.lon.to(u.deg).value / 180 * np.pi
lat = model3d.lat.to(u.deg).value
lat = (90 - lat) / 180 * np.pi
r = model.r.to(u.solRad).value
time = model.time_out.to(u.day).value
# end of save

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

p = pv.Plotter()
p.enable_depth_peeling()
p.open_movie('sw_submit.mp4')
for tid in range(0, v.shape[0], 10):
    id = 0
    for id_lat in range(lat.shape[0]):
        for id_r in range(r.shape[0]):
            for id_lon in range(lon.shape[0]):
                point_corr[id] = np.array([gx[id_r, id_lat, id_lon],
                                           gy[id_r, id_lat, id_lon],
                                           gz[id_r, id_lat, id_lon]])
                v_corr[id] = v[tid, id_lat, id_r, id_lon]
                id += 1
    assert id == lat.shape[0] * r.shape[0] * lon.shape[0]
    my_mesh = pv.PolyData(point_corr)
    my_mesh.point_arrays['solar wind speed'] = v_corr
    interp = grid.interpolate(my_mesh, radius=7, sharpness=5, strategy='mask_points')
    print(type(interp))
    vol_opac = [0, 0, .2, 0.2, 0.5, 0.5]
    p.clear()
    p.add_volume(interp, opacity=vol_opac, **dargs)
    p.add_text("Time: {:.3f} day".format(time[tid]), name='time-label')
    p.show(screenshot='./fig/' + "{:0>4d}".format(tid)+'.png', interactive_update=True)
    p.update()
    p.write_frame()
p.close()
