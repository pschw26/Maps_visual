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

task = r'\ex8\simple_model'

'''TODO:
    - make random topo range smaller 
    - add points for fault over topography
    - increase topo resolution 
    - adapt shown Z-extent '''
#%% rotate coordinates back (map is tilted in file)

df_extent = pd.read_csv(repo_path + task + r'\extent_new_csv.csv', sep=',')
df_orientations = pd.read_csv(repo_path + task + r'\orientations_csv.csv', sep=',')
df_surface_points = pd.read_csv(repo_path + task + r'\surface_points_csv_new.csv', sep=',')

print(df_extent.head, df_orientations.head, df_surface_points.head)
 
# Winkel in Grad → z. B. 30°
winkel_grad = -70
theta = np.radians(winkel_grad)  # in Bogenmaß umwandeln

# Rotationsmatrix gegen den Uhrzeigersinn
R = np.array([
    [np.cos(theta), -np.sin(theta)],
    [np.sin(theta),  np.cos(theta)]
])
# Koordinaten extrahieren und rotieren
original_coords_ext = df_extent[['X', 'Y']].values
original_coords_ori = df_orientations[['X', 'Y']].values
original_coords_pnt = df_surface_points[['X', 'Y']].values

rot_coords_ext = original_coords_ext @ R.T  # Matrixmultiplikation
rot_coords_ori = original_coords_ori @ R.T 
rot_coords_pnt = original_coords_pnt @ R.T 

# Neue Koordinaten zum DataFrame hinzufügen
df_extent['X_rot'] = rot_coords_ext[:, 0]
df_extent['Y_rot'] = rot_coords_ext[:, 1]

df_orientations['X_rot'] = rot_coords_ori[:, 0]
df_orientations['Y_rot'] = rot_coords_ori[:, 1]

df_surface_points['X_rot'] = rot_coords_pnt[:, 0]
df_surface_points['Y_rot'] = rot_coords_pnt[:, 1]

# Optional: neue CSV speichern
df_extent.to_csv(repo_path + task + r'\extent_new_csv.csv', index=False)
df_orientations.to_csv(repo_path + task + r'\orientations_csv.csv', index=False)
df_surface_points.to_csv(repo_path + task + r'\surface_points_csv_new.csv', index=False)


#%% add topo raster


# extent = pd.read_csv(repo_path + task + r'\extent_new_csv.csv', sep=',')

data = gp.create_geomodel(
    project_name='GMP_ex8_model_simple',
    # extent=[int(extent.iloc[1,1])-1, int(extent.iloc[0,1])+1, 
    #         int(extent.iloc[1,2])-1, int(extent.iloc[0,2])+1, 100, 550],
    # extent: x_min, x_max, y_min, y_max, z_min, z_max
    extent=[0, 500, 
            0, 500, 100, 500],
    refinement=6, 
    importer_helper=gp.data.ImporterHelper(
        path_to_orientations=repo_path + task + r"\orientations.csv",
        path_to_surface_points=repo_path + task + r"\surface_points.csv"
    )
)

# clear cached files to ensure correct updating after changes in e.g. map_stack_to_surfaces
# data.structural_frame.structural_groups.clear()

# Map geological series to surfaces
gp.map_stack_to_surfaces(
    gempy_model=data,
    mapping_object={"Fault_Series": ('fault'),
                    "Strat_Series_1": ('S2', 'S1'),
                    "Strat_Series_2": ('C', 'B', 'A')}
)

data.structural_frame.structural_groups[0].structural_relation = StackRelationType.FAULT
data.structural_frame.fault_relations = np.array([[0, 1, 1], 
                                                  [0, 0, 0], 
                                                  [0, 0, 0]])


gp.set_topography_from_random(
    grid=data.grid,
    fractal_dimension=1.2,
    d_z=np.array([320, 500]),
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

# data.surfaces_df.loc[['A', 'B', 'C', 'fault', 'S1', 'S2'], 'color'] = ['#1f77b4', '#ff7f0e', '#2ca02c', 
#                                                            '#ff0000', '#cc00cc', '#0077cc']

colors = [['#ff0000'], ['#ff7f0e', '#ffe000'], ['#cc00cc', '#0077cc', '#3b05aa']]

for i,group in enumerate(data.structural_frame.structural_groups):
    for j in range(len(group.elements)):
        group.elements[j].color = colors[i][j]

# data.structural_frame.structural_groups[0].elements[0].color = '#ff0000'

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

with open(repo_path + task + r'\GMP_ex8_simple_geomodel.pkl', 'wb') as f:
    pickle.dump(geo_data, f)
#%%% plot top view of model

gpv.plot_2d(
    geo_data,
    # direction ='z',
    section_names=['topography'],
    show_topography=True,
    show_faults=True,       # Wichtig!
    show_boundaries=True,
    show_data=False,
    show_surfaces=True,
    legend = False,
    kwargs_topography= {'hillshade' : False, 'azdeg': 135, 'altdeg': 30},
    # hillshade_kwargs={'azimuth': 0, 'altitude': 90},
    # kwargs_contour ={'levels': 10, 'colors': 'black', 'linewidths': 0.5}
)

#%% cross sections
# gpv.plot_2d(data, show_faults=True, show_topography=True)

section_coords_AB = ([0, 250], 
                     [500, 250], 
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
import os

repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, repo_path)

task = r'\ex8\simple_model'

# Laden des gespeicherten GeoModels
with open(repo_path + task + r'\GMP_ex8_simple_geomodel.pkl', 'rb') as f:
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


