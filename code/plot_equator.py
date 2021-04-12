import numpy as np
import astropy.units as u
from astropy.time import Time
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import huxt as H
import huxt_analysis as HA
import huxt_inputs as Hin


#set up a meridional cut run.
cr=2210
vmap, vlats, vlongs = Hin.get_MAS_maps(cr)

model3d=H.HUXt3d(cr_num=cr,v_map=vmap, v_map_lat=vlats, v_map_long=vlongs,
                    latitude_max=90*u.deg, latitude_min=-90*u.deg,
                    lon_out=0.0*u.deg,
                    simtime=1*u.day, r_min=30*u.solRad)

print(model3d.time_out)

daysec = 86400
times = [0.5*daysec, 1.5*daysec, 3*daysec]
speeds = [850, 1000, 700]
lons = [0, 90, 300]
widths = [30, 40, 20]
thickness = [5, 4, 2]
cme_list = []
for t, l, w, v, thick in zip(times, lons, widths, speeds, thickness):
    cme = H.ConeCME(t_launch=t*u.s, longitude=l*u.deg,
                    width=w*u.deg, v=v*(u.km/u.s), thickness=thick*u.solRad)
    cme_list.append(cme)


#run the model
model3d.solve(cme_list)
print(model3d.time_out)

#plot the equator
HA.plot(model3d, model3d.time_out[0])
plt.show()

#animate the meridional cut
HA.animate(model3d, tag='model3d-equator')
