import numpy as np
import astropy.units as u
from astropy.time import Time
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import huxt as H
import huxt_analysis as HA
import huxt_inputs as Hin
import pyvista

# set up a meridional cut run.
cr = 2210
vmap, vlats, vlongs = Hin.get_MAS_maps(cr)

model3d = H.HUXt3d(cr_num=cr, v_map=vmap, v_map_lat=vlats, v_map_long=vlongs,
                   latitude_max=90 * u.deg, latitude_min=-90 * u.deg,
                   # lon_out=0.0*u.deg,
                   lon_start=-60 * u.deg, lon_stop=60 * u.deg,
                   simtime=1 * u.day, r_min=30 * u.solRad)

daysec = 86400
times = [5 * daysec, 15 * daysec, 20 * daysec]
speeds = [850, 1000, 700]
lons = [0, 0, 0]
lats = [-45, 0, 45]
widths = [30, 40, 20]
thickness = [5, 4, 2]
cme_list = []
for t, l, w, v, thick, lat in zip(times, lons, widths, speeds, thickness, lats):
    cme = H.ConeCME(t_launch=t * u.s, longitude=l * u.deg, latitude=lat * u.deg,
                    width=w * u.deg, v=v * (u.km / u.s), thickness=thick * u.solRad)
    cme_list.append(cme)

# run the model
model3d.solve(cme_list)

# animate the meridional cut
# HA.animate_3d(model3d, lon=0 * u.deg, tag='model3d-lonrange')

# plot the meridional cut
HA.plot_3d_meridional(model3d, 0 * u.day, lon=0 * u.deg)
# HA.plot(model3d, 0 * u.day)
plt.show()

lat = model3d.lat
lon = model3d.HUXtlat[0].lon
r = model3d.HUXtlat[0].r_grid[:, 0]

lons, lats, rs = np.meshgrid(lon, lat, r)

v = np.zeros((len(lat), len(lon), len(r)))

for i in range(len(lat)):
    v[i, :, :] = np.transpose(model3d.HUXtlat[i].v_grid[0])

# Make a grid
x = rs * np.cos(lats) * np.cos(lons)
y = rs * np.cos(lats) * np.sin(lons)
z = rs * np.sin(lats)

points = np.empty((x.size, 3))
points[:, 0] = x.ravel('F')
points[:, 1] = y.ravel('F')
points[:, 2] = z.ravel('F')

# # Compute a direction for the vector field
vd = np.zeros((len(lat), len(lon), len(r), 3))
vd[:, :, :, 0] = v * np.cos(lats) * np.cos(lons)
vd[:, :, :, 1] = v * np.cos(lats) * np.sin(lons)
vd[:, :, :, 2] = v * np.sin(lats)
direction = np.reshape(vd, (len(points[:, 0]), 3), order='F')


print('begin vista plot')
# plot using the plotting class
plobj = pyvista.Plotter()
print('1')
plobj.camera_position = [(3500, 3500, 0), (0, 1, 0), (0, 0, 1000)]
print('2')
plobj.add_arrows(points, direction, 1.0)
print('3')
plobj.show_grid()
print('4')
plobj.show(screenshot='vectorfield.png')
print('5')