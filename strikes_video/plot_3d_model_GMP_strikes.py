# plot model 
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
repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, repo_path)

task = r'\strikes_video'

#%% add topo raster


# extent = pd.read_csv(repo_path + task + r'\extent_new_csv.csv', sep=',')

data = gp.create_geomodel(
    project_name='GMP_ex8_model',
    # extent=[int(extent.iloc[1,1])-1, int(extent.iloc[0,1])+1, 
    #         int(extent.iloc[1,2])-1, int(extent.iloc[0,2])+1, 100, 550],
    # extent: x_min, x_max, y_min, y_max, z_min, z_max
    extent=[0, 600, 
            0, 600, 0, 500],
    refinement=6, 
    importer_helper=gp.data.ImporterHelper(
        path_to_orientations=repo_path + task + r"\orientations.csv",
        path_to_surface_points=repo_path + task + r"\surface_points.csv"
    )
)


# Map geological series to surfaces
gp.map_stack_to_surfaces(
    gempy_model=data,
    mapping_object={"Strat_Series_1": ('Layer_1', 'Layer_2'), 
    }
)


gp.set_topography_from_random(
    grid=data.grid,
    fractal_dimension=1.1,
    d_z=np.array([350, 500]),
    topography_resolution=np.array([300, 300]),
)


# Beispiel: eine Linie von Punkt A nach Punkt B (egal wie schräg sie ist)
# section_coords_AB = ([826.366, -1069.119], [747.043, -167.843], [300, 300])  # X, Y Koordinaten
# section_coords_CD = ([410.603, -1069.119], [1339.231, -167.843], [300, 300])

# # Setze den Pfad für die Cross-Section
# gp.set_section_grid(
#     data.grid,
#     section_dict={  # beliebiger Name
#         r'Cross section $\overline{\text{AB}}$': section_coords_AB,
#         r'Cross section $\overline{\text{CD}}$': section_coords_CD
#     }  
# )

gp.compute_model(data)
geo_data = data


# gpv.plot_2d(
#     data,
#     section_names=[r'Cross section $\overline{\text{AB}}$'],
#     show_topography=True,
#     show_data=False,  # ax ist hier ein Array mit 2 Subplots
# )

# gpv.plot_2d(
#     data,
#     section_names=[r'Cross section $\overline{\text{CD}}$'],
#     show_topography=True,
#     show_data=False,  # ax ist hier ein Array mit 2 Subplots
# )
#%% plot and save 3D model

gpv.plot_3d(geo_data, show_data=False, show_boundaries=True, show_lith=True)
# # gpv.plot_3d(geo_model, show_data=True, image=False, plotter_type='basic')

import pickle 

with open(repo_path + task + r'\GMP_strikes_geomodel.pkl', 'wb') as f:
    pickle.dump(geo_data, f)
#%%% plot top view of model

gpv.plot_2d(
    data,
    # direction ='z',
    section_names=['topography'],
    show_topography=True,
    show_faults=True,       # Wichtig!
    show_boundaries=True,
    show_data=False,
    show_surfaces=True,
    legend = False,
    kwargs_topography= {'hillshade' : True, 'azdeg': 135, 'altdeg': 30}
    # hillshade_kwargs={'azimuth': 0, 'altitude': 90},
    # contour_kwargs={'levels': 10, 'colors': 'black', 'linewidths': 0.5}
)

#%% cross sections
# gpv.plot_2d(data, show_faults=True, show_topography=True)

section_coords_AB = ([1364.181, -1272.610], 
                     [1000.210, -1153.842], 
                     [300, 300])

# Setze den Pfad für die Cross-Section
gp.set_section_grid(
    data.grid,
    section_dict={  # beliebiger Name
        r'Cross section $\overline{\text{AB}}$': section_coords_AB,
    }  
)

gpv.plot_2d(
    data,
    section_names=[r'Cross section $\overline{\text{AB}}$'],
    show_topography=True,
    show_data=False,  # ax ist hier ein Array mit 2 Subplots
)

#%% open model from file

import pickle
import sys
import gempy_viewer as gpv

repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, repo_path)

task = r'\ex8'

# Laden des gespeicherten GeoModels
with open(repo_path + task + r'\GMP_ex8_geomodel.pkl', 'rb') as f:
    geo_data = pickle.load(f)
    
gpv.plot_3d(geo_data, show_data=False, show_boundaries=True, show_lith=True)

#%% Add topo raster (not yet included in gempy)

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


