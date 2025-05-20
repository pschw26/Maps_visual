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
            x_range=[-4, 4],
            y_range=[-4, 4],
            z_range=[-4, 4], 
            x_length=8,
            y_length=8,
            z_length=8,
        )
        
        x_label = MathTex("x").move_to(axes.c2p(4, 0, 0) + 0.5*RIGHT)
        y_label = MathTex("y").move_to(axes.c2p(0, 4, 0) + 0.5*UP)
        z_label = MathTex("z").move_to(axes.c2p(0, 0, 4) + 0.5*OUT)
        
        lower_color = ManimColor("#4dd730")
        upper_color = ManimColor("#ff0808")
        
        upper = Surface(
            lambda u, v: axes.c2p(*np.array([u, v, 0])),
            u_range =[-2, 2],
            v_range =[-2, 2],
            resolution = (self.res, self.res)
            ).rotate(PI/4, axis=[1, 0, 0]).set_color(upper_color).set_opacity(0.5)
        
        lower = upper.copy().set_color(lower_color).set_opacity(0.5)
        
        upper.shift([0, 0, 0.25])
        lower.shift([0, 0, -0.25])
        
        
        lm = Line(start=[-2, -1, -1], end=[2, -1, -1])
        lm_proj = Line(start=[-2, -1, 0], end=[2, -1, 0])
        lines = [lm]
        lines_proj = [lm_proj]
        for i in range(8):
            ln = lm.copy().shift([0, 0.25, 0.25])
            ln_proj =  lm_proj.copy().shift([0, 0.25, 0])
            lines.append(ln)
            lines_proj.append(ln_proj)
            lm = ln
            lm_proj = ln_proj
        
        # Kopien der Linien mit verschobenen Z-Koordinaten
        strikes_upper_lines = [x.copy().shift([0, 0, 0.25]).set_color(upper_color) for x in lines]
        strikes_lower_lines = [x.copy().shift([0, 0, -0.25]).set_color(lower_color) for x in lines]
        
        
        project_upper = [DashedVMobject(x.copy().set_color(upper_color)) for x in lines_proj]
        project_lower = [x.copy().set_color(lower_color) for x in lines_proj]
        
        strike_labels_upper = []
        strike_labels_lower = []
        
        for i,strike in enumerate(strikes_upper_lines):
            height = 320 + i*20
            label_i_upper = MathTex(rf"{height}_{{S2-S3}}").move_to(strike.get_end()+0.4*RIGHT)
            label_i_upper.scale(0.3).set_color(upper_color).rotate(PI/4, axis=[0, 0, 1]).shift([0, 0.2, 0])
            strike_labels_upper.append(label_i_upper)
            # self.add(label_i_upper)
         
        for i,strike in enumerate(strikes_lower_lines):
            height = 300 + i*20
            label_i_lower= MathTex(rf"{height}_{{S1-S2}}").move_to(strike.get_start() + 0.4*LEFT)
            label_i_lower.scale(0.3).set_color(lower_color).rotate(3*PI/4, axis=[0, 0, 1]).shift([0, 0.2, 0])
            strike_labels_lower.append(label_i_lower)
            # self.add(label_i_lower)
        
        projected_labels_upper = [label.copy().shift([0, 0, -label.get_center()[2]]) for label in strike_labels_upper]
        projected_labels_lower = [label.copy().shift([0, 0, -label.get_center()[2]]) for label in strike_labels_lower]
    
        self.add(axes, x_label, y_label, z_label)#, *project_lower, *project_upper)#, *strikes_upper, *strikes_lower)
        # self.add(*strikes_upper_lines, *strikes_lower_lines)
        # self.add(*[obj.rotate(PI/4, axis=[0, 0, 1]).rotate(PI/3, axis=[0, 1, 0]) for obj in strike_labels_upper],
        #           *[obj.rotate(-PI/4, axis=[0, 0, 1]).rotate(PI/3, axis=[0, 1, 0]) for obj in strike_labels_lower])
        self.set_camera_orientation(zoom=1.5, theta=0*DEGREES, phi=0*DEGREES)

        
        # create projectied strikes and labels. Start with lower
        self.play(*[Create(obj) for obj in project_lower])
        self.wait(1)
        self.play(*[Write(obj) for obj in projected_labels_lower], run_time=3)
        self.wait(1)
        self.play(*[Create(obj) for obj in project_upper])
        self.wait(1)
        self.play(*[Write(obj) for obj in projected_labels_upper], run_time=3)
        self.wait(2)
        
        # show side and relocate labels while playing
        self.play(*[Uncreate(obj) for obj in project_lower], *[Unwrite(obj) for obj in projected_labels_lower], 
                  *[Uncreate(obj) for obj in project_upper], *[Unwrite(obj) for obj in projected_labels_upper])
        self.move_camera(phi=60*DEGREES, theta= -45*DEGREES)

        self.play(*[Create(obj) for obj in strikes_upper_lines], *[Create(obj) for obj in strikes_lower_lines])
        self.wait(1)
        self.play(*[Write(obj.rotate(PI/4, axis=[0, 0, 1]).rotate(PI/3, axis=[0, 1, 0])) for obj in strike_labels_upper],
                  *[Write(obj.rotate(-PI/4, axis=[0, 0, 1]).rotate(PI/3, axis=[0, 1, 0])) for obj in strike_labels_lower])
        self.wait(1)
        self.play(Create(upper), Create(lower), run_time=3)
        self.begin_ambient_camera_rotation(about='theta', rate=0.75)
        self.wait(8)
        self.stop_ambient_camera_rotation()
        self.wait(2)
        
        
        
        