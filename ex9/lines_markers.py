# -*- coding: utf-8 -*-
"""
Created on Mon Jun 16 19:38:15 2025

@author: pschw
"""
from manim import *
import numpy as np

class fold(ThreeDScene):
    
    def construct(self):
        
        axes = ThreeDAxes(
            x_range=[-5, 5],
            y_range=[-5, 5],
            z_range=[-5, 5], 
            x_length=10,
            y_length=10,
            z_length=10)
        
        fold = Surface(lambda u, v: axes.c2p(*np.array([u,
                                                        v,
                                                        2*np.cos(v)])), 
                       u_range=[-2, 2], 
                       v_range=[-PI/2, PI/2], 
                       resolution=(32, 32)).set_color(PURPLE)
        
        fault_surf = Surface(lambda u, v: axes.c2p(*np.array([u, v, -2*u+2])), 
                             u_range=[-1, 2],
                             v_range=[-1, 2],
                             resolution=(32, 32)).set_color(PURPLE)
        
        limb_0_hanging = Polygon(
            [1, 2, 0],
            [2, 2, 0],  
            [2, 0, 2], 
            [0, 0, 2],   
            color=BLUE,
            fill_color=BLUE,
            fill_opacity=0.5
        )
        
        limb_1_hanging = Polygon(
            [1, -2, 0],
            [2, -2, 0],  
            [2, 0, 2], 
            [0, 0, 2],   
            color=BLUE,
            fill_color=BLUE,
            fill_opacity=0.5
        )
        
        
        limb_0_foot = Polygon(
            [1, 2, 0],
            [-1, 2, 0], 
            [-1, 0, 2], 
            [0, 0, 2], 
            color=RED,
            fill_color=RED,
            fill_opacity=0.5
        )
        
        limb_1_foot = Polygon(
            [1, -2, 0],
            [-1, -2, 0], 
            [-1, 0, 2], 
            [0, 0, 2], 
            color=RED,
            fill_color=RED,
            fill_opacity=0.5
        )
        
        
        FA_foot = Line(start=[-1, 0, 2], end=[0, 0, 2]).set_color(YELLOW)
        FA_hanging = Line(start=[0, 0, 2], end=[2, 0, 2]).set_color(YELLOW)
        
        displacement = always_redraw(lambda: Line(FA_foot.get_end(), FA_hanging.get_start(), stroke_color=GREEN))
        
        
        fold_foot = VGroup(limb_0_foot, limb_1_foot, FA_foot)
        fold_hanging = VGroup(limb_0_hanging, limb_1_hanging, FA_hanging)
        
        normal_arrow = Arrow3D(start=[0, 0, 2], end=[1, 0, 0])
        stirke_arrow = Arrow3D(start=[1, 0, 0], end=[1, 0.5, 0])
        
        label_normal = MathTex("\text{normal}").next_to(normal_arrow, DOWN).rotate(np.arctan(2), axis=RIGHT).rotate(PI/2, OUT).scale(0.7)
        label_strike = MathTex("\text{strike}").next_to(stirke_arrow, IN).rotate(np.arctan(2), axis=RIGHT).rotate(PI/2, OUT).scale(0.7)
        
        
        self.add(fold_hanging, fold_foot, fault_surf, displacement, axes)
        self.set_camera_orientation(zoom= 0.75, phi = 60*DEGREES, theta= 45*DEGREES)
        self.play(fold_hanging.animate.shift([1, 0.5, -2]))
        self.play(Create(normal_arrow), Create(stirke_arrow))
        self.play(Write(label_normal), Write(label_strike))
        self.wait(1)
        
