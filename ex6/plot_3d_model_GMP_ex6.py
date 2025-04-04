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
from shapely.geometry import Point
import pandas as pd 
import gempy as gp
import gempy_viewer as gpv
import os
import sys

# os.environ['GDAL_DATA'] = 'C:/Users/pschw/anaconda3/envs/gemgis/Library/share/gdal'


# add topo raster
repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, repo_path)

task = r'\ex6'


dem_work = rasterio.open(repo_path + task + 'GMP_ex6_interpol_raster.tif')
# contours

grid = gg.visualization.create_dem_3d(dem=np.flipud(dem_work.read(1)), extent=[0,838,0,404])
# lines = gg.visualization.create_lines_3d_polydata(gdf=)

grid.points[:,2] *= 0.5


# fix, ax = plt.subplots(1, figsize=(10, 10))
# # topo.plot(ax=ax, aspect='equal', column='Z', cmap='gist_earth')
# im = plt.imshow(np.flipud(dem_work.read(1)), origin='lower', extent=[0, 838, 0, 404], cmap='gist_earth')
# cbar = plt.colorbar(im)
# cbar.set_label('Altitude [m]')
# ax.set_xlabel('X [m]')
# ax.set_ylabel('Y [m]')
# ax.set_xlim(0, 838)
# ax.set_ylim(0, 404)


# add interfaces
interfaces_raw = gpd.read_file(repo_path + task + 'shapes_layers_fault.shp')
# interfaces.head()
series_object =  interfaces_raw.translate(-205.3966599010873892, 1240.6153075132974664)

interfaces = gpd.GeoDataFrame(pd.DataFrame(interfaces_raw), geometry=series_object, crs="EPSG:4326")
# extract z coords for points in interfaces and plot them
interfaces_coords = gg.vector.extract_xyz(gdf=interfaces, dem=dem_work)
# interfaces_coords


# add orientations
orientations_raw = gpd.read_file(repo_path + task + 'orientations.shp')
df_orientations = pd.DataFrame(orientations_raw)
df_orientations.to_csv(file_path+'orientations.csv', index=False)
# interfaces.head()
series_object =  orientations_raw.translate(-205.3966599010873892, 1240.6153075132974664)

orientations = gpd.GeoDataFrame(pd.DataFrame(orientations_raw), geometry=series_object, crs="EPSG:4326")


#create model
# geo_model = gp.create_geomodel()
# geo_model
# gp.init_data(geo_model, [0, 838, 0, 404, 570, 1144], [100, 100, 100],
#               surface_points_df=interfaces_coords,
#               orientations_df=orientations,
#               default_values=True)
#%% plot model 
geo_model: gp.data.GeoModel = gp.create_geomodel(
    project_name='GMP_ex6_model',
    extent=[0, 838, 0, 404, 570, 1144],
    refinement=6,  # * Here we define the number of octree levels. If octree levels are defined, the resolution is ignored.
    importer_helper=gp.data.ImporterHelper(
        path_to_orientations=repo_path + task + "orientations_transformed.csv",
        path_to_surface_points=repo_path + task + "raster.csv",
    )
)

gpv.plot_3d(geo_model, show_data=True, image=False, plotter_type='basic')



# p = pv.Plotter()

# p.add_mesh(mesh=grid, scalars=grid.points[:, 2], cmap='gist_earth')

# p.show_grid(color='black')
# p.set_background(color='white')
# p.show()

# Extent interfaces
# 205.3966599010873892,-1240.6153075132974664 : 1037.9668758311170222,-1041.0871447811316557


