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
from gempy_engine.core.data.stack_relation_type import StackRelationType
import os
import sys

# os.environ['GDAL_DATA'] = 'C:/Users/pschw/anaconda3/envs/gemgis/Library/share/gdal'


# add topo raster
repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, repo_path)

task = r'\ex6'


dem_work = rasterio.open(repo_path + task + r'\GMP_ex6_interpol_raster.tif')
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
interfaces_raw = gpd.read_file(file_path + 'shapes_layers_fault.shp')
# interfaces.head()
series_object =  interfaces_raw.translate(-205.3966599010873892, 1240.6153075132974664)

interfaces = gpd.GeoDataFrame(pd.DataFrame(interfaces_raw), geometry=series_object, crs="EPSG:4326")
# extract z coords for points in interfaces and plot them
interfaces_coords = gg.vector.extract_xyz(gdf=interfaces, dem=dem_work)
# interfaces_coords


# add orientations
orientations_raw = gpd.read_file(file_path + 'orientations.shp')
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
        path_to_orientations=file_path + "orientations_transformed.csv",
        path_to_surface_points=file_path + "raster.csv",
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
interfaces_raw = gpd.read_file(repo_path + task + r'\shapes_layers_fault.shp')
# interfaces.head()
series_object =  interfaces_raw.translate(-205.3966599010873892, 1240.6153075132974664)

interfaces = gpd.GeoDataFrame(pd.DataFrame(interfaces_raw), geometry=series_object, crs="EPSG:4326")
# extract z coords for points in interfaces and plot them
interfaces_coords = gg.vector.extract_xyz(gdf=interfaces, dem=dem_work)
# interfaces_coords


# add orientations
orientations_raw = gpd.read_file(repo_path + task + r'\orientations.shp')
df_orientations = pd.DataFrame(orientations_raw)
df_orientations.to_csv(repo_path + task + r'\orientations.csv', index=False)
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
# structure data like input files in example model5 of gempy examples 

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
from gempy_engine.core.data.stack_relation_type import StackRelationType
from gempy.core.data import StructuralFrame
from gempy.core.data import SurfacePointsTable as spt
import os
import sys

# add topo raster
repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, repo_path)

task = r'\ex6'

# orientations = gpd.read_file(repo_path + task + r'\gempy_geomodel\orientations.shp')
# df_orientations = pd.DataFrame(orientations)
# df_orientations.to_csv(repo_path + task + r'\gempy_geomodel\orientations.csv', index=False)

# surface = gpd.read_file(repo_path + task + r'\gempy_geomodel\surface_points.shp')
# df_surface = pd.DataFrame(surface)
# df_surface.to_csv(repo_path + task + r'\gempy_geomodel\surface_points.csv', index=False)


# surface_df = pd.read_csv(repo_path + task + r"\gempy_geomodel\surface_points.csv")
# orientation_df = pd.read_csv(repo_path + task + r"\gempy_geomodel\orientations.csv")


data = gp.create_geomodel(
    project_name='GMP_ex6_model',
    extent=[203, 1038, -1305, -906, 500, 1200],
    refinement=7, 
    importer_helper=gp.data.ImporterHelper(
        path_to_orientations=repo_path + task + r"\gempy_geomodel\orientations.csv",
        path_to_surface_points=repo_path + task + r"\gempy_geomodel\surface_points.csv"
    )
)


# gp.set_surface_points(data, surface_df, surface_column='formation')
# gp.set_orientations(data, orientation_df, surface_column='formation')

# Map geological series to surfaces
gp.map_stack_to_surfaces(
    gempy_model=data,
    mapping_object={
        "Fault_Series": ['fault'],
        "Strat_Series": ['layer']
    }
)

# Define fault groups
data.structural_frame.structural_groups[0].structural_relation = StackRelationType.FAULT
data.structural_frame.fault_relations = np.array([[0, 1], [0, 0]])

# origin: X = 203,944; Y = -1305,260


# gpv.plot_3d(geo_data, show_data=True, show_boundaries=True, show_lith=True)
# gpv.plot_3d(geo_model, show_data=True, image=False, plotter_type='basic')


# Add topo raster

gp.set_topography_from_random(
    grid=data.grid,
    fractal_dimension=1.2,
    d_z=np.array([800, 1000]),
    topography_resolution=np.array([100, 100]),
)

# gp.set_topography_from_file(grid=data, 
#                             filepath= repo_path + task + r'\GMP_ex6_interpol_raster.tif', 
#                             crop_to_extent = [203, 1038, -1305, -906, 500, 1200])


# Compute the geological model
gp.compute_model(data)
geo_data = data

# Extrahieren der Lösungen
sol = data.solutions

# gpv.plot_2d(data, show_topography=True)
gpv.plot_3d(geo_data, show_data=False, show_topography=True, show_boundaries=True, show_lith=True)


