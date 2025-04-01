# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 14:59:04 2024

@author: pschw
"""
import numpy as np
import pandas as pd
from scipy.spatial import Delaunay
from stl import mesh

# Step 1: Load the CSV file containing x, y, z data
df = pd.read_csv('C:/Daten/Peter/Studium/A_Programme_Hiwi/Projekte/Topo_conversion/Grid.csv')# Replace with your CSV file path

points = df[['x', 'y', 'z']].values  # Extract x, y, z columns as numpy array

# Step 2: Create a triangulation of the (x, y) coordinates
tri = Delaunay(points[:, :2])  # Triangulate the x, y coordinates

# Step 3: Create the mesh by defining faces (triangles)
faces = tri.simplices  # Triangulation produces the indices of the triangles

# Step 4: Create an empty mesh object
your_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))

# Step 5: Populate the mesh with the vertices and faces
for i, face in enumerate(faces):
    for j in range(3):
        your_mesh.vectors[i][j] = points[face[j], :]

# Step 6: Save the mesh to an STL file
your_mesh.save('C:/Daten/Peter/Studium/A_Programme_Hiwi/Projekte/Topo_conversion/output_grid.stl')


