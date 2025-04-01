# -*- coding: utf-8 -*-
"""
Created on Mon Mar 17 17:51:29 2025

@author: wq271
"""

import geopandas as gpd
import gemgis as gg
import matplotlib.pyplot as plt  

file_path = 'C:/Users/wq271/GMP_SoSe24/GMP_Exercises/ex6/GMP_ex6/'



gmap = gpd.read_file(file_path + 'interfaces_GMP_ex6.shp')
# gmap

import matplotlib.pyplot as plt

gmap.plot(column='formation', aspect='equal', legend=True)
plt.grid()


stratigraphy = ['conglo', 'sand']

gmap_sorted = gg.vector.sort_by_stratigraphy(gdf=gmap,
                                             stratigraphy=stratigraphy)

gmap_sorted

intersection = gg.vector.intersection_polygon_polygon(polygon1=gmap_sorted.loc[0].geometry,
                                                      polygon2=gmap_sorted.loc[1].geometry)
intersection