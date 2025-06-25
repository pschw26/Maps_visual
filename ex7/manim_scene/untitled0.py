# -*- coding: utf-8 -*-
"""
Created on Tue May 20 11:51:24 2025

@author: wq271
"""

"""create pseudo 3D scalar Temperature profile for 2D simulations """

import numpy as np
from matplotlib import pyplot as plt 

x_left = np.linspace(-8, 0, 16)
x_right = np.linspace(0, 8, 16)
x = np.linspace(-8, 8, 32)
z = np.linspace(-35, -5, 64)

X_left, Z_left = np.meshgrid(x_left, z)
X_right, Z_right = np.meshgrid(x_right, z)
X, Z = np.meshgrid(x, z)

coords_left = np.column_stack(np.array([X_left.ravel(), Z_left.ravel()]))
coords_right = np.column_stack(np.array([X_right.ravel(), Z_right.ravel()]))

def f(T0, coords, side, X, Z, dT_x, dT_z):
    Dx = abs(coords[:, 0] + (-1)**(side%2)*8)
    Dz = abs(coords[:, 1] + 20)
    print(Dx[:5], Dz[:5])
    dx = X.max() - X.min()
    dz = Z.max() - Z.min()
    return T0 - (Dx * dT_x/dx) - (Dz * dT_z/dz)

T_left = f(1000, coords_left, 0,  X_left, Z_left, 60, 100).reshape(Z_right.shape)
T_right = f(1000, coords_right, 1, X_right, Z_right, 60, 100).reshape(Z_right.shape)

T = np.hstack((T_left, T_right))



plt.pcolormesh(X, Z, T, cmap='viridis')

# plt.pcolormesh(X_left, Z, T_left, cmap='viridis')
# plt.pcolormesh(X_right, Z, T_right, cmap='viridis')
plt.colorbar()
plt.show()

#%%

import numpy as np
from matplotlib import pyplot as plt 

x = np.linspace(-8, 8, 32)
y = np.linspace(-8, 8, 32)
z = np.linspace(-35, -5, 64)

X, Y = np.meshgrid(x, y)

coords = np.column_stack(np.array([X.ravel(), Y.ravel()]))

def T(T0, dT_xy):
    distances = np.array([np.linalg.norm(pair) for pair in coords])
    dxy = 8
    return T0 + (distances * dT_xy/dxy) 

T0 = T(813, 60).reshape(X.shape)

plt.pcolormesh(X, Y, T0, cmap='viridis')
plt.colorbar()
plt.show()


dT_z = 100
dz = z.max() - z.min()


for i in range():
    T_layer_up = T(813) 
    




