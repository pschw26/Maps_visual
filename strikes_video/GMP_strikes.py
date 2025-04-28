# -*- coding: utf-8 -*-
"""
Created on Mon Apr 28 13:45:24 2025

@author: pschw
"""

from manim import *
import numpy as np

class strikes(ThreeDScene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.res = 32
    
    def construct(self):
        
        axes = ThreeDAxes(
            x_range=[-3, 3],
            y_range=[-3, 3],
            z_range=[-3, 3], 
            x_length=6,
            y_length=6,
            z_length=6,
        )
        
        x_label = MathTex("x").move_to(axes.c2p(3, 0, 0) + RIGHT)
        y_label = MathTex("y").move_to(axes.c2p(0, 3, 0) + UP)
        z_label = MathTex("z").move_to(axes.c2p(0, 0, 3) + OUT)
        
        upper = Surface(
            lambda u, v: axes.c2p(*np.array([u, v, 0])),
            u_range =[-2, 2],
            v_range =[-2, 2],
            resolution = (self.res, self.res)
            ).rotate(PI/4, axis=[1, 0, 0])
        
        lower = upper.copy()
        
        upper.shift([0, 0, 0.25] - upper.get_center())
        lower.shift([0, 0, -0.25] - upper.get_center())
        
        
        lm = Line(start=[-2, -1, -1], end=[2, -1, -1]).set_color(RED)
        lines = [lm]
        for i in range(8):
            ln = lm.copy().shift([0, 0.25, 0.25])
            lines.append(ln)
            lm = ln
            
        lower_color =  ManimColor.from_hex('#4dd730').to_hsv()
        upper_color =  ManimColor.from_hex('#ff0808').to_hsv()
        
        strikes_upper = list(map(lambda x: x.copy().shift([0, 0, 0.25]).set_color(upper_color), lines))
        strikes_lower = list(map(lambda x: x.copy().shift([0, 0, -0.25]).set_color(lower_color), lines))
        
        self.add(axes, x_label, y_label, z_label, *strikes_upper, *strikes_lower)
        self.set_camera_orientation(zoom=1, theta=0*DEGREES, phi=60*DEGREES)
            
        
        
        
        