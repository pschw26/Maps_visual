# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 22:17:11 2025

@author: pschw
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


# add topo raster
file_path = 'C:/Daten/Peter/Studium/A_Programme_Hiwi/Projekte/Maps_visual/ex6/'

#%% create raw csv to later manipulate, so it fits with csv datapoints from raster (x,y,z) 

orientations_raw = gpd.read_file(file_path + 'orientations.shp')
df_orientations = pd.DataFrame(orientations_raw)
df_orientations.to_csv(file_path+'orientations.csv', index=False)

#%% create transformed orientationpoints 

# Lade die Orientierungspunkte
orientations = pd.read_csv(file_path+"orientations.csv")

# Lade das Raster, um die Transformationsmatrix zu bekommen
with rasterio.open(file_path+"GMP_ex6_interpol_raster.tif") as dataset:
    transform = dataset.transform
    
# Transformiere Pixelkoordinaten in Weltkoordinaten
orientations[["x_world", "y_world"]] = orientations.apply(
    lambda row: rasterio.transform.xy(transform, int(row["Y"]), int(row["X"])), axis=1, result_type="expand"
)


# Aktualisiere das DataFrame
orientations["x_world"] = x_world
orientations["y_world"] = y_world

orientations.to_csv(file_path+"orientations_transformed.csv", index=False)




