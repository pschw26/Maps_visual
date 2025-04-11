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
import os 
import sys

# INTERPOLATE TOPOGRAPHY
repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, repo_path)

task = r'\ex6'

contours = gpd.read_file(repo_path + task + r'\topography_GMP_ex6.shp')

# contours.head()

# contours.plot(aspect='equal',column='Z', cmap='gist_earth', legend=True)
# plt.grid()

raster = gg.vector.interpolate_raster(gdf=contours,
                                      method='rbf')

# # raster[:2]

im = plt.imshow(raster, cmap='gist_earth', origin='lower')
plt.grid()
plt.colorbar(im)

# gg.raster.save_as_tiff(raster=raster,
#                        path= file_path + 'GMP_ex6_interpol_raster.tif',
#                        extent=[0,972,0,1069],
#                        crs='EPSG:4326',
#                        overwrite_file=True)
#%% # PLOT TOPOGRAPHY

import pyvista as pv

mesh = gg.visualization.read_raster(path=repo_path + task + r'\GMP_ex6_interpol_raster.tif',
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
#%% get X,Y,Z coordinates of the raster to be able to feed it into gempy geomodel
import rasterio
import numpy as np
import pandas as pd
import os 
import sys

# INTERPOLATE TOPOGRAPHY
repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, repo_path)

task = r'\ex6'



# Beispiel: Öffnen des Rasters mit Rasterio
with rasterio.open(repo_path + task + r"\GMP_ex6_interpol_raster.tif") as src:
    raster = src.read(1)  # Lies das erste Band (Z-Werte)
    transform = src.transform  # Georeferenzierung

# Extrahiere die X,Y Koordinaten
height, width = raster.shape  # Rastergröße
x_coords, y_coords = np.meshgrid(np.arange(width), np.arange(height))

# Transformiere die Koordinaten von Pixelkoordinaten in Weltkoordinaten (X,Y)
x_world, y_world = rasterio.transform.xy(transform, y_coords, x_coords)

# Die Z-Werte (Höhen) befinden sich im raster-Array
z_values = raster

# Erstelle ein Array der X, Y, Z Koordinaten
xyz_coordinates = np.column_stack((x_world, y_world, z_values.flatten()))
df = pd.DataFrame(xyz_coordinates)
df['formation'] = 'layer'
df.to_csv(repo_path + task + r'\raster.csv', index=False)


# Beispielausgabe der ersten paar Koordinaten
# print(xyz_coordinates[:5])








