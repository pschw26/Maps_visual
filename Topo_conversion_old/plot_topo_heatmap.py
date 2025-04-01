# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 18:53:56 2024

@author: pschw
"""

'''TODO: 
    - (implement right scale in QGIS)
    - automate process with model designer (based on vector-file)
    - (test for more complex topography)
    - make surface even smoother
    - what file-format does a 3D printer need, what file format does a cnc need?'''

import pandas as pd 
import numpy as np 
from matplotlib import pyplot as plt
from scipy.interpolate import griddata
from scipy.ndimage import uniform_filter
from scipy import ndimage
from scipy.ndimage import gaussian_filter
import math

# import matplotlib.colors as mcolors

# Generiere 10 zufällige Farben aus einem colormap
def generate_random_colors(num_colors):
    colormap = plt.get_cmap('hsv')  # HSV-Farbmap, die ein breites Spektrum abdeckt
    return [colormap(i / num_colors) for i in range(num_colors)]

# Erzeuge 10 zufällige Farben
random_colors = generate_random_colors(10)


data = pd.read_csv('C:/Daten/Peter/Studium/A_Programme_Hiwi/Projekte/Topo_conversion/attribut_table_coords_evenscatter_scaled_complete.csv')

# x = np.linspace(100, 700, 1000)
# y = np.linspace(-1200, -600, 1000)

# X, Y = np.meshgrid(x, y)

# x = np.array(data['xcoord'])
# y = np.array(data['ycoord'])
# z = np.array(data['id'])
height_450 = data[data['id'] == 450]
height_500 = data[data['id'] == 500]
height_550 = data[data['id'] == 550]
height_600 = data[data['id'] == 600]
height_650 = data[data['id'] == 650]
height_700 = data[data['id'] == 700]
height_750 = data[data['id'] == 750]
height_800 = data[data['id'] == 800]
height_850 = data[data['id'] == 850]
height_900 = data[data['id'] == 900]

x_1 = np.array(height_800['xcoord'])
y_1 = np.array(height_800['ycoord'])
z_1 = np.array(height_800['id'])

x_2 = np.array(height_850['xcoord'])
y_2 = np.array(height_850['ycoord'])
z_2 = np.array(height_850['id'])

x_3 = np.array(height_900['xcoord'])
y_3 = np.array(height_900['ycoord'])
z_3 = np.array(height_900['id'])

x_4 = np.array(height_750['xcoord'])
y_4 = np.array(height_750['ycoord'])
z_4 = np.array(height_750['id'])

x_5 = np.array(height_700['xcoord'])
y_5 = np.array(height_700['ycoord'])
z_5 = np.array(height_700['id'])

x_6 = np.array(height_650['xcoord'])
y_6 = np.array(height_650['ycoord'])
z_6 = np.array(height_650['id'])

x_7 = np.array(height_600['xcoord'])
y_7 = np.array(height_600['ycoord'])
z_7 = np.array(height_600['id'])

x_8 = np.array(height_550['xcoord'])
y_8 = np.array(height_550['ycoord'])
z_8 = np.array(height_550['id'])

x_9 = np.array(height_500['xcoord'])
y_9 = np.array(height_500['ycoord'])
z_9 = np.array(height_500['id'])

x_10 = np.array(height_450['xcoord'])
y_10 = np.array(height_450['ycoord'])
z_10 = np.array(height_450['id'])


# for i in range(10):
#     plt.scatter()
# heatmap plot of different heights in 2D
# plt.scatter(x_1, y_1, color= 'green')
# plt.scatter(x_2, y_2, color= 'yellow')
# plt.scatter(x_3, y_3, color= 'red')

# heatmap plot of different heights in 3D
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.scatter(x_1, y_1, z_1, color='green')
# ax.scatter(x_2, y_2, z_2, color='yellow')
# ax.scatter(x_3, y_3, z_3, color='red')

# plt.show()


# Punktkoordinaten
points = data[['xcoord_scaled', 'ycoord_scaled']].to_numpy()
values = data['id'].to_numpy()

# Erstelle ein Gitter für die Interpolation
grid_x, grid_y = np.mgrid[190:1900:, -2100:-400:1700j]  # Beispiel-Gitter

# Interpolation der Höhenwerte auf das Gitter
grid_z = griddata(points, values, (grid_x, grid_y), method='linear')

# Subsample every 10th value from the grid in both x and y directions
subsampled_grid_x = grid_x[::10, ::10]
subsampled_grid_y = grid_y[::10, ::10]
subsampled_grid_z = grid_z[::10, ::10]
            

# Apply Gaussian filter to smooth the grid_z
sigma = 2  # Standard deviation of the Gaussian kernel
smoothed_grid_z = gaussian_filter(subsampled_grid_z, sigma=sigma)

# # The size of the filter can be adjusted; here we use size 3 for simplicity
# # Convert the grid to a DataFrame
# df = pd.DataFrame(subsampled_grid_z)

# # Apply moving average with a window size of 3
# smoothed_df = df.rolling(window=15, min_periods=1, axis=0).mean()

# # Convert back to numpy array
# smoothed_grid_z = smoothed_df.to_numpy()

# # # Flatten the subsampled and smoothed grid data
flat_subsampled_x = subsampled_grid_x.flatten()
flat_subsampled_y = subsampled_grid_y.flatten()
flat_subsampled_z = smoothed_grid_z.flatten()

for i,item in enumerate(flat_subsampled_z):
    if np.isnan(item):
        flat_subsampled_z[i] = 0.0

# # # Create a DataFrame with the subsampled and smoothed (x, y, z) values
df = pd.DataFrame({
    'x': flat_subsampled_x,
    'y': flat_subsampled_y,
    'z': flat_subsampled_z
})

# # Optional: Save the DataFrame to a CSV file
df.to_csv('C:/Daten/Peter/Studium/A_Programme_Hiwi/Projekte/Topo_conversion/Grid.csv', index=False)

# Grid.to_csv('C:/Daten/Peter/Studium/A_Programme_Hiwi/Projekte/Topo_conversion/Grid.csv', sep='\t', index=False)

# Visualisierung der interpolierten Daten
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(grid_x, grid_y, grid_z, cmap='viridis')

ax.set_zlim(0, 1700)

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Höhe')

ax.view_init(elev=30, azim=-75)
plt.show()



