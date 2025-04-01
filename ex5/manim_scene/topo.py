from manim import *
import numpy as np 
import os
os.chdir(r'C:\Users\wq271\GMP_SoSe24\GMP_Exercises\ex5\Topo_conversion')
import pandas as pd 

class CreateTopo(ThreeDScene):
    def __init__(self):
        df = pd.read_csv('Grid.csv', sep=',')
        self.x_data = np.array(df['x'])
        self.y_data = np.array(df['y'])
        self.z_data = np.array(df['z'])
    
    def func(self, u, v):
        return np.array([u, v, self.z_data])

    def construct(self):
        axes = ThreeDAxes(
            x_range=[np.min(self.x_data), np.max(self.x_data)],
            x_length=np.max(self.x_data) - np.min(self.x_data)
        )
        surface = Surface(
            lambda u, v: axes.c2p(*self.func(u, v)),
            u_range=[190, 1900],
            v_range=[-2100, -400],
            resolution=1700,
        )
        self.set_camera_orientation(theta=70 * DEGREES, phi=75 * DEGREES)
        self.add(axes, surface)
