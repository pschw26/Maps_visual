# -*- coding: utf-8 -*-
"""
Created on Wed Jun 18 11:52:59 2025

@author: pschw
"""

from manim import *
import numpy as np

class fault_fault(ThreeDScene):
    
    def construct(self):
        
        axes = ThreeDAxes(
            x_range=[-5, 5],
            y_range=[-5, 5],
            z_range=[-5, 5], 
            x_length=10,
            y_length=10,
            z_length=10)
        
        
        ### box_NW ###
        A = [-2, -2, 0]    # A: Oben links vorne
        B = [-2, -1, 0]  # B: Unten links vorne
        C = [1.5, -1, 0]   # C: Unten rechts vorne
        D = [1.5, -2, 0]   # D: Etwas weiter unten rechts vorne
        E = [0, -2, 2]    # H: Links unten hinten
        F = [-2, -2, 2]     # E: Tiefer unten rechts hinten (3D)
        G = [-2, 0, 2]      # F: Mittig oben hinten
        H = [0, 0, 2]     # G: Links oben hinten
  
        
        polygon_style_NW = {
           "color": RED,
           "fill_color": RED,
           "fill_opacity": 0.5
       }
        
        S_face = Polygon(D, C, H, E, **polygon_style_NW)
        E_face = Polygon(C, B, G, H, **polygon_style_NW)
        N_face = Polygon(B, A, F, G, **polygon_style_NW)
        W_face = Polygon(D, A, F, E, **polygon_style_NW)
        
        box_NW = VGroup(S_face, E_face, N_face, W_face)
        
        box_NW.shift(1/np.sqrt(5)*np.array([0,-1, -2]))
  
            
        ### box_NE ### 
        A = [-2, -1, 0]
        B = [-2, 2, 0] 
        C = [1.5, 2, 0]
        D = [1.5, -1, 0] 
        E = [-2, 0, 2] 
        F = [-2, 2, 2]
        G = [0, 2, 2] 
        H = [0, 0, 2]
        
        # corners = [A, B, C, D, E, F, G, H]
        
        # for corner in corners:
        #     corner = np.array(corner)+1/np.sqrt(5)*np.array([0, 1, -2])
        
        polygon_style_NE = {
           "color": BLUE,
           "fill_color": BLUE,
           "fill_opacity": 0.5
       }
        
        
        S_face = Polygon(D, C, G, H, **polygon_style_NE)
        E_face = Polygon(C, B, F, G, **polygon_style_NE)
        N_face = Polygon(B, A, E, F, **polygon_style_NE)
        W_face = Polygon(E, A, E, H, **polygon_style_NE)
        
        box_NE = VGroup(S_face, E_face, N_face, W_face)
        
        ### box_SW ###
        B = [1.5, -2, 0]  
        A = [1.5, -1, 0]  
        C = [2, -2, 0]
        D = [2, -1, 0] 
        E = [2, -2, 2] 
        F = [2, 0, 2]
        G = [0, -2, 2] 
        H = [0, 0, 2]
        
        polygon_style_SW = {
           "color": RED,
           "fill_color": RED,
           "fill_opacity": 0.2
       }
        
        
        S_face = Polygon(C, D, F, E, **polygon_style_SW)
        E_face = Polygon(A, D, F, H, **polygon_style_SW)
        N_face = Polygon(A, B, G, H, **polygon_style_SW)
        W_face = Polygon(B, C, E, G, **polygon_style_SW)
        
        box_SW = VGroup(S_face, E_face, N_face, W_face)
        
        box_SW.shift(1/np.sqrt(5)*np.array([0,-1, -2]))
        
        ### box_SE ###
        B = [1.5, 2, 0]  
        A = [1.5, -1, 0]  
        C = [2, 2, 0]
        D = [2, -1, 0] 
        E = [2, 2, 2] 
        F = [2, 0, 2]
        G = [0, 2, 2] 
        H = [0, 0, 2]
        
        polygon_style_SE = {
           "color": BLUE,
           "fill_color": BLUE,
           "fill_opacity": 0.2
       }
        
        
        S_face = Polygon(C, D, F, E, **polygon_style_SE)
        E_face = Polygon(A, D, F, H, **polygon_style_SE)
        N_face = Polygon(A, B, G, H, **polygon_style_SE)
        W_face = Polygon(B, C, E, G, **polygon_style_SE)
        
        box_SE = VGroup(S_face, E_face, N_face, W_face)
  
        
        self.add(box_NW, box_NE,#.shift(1/np.sqrt(2.5)*np.array([-1.5, 0, -2])),
                  box_SW.shift(1/np.sqrt(2.5)*np.array([1.5, 0, -2])), box_SE.shift(1/np.sqrt(2.5)*np.array([1.5, 0,-2]))
                 , axes)
        self.set_camera_orientation(zoom= 1, phi = 60*DEGREES, theta= 45*DEGREES)
        self.begin_ambient_camera_rotation(about='theta', rate=1.5)
        self.wait(4)
        self.stop_ambient_camera_rotation()
        
        
        