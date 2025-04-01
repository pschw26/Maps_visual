# -*- coding: utf-8 -*-
"""
Created on Mon Mar 17 18:06:53 2025

@author: wq271
"""

import rasterio
import geopandas as gpd
import gemgis as gg
import matplotlib.pyplot as plt 
import numpy as np
import pyvista as pv 


file_path = 'C:/Users/wq271/GMP_SoSe24/GMP_Exercises/ex6/GMP_ex6/'

dem_work = rasterio.open(file_path + 'GMP_ex6_interpol_raster.tif')
# contours

grid = gg.visualization.create_dem_3d(dem=np.flipud(dem_work.read(1)), extent=[0,838,0,404])
# lines = gg.visualization.create_lines_3d_polydata(gdf=)

# grid

p = pv.Plotter()

p.add_mesh(mesh=grid, scalars=grid.z, cmap='gist_earth')

p.show_grid(color='black')
p.set_background(color='white')
p.show()
#%%
import rasterio
import pyvista as pv
import numpy as np
import gemgis as gg

file_path = 'C:/Users/wq271/GMP_SoSe24/GMP_Exercises/ex6/GMP_ex6/'

# Open the DEM raster file
dem_work = rasterio.open(file_path + 'GMP_ex6_interpol_raster.tif')

# Read the DEM data and flip it (as you did before)
# dem_data = dem_work.read(1)


# Create the 3D grid from the DEM data
grid = gg.visualization.create_dem_3d(dem=dem_work, extent=[0, 838, 0, 404])

# Ensure the scalar field has the same shape as the grid. Reshape the DEM data to match the grid's point structure
# Reshape dem_data if necessary, based on grid dimensions

# Plot the 3D grid with proper scalar field and colormap
p = pv.Plotter()

# Ensure the scalar field and colormap are applied correctly
p.add_mesh(grid, scalars=np.flipud(dem_work.read(1)), cmap="coolwarm", show_edges=False)

# Add grid lines and background settings
p.show_grid(color='black')
p.set_background(color='white')

# Show the plot
p.show()
#%%

import matplotlib.pyplot as plt
plt.imshow( np.flipud(dem_work.read(1)), cmap='gist_earth')
plt.colorbar()
plt.show()
