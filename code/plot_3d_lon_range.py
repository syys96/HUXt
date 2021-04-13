import numpy as np
import astropy.units as u
from astropy.time import Time
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import huxt as H
import huxt_analysis as HA
import huxt_inputs as Hin

# set up a meridional cut run.
cr = 2210
vmap, vlats, vlongs = Hin.get_MAS_maps(cr)

model3d = H.HUXt3d(cr_num=cr, v_map=vmap, v_map_lat=vlats, v_map_long=vlongs,
                   latitude_max=90 * u.deg, latitude_min=-90 * u.deg,
                   # lon_out=0.0*u.deg,
                   lon_start=-10 * u.deg, lon_stop=10 * u.deg,
                   simtime=28 * u.day, r_min=30 * u.solRad)

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
HA.animate_3d(model3d, lon=0 * u.deg, tag='model3d-lonrange')

# plot the meridional cut
HA.plot_3d_meridional(model3d, 0 * u.day, lon=0 * u.deg)
plt.show()
