from manim import *
import numpy as np 
import sys

class CreateTopo(ThreeDScene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # Initialize the parent class
        self.order = 10
        self.params = [np.random.rand()*0.5*(-1)**np.random.randint(2) for i in range(self.order)]

    def func(self, u, v):
        return np.array([
            u, 
            v, 
            (sum([self.params[i]*u**i for i in range(self.order//2)]) * sum([self.params[-i]*v**i for i in range(1, (self.order//2)+1)]))+2
        ])

    def construct(self):
        # Define 3D axes
        axes = ThreeDAxes(
            x_range=[-5, 5],
            y_range=[-5, 5],
            z_range=[-5, 5],  # Adjust z_range to fit your surface
            x_length=10,
            y_length=10,
            z_length=10,
        )

        # Define surface
        surface = Surface(
            lambda u, v: axes.c2p(*self.func(u, v)),
            u_range=[-2, 2],
            v_range=[-2, 2],
            resolution=(32, 32),  # Higher resolution for smoother surface
        )
        surface.set_fill(BLUE, opacity=1)  # Uniform blue surface
        surface.stroke_width = 2

        # Set camera orientation

	# Add axes and surface to the scene
        self.add(axes, surface)


