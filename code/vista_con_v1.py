from pyvista import examples
import pyvista as pv
import numpy as np

# mesh = examples.load_random_hills()
#
# contours = mesh.contour()
#
# p = pv.Plotter()
# p.add_mesh(mesh, opacity=0.85)
# # p.add_mesh(contours, color="white", line_width=5)
# p.show()

mesh = examples.download_embryo()
print(mesh.points.shape)
exit(0)

contours = mesh.contour(np.linspace(50, 200, 10))

p = pv.Plotter()
p.add_mesh(mesh.outline(), color="k")
p.add_mesh(contours, opacity=0.25, clim=[0, 200])
p.camera_position = [(-130.99381142132086, 644.4868354828589, 163.80447435848686),
 (125.21748748157661, 123.94368717158413, 108.83283586619626),
 (0.2780372840777734, 0.03547871361794171, 0.9599148553609699)]
p.show()