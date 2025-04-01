from manim import *
import numpy as np 

class CreateSurface(ThreeDScene):

	
    def func(self, u, v):
        return np.array([u, v, np.sin(u) * np.sin(v)])

    def construct(self):
        axes = ThreeDAxes(x_range=[-4,4], x_length=8)
        surface = Surface(
            lambda u, v: axes.c2p(*self.func(u, v)),
            u_range=[-PI, PI],
            v_range=[0, TAU],
            resolution=8,
        )
        self.set_camera_orientation(theta=70 * DEGREES, phi=75 * DEGREES)
        self.add(axes, surface)