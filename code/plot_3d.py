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
                    latitude_max=20*u.deg, latitude_min=-20*u.deg,
                    lon_start=-180.0*u.deg,lon_stop=179.0*u.deg,
                    simtime=28*u.day, r_min=30*u.solRad)

cme = H.ConeCME(t_launch=10*u.day, longitude=0.0*u.deg, latitude=0.0*u.deg,
                width=30*u.deg, v=1000*(u.km/u.s), thickness=5*u.solRad)

#run the model
cme_list=[cme]
model3d.solve(cme_list)

#plot the meridional cut
HA.plot_3d_meridional(model3d, 1*u.day, lon=5*u.deg)

#animate the meridional cut
HA.animate_3d(model3d, lon=0*u.deg, tag='model3d')

plt.show()
