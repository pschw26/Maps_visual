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

task = r'\ex4'

extent = pd.read_csv(repo_path + task + r'\extent_csv.csv', sep=',')

data = gp.create_geomodel(
    project_name='GMP_ex4_model',
    extent=[int(extent.iloc[0,1])-1, int(extent.iloc[1,1])+1, 
            int(extent.iloc[0,2])-1, int(extent.iloc[1,2])+1, 0, 800],
    refinement=6, 
    importer_helper=gp.data.ImporterHelper(
        path_to_orientations=repo_path + task + r"\orientations_csv.csv",
        path_to_surface_points=repo_path + task + r"\surface_points_csv.csv"
    )
)


# Map geological series to surfaces
gp.map_stack_to_surfaces(
    gempy_model=data,
    mapping_object={"Strat_Series": ('Selm_Folge', 'Dünensandstein', 
                                     'Wackenbach_Folge', 'Enztal_Sandstein')}
)


gp.set_topography_from_random(
    grid=data.grid,
    fractal_dimension=1.2,
    d_z=np.array([600, 800]),
    topography_resolution=np.array([100, 100]),
)


# Beispiel: eine Linie von Punkt A nach Punkt B (egal wie schräg sie ist)
section_coords_AB = ([826.366, -1069.119], [747.043, -167.843], [300, 300])  # X, Y Koordinaten
section_coords_CD = ([410.603, -1069.119], [1339.231, -167.843], [300, 300])

# Setze den Pfad für die Cross-Section
gp.set_section_grid(
    data.grid,
    section_dict={  # beliebiger Name
        r'Cross section $\overline{\text{AB}}$': section_coords_AB,
        r'Cross section $\overline{\text{CD}}$': section_coords_CD
    }  
)

gp.compute_model(data)
geo_data = data


gpv.plot_2d(
    data,
    section_names=[r'Cross section $\overline{\text{AB}}$'],
    show_topography=True,
    show_data=False,  # ax ist hier ein Array mit 2 Subplots
)

gpv.plot_2d(
    data,
    section_names=[r'Cross section $\overline{\text{CD}}$'],
    show_topography=True,
    show_data=False,  # ax ist hier ein Array mit 2 Subplots
)
#%%

gpv.plot_3d(geo_data, show_data=False, show_boundaries=True, show_lith=True)
# # gpv.plot_3d(geo_model, show_data=True, image=False, plotter_type='basic')

import pickle 

with open(repo_path + task + r'\GMP_ex4_geomodel.pkl', 'wb') as f:
    pickle.dump(geo_data, f)

#%%

import pickle
import sys
import gempy_viewer as gpv

repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, repo_path)

task = r'\ex4'

# Laden des gespeicherten GeoModels
with open(repo_path + task + r'\GMP_ex4_geomodel.pkl', 'rb') as f:
    geo_data = pickle.load(f)
    
gpv.plot_3d(geo_data, show_data=False, show_boundaries=True, show_lith=True)

#%%
# # Add topo raster

# gp.set_topography_from_random(
#     grid=data.grid,
#     fractal_dimension=1.2,
#     d_z=np.array([800, 1000]),
#     topography_resolution=np.array([100, 100]),
# )

# # gp.set_topography_from_file(grid=data, 
# #                             filepath= repo_path + task + r'\GMP_ex6_interpol_raster.tif', 
# #                             crop_to_extent = [203, 1038, -1305, -906, 500, 1200])


# # Compute the geological model
# gp.compute_model(data)
# geo_data = data

# # Extrahieren der Lösungen
# sol = data.solutions

# gpv.plot_2d(data, show_topography=True)
# gpv.plot_3d(geo_data, show_data=False, show_topography=True, show_boundaries=True, show_lith=True)


