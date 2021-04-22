# sphinx_gallery_thumbnail_number = 4
import pyvista as pv
from pyvista import examples

# Download sample data
surface = examples.download_saddle_surface()
points = examples.download_sparse_points()

print(surface.points.shape)
print(points.points.shape)
exit(0)

interpolated = surface.interpolate(points, radius=12.0)


p = pv.Plotter()
p.add_mesh(points, point_size=30.0, render_points_as_spheres=True)
p.add_mesh(interpolated, scalars="val")
p.show()