# -*- coding: utf-8 -*-
"""
Created on Wed Jun  4 15:27:05 2025

@author: pschw
"""

from manim import *
import numpy as np



class test(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes(
            x_range=[-5, 5],
            y_range=[-5, 5],
            z_range=[-5, 5], 
            x_length=10,
            y_length=10,
            z_length=10)
        
        self.add(axes)
        # self.add(self.surfstrikes(axes, 270, 45, 0.25, [-2, 2], [-2, 2], 32, show_surf=False))
        self.set_camera_orientation(phi = 60*DEGREES, theta = -45*DEGREES)
        
        Surf = Surface(lambda u,v: axes.c2p(*np.array([u, v, 0])), 
                    u_range = [-2, 2], 
                    v_range = [-2, 2], 
                    resolution = (32, 32)
                    )
        
        # create fault surface cutting the strike lines 
        dip_fault = np.radians(45)
        strike_fault = np.radians(90)
        
        Fault = Surface(lambda u,v: axes.c2p(*np.array([u, v, 0])), 
                    u_range = [-2, 2], 
                    v_range = [-2, 2], 
                    resolution = (32, 32)
                    ).set_color(RED).rotate(
                        dip_fault, axis=[0, 0, 1], about_point=ORIGIN)#.rotate(
                            #PI-strike_fault, axis=[0, 0, 1], about_point=ORIGIN)
        
                        
        # # rot about x for dip
        # rot_matrix_dip_fault = rotation_matrix(dip_fault, axis=RIGHT)  
        # Fault.apply_matrix(rot_matrix_dip_fault)
        # # rot about z for strike
        # rot_matrix_strike_fault = rotation_matrix(strike_fault, axis=OUT)  
        # Fault.apply_matrix(rot_matrix_strike_fault)
           
        # rotate the surface plane for the strikes                 
        dip = np.radians(60)
        strike = np.radians(135)  
        # # rot about x for dip
        # rot_matrix_dip = rotation_matrix(dip, axis=RIGHT)  
        # Surf.apply_matrix(rot_matrix_dip)
        # # rot about z for strike
        # rot_matrix_strike= rotation_matrix(strike, axis=OUT)  
        # Surf.apply_matrix(rot_matrix_strike)                  
 
        Surf.rotate(
            dip, axis=[0, 1, 0], about_point=ORIGIN).rotate(
                np.radians(-45), axis=[0, 0, 1], about_point=ORIGIN)
                
        self.add(Fault, Surf, Arrow3D(start=ORIGIN, end=[0.70710678, -0.70710678, 0]))
                
        
    def surfstrikes(self, axes, strike, dip, dz, urange, vrange, res, **kwargs):
        # convert degrees -> radians 
        dip = np.radians(dip)
        strike = np.radians(strike)
        
        # create strikes and surface
        Surf = Surface(lambda u,v: axes.c2p(*np.array([u, v, 0])), 
                    u_range = urange, 
                    v_range = vrange, 
                    resolution = (res, res)
                    )
        
        strike_fault = kwargs.get('strike', None)
        dip_fault = kwargs.get('dip', None)
        if (strike_fault is not None) & (dip_fault is not None):
            # create fault surface cutting the strike lines 
            dip_fault = np.radians(dip_fault)
            strike_fault = np.radians(strike_fault)
            Fault = Surface(lambda u,v: axes.c2p(*np.array([u, v, 0])), 
                        u_range = urange, 
                        v_range = vrange, 
                        resolution = (res, res)
                        ).rotate(
                            dip_fault, axis=[1, 0, 0], about_point=ORIGIN).rotate(
                                PI-strike_fault, axis=[0, 0, 1], about_point=ORIGIN)
            # rotate the surface plane for the strikes 
            Surf.rotate(
                dip, axis=[1, 0, 0], about_point=ORIGIN).rotate(
                    PI-strike, axis=[0, 0, 1], about_point=ORIGIN)
                
            # get corners of the planes and find upper and lower intersection
            Up_Surf = Line(start=Surf.get_corner(UL), end=Surf.get_corner(UR)).set_color(RED)
            Up_Fault = Line(start=Fault.get_corner(UL), end=Fault.get_corner(UR)).set_color(GREEN)
            
            
            Do_Surf = Line(start=Surf.get_corner(DL), end=Surf.get_corner(DR)).set_color(BLUE)
            Do_Fault = Line(start=Fault.get_corner(DL), end=Fault.get_corner(DR)).set_color(YELLOW)
            
            self.add(Up_Surf, Up_Fault, Do_Surf, Do_Fault, 
                     Dot3D(Up_Surf.get_center()), Dot3D(Do_Surf.get_center()))
                
        
        Strikes = [Line(start=[urange[0], vrange[0]+(dz*i/np.tan(dip)), 0], 
                        end  =[urange[1], vrange[0]+(dz*i/np.tan(dip)), 0]) 
                    for i in range(int(vrange[1]/dz)*2)]
        
        # create outputgroup
        show_surf = kwargs.get('show_surf', True)
        show_strikes = kwargs.get('show_strikes', True)
        if (show_surf==True) & (show_strikes==True):
            Group =  VGroup(Surf, *Strikes)
        elif show_surf==True:
            Group =  VGroup(Surf)
        elif show_strikes==True:
            Group =  VGroup(*Strikes)
        
        if (strike_fault is None) & (dip_fault is None):
            # rotate vertically for right dip
            Group.rotate(dip, axis=[1, 0, 0], about_point=ORIGIN)
            
            # rotate horizontally for right strike  
            Group.rotate(PI-strike, axis=[0, 0, 1], about_point=ORIGIN)
            
        return Group
        
        
        