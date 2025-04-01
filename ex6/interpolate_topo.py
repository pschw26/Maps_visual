# -*- coding: utf-8 -*-
"""
Created on Mon Mar 17 14:57:06 2025

@author: wq271
"""

# import sys 
# sys.path.append("C:/Users/wq271/appdata/local/anaconda3/envs/gemgis/lib/site-packages")
# sys.path.append(r'C:\Users\wq271\AppData\Local\anaconda3\envs\gemgis\Lib\site-packages\shapely')

import geopandas as gpd
import gemgis as gg
import matplotlib.pyplot as plt  

# INTERPOLATE TOPOGRAPHY

file_path= 'C:/Users/wq271/GMP_SoSe24/GMP_Exercises/ex6/GMP_ex6/'

contours = gpd.read_file(file_path + 'topography_GMP_ex6.shp')

# contours.head()

# contours.plot(aspect='equal',column='Z', cmap='gist_earth', legend=True)
# plt.grid()

raster = gg.vector.interpolate_raster(gdf=contours,
                                      method='rbf')
# raster[:2]

# im = plt.imshow(raster, cmap='gist_earth', origin='lower')
# plt.grid()
# plt.colorbar(im)

gg.raster.save_as_tiff(raster=raster,
                       path= file_path + 'GMP_ex6_interpol_raster.tif',
                       extent=[0,972,0,1069],
                       crs='EPSG:4326',
                       overwrite_file=True)
#%% # PLOT TOPOGRAPHY

import pyvista as pv

mesh = gg.visualization.read_raster(path=file_path + 'GMP_ex6_interpol_raster.tif',
                                    nodata_val=10000.0,
                                    name='Elevation [m]')

# mesh

topo = mesh.warp_by_scalar(scalars="Elevation [m]", factor=0.5)

topo

sargs = dict(fmt="%.0f", color='black')


p = pv.Plotter(notebook=False)
p.add_mesh(mesh=topo, cmap='gist_earth', scalar_bar_args=sargs, clim=[600, 1100])

p.set_background('white')
p.show_grid(color='black')
p.show()









