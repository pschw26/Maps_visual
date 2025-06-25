# -*- coding: utf-8 -*-
"""
Created on Sat May  3 12:49:55 2025

@author: pschw
"""
from  manim import *
import numpy as np

class crosscut(ThreeDScene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.res = 32
    
    def Map(self, array, function):
        return [function(item) for item in array]
    
    def construct(self):
        # create cartesian coord sys
        axes = ThreeDAxes(
            x_range=[-5, 5],
            y_range=[-5, 5],
            z_range=[-5, 5], 
            x_length=10,
            y_length=10,
            z_length=10,
        )
        
        label_x = MathTex('x').move_to(axes.c2p(5, 0, 0)+0.3*RIGHT)
        label_y = MathTex('y').move_to(axes.c2p(0, 5, 0)+0.3*UP)
        label_z = MathTex('z').move_to(axes.c2p(0, 0, 5)+0.3*OUT)
    
        
        strikes_hanging = VGroup(*[Line(start=[-2+i*0.536, -2, -1+i*0.25], 
                                        end=[-2+i*0.536, 2-i*0.536, -1+i*0.25])
                                        .set_color(GREEN_B) for i in range(8)])
        
        strikes_hanging_projected = VGroup(*[Line(start=[-2+i*0.536, -2, 0], 
                                        end=[-2+i*0.536, 2-i*0.536, 0])
                                        .set_color(GREEN_B) for i in range(8)])
        
        
        strikes_foot = VGroup(*[Line(start=strikes_hanging[i].get_end()-0.625*OUT, 
                                     end= [-2+i*0.536, 2, -1-0.625+i*0.25])
                                     .set_color(WHITE) for i in range(8)])
        
        strikes_foot_projected = VGroup(*[Line(start=strikes_hanging_projected[i].get_end(), 
                                     end= [-2+i*0.536, 2, 0])
                                     .set_color(WHITE) for i in range(8)])
        
        
        strikes_fault_projected = VGroup(*[Line(start=[-3, 2*0.25/np.tan(np.radians(35))-i*0.25/np.tan(np.radians(35)), 0], 
                                                end = [3, 2*0.25/np.tan(np.radians(35))-i*0.25/np.tan(np.radians(35)), 0])
                                         .set_color(RED)for i in range(5)])
        
        # create vectors and rotate 
        # start = 0.5 * (strikes_hanging[-1].get_start() + strikes_hanging[-1].get_end())
        # theta = np.radians(45)


        # R = np.array([
        #     [np.cos(theta), -np.sin(theta), 0],
        #     [np.sin(theta),  np.cos(theta), 0],
        #     [0,              0,             1]
        # ])
        
        # start_rot = R @ start
        # end_disp_rot = R @ (start-[0.625/np.tan(np.radians(25)), 0, 0.625])
        # end_sprung_rot = R @ (start-[0, 0, 0.625])
        
        strikes = VGroup(*[strikes_hanging, strikes_foot])
        strikes_projected = VGroup(*[strikes_hanging_projected, strikes_foot_projected])
        
        strikes.rotate(PI/4, axis=OUT, about_point=ORIGIN)
        strikes_projected.rotate(PI/4, axis=OUT, about_point=ORIGIN)
        
        strikes_hanging_projected.shift([-2*0.536/np.cos(np.pi/4), 0, 0])
        
        
        
        # shift lines to end perfectly on fault surface 
        for i in range(8):
            strikes_hanging[i].shift([0, strikes_hanging[i].get_center()[2]*0.625/np.tan(np.radians(20)), 0])
            strikes_foot[i].shift([0, strikes_foot[i].get_center()[2]*0.625/np.tan(np.radians(20)), 0])




        # strikes trans
        strikes_hanging_trans = VGroup(*[line.copy().shift([-np.sqrt(0.125), 0 , 0]).set_color(GREEN_B) #TODO: changed disp vector
                                         for line in strikes_hanging])
        
        strikes_hanging_trans_projected = VGroup(*[line.copy().shift([-0.125/np.cos(np.pi/4), 0, 0]).set_color(GREEN_B)
                                         for line in strikes_hanging_projected])

        # place vectors 
        start = strikes_hanging[-1].get_center()
        disp_vector = Arrow3D(start, start-[0.625/np.tan(np.radians(30)), 
                                            0.625/np.tan(np.radians(30)), 
                                            0.625]).set_color(PURE_RED)
        sprung = Arrow3D(start, start-[0, 0, 0.625]).set_color(PURE_RED)
        
        
        
        # add sprung vector label
        label_sprung = MathTex(r'\Delta z\, = \, 50 \,\text{m}').set_color(PURE_RED).scale(0.4)
        label_sprung.move_to(sprung.get_center()+0.7*UP).rotate(PI/2, axis=UP).rotate(PI/2, axis=RIGHT)


        # print(np.array([lines_1[5].get_start() - lines_1[5].get_center()[2]/np.tan(35*DEGREES)]))
            
        # labels for strikes on hangingwall
        strike_labels_hanging = [MathTex(rf'{300+i*25}_{{A-B}}')
                              .move_to(line.get_start()+ 0.4*RIGHT)
                              .scale(0.4)
                              .set_color(GREEN_B)
                              .rotate(PI/2, axis=[0, 0, 1]) 
                              .shift([-0.2, -0.2, 0])
                              for i,line in enumerate(strikes_hanging_projected)]
        
        # labels for strikes on footwall 
        strike_labels_foot = [MathTex(rf'{300+i*25}_{{A-B}}')
                              .move_to(line.get_end()+ 0.4*LEFT)
                              .scale(0.4)
                              .set_color(WHITE)
                              .rotate(PI/2, axis=[0, 0, 1]) 
                              .shift([0.2, 0.2, 0])
                              for i,line in enumerate(strikes_foot_projected)]
        
        # labels for fault 
        strike_labels_fault = [MathTex(rf'{425-i*25}_\text{{fault}}')
                             .move_to(line.get_end()+ 0.3*RIGHT)
                             .scale(0.4)
                             .set_color(RED)
                             .rotate(PI/4, axis=[0, 0, 1]) 
                             .shift([0.2, 0, 0])
                             for i,line in enumerate(strikes_fault_projected)]
        
        # labels for example with strike slip component 
        strike_labels_hanging_trans = [MathTex(rf'{300+i*25}_{{A-B}}')
                              .move_to(line.get_start()+ 0.4*RIGHT)
                              .scale(0.4)
                              .set_color(GREEN_B)
                              .rotate(PI/2, axis=[0, 0, 1]) 
                              .shift([-0.2, -0.2, 0])
                              for i,line in enumerate(strikes_hanging_trans_projected)]
        
            
        
        # fault surface 
        Surf = Surface(lambda u, v: axes.c2p(*np.array([u, v, np.sin(np.radians(35))*v])),
                       u_range= [-3, 3],
                       v_range=[-3, 3],
                       resolution= (self.res, self.res)).set_color(RED)
        

        self.add(axes, label_x, label_y, label_z)
        # self.set_camera_orientation(zoom = 1, theta= -45*DEGREES, phi= 60*DEGREES)
        # strike_slip = Arrow3D(start, start+[np.sqrt(0.125), 0, 0], thickness=0.02, height=0.1, base_radius=0.05).set_color(PURE_RED)
        # self.add(strike_slip)
        # # test if projected strikes work
        # self.add(strikes_projected, *strike_labels_foot, *strike_labels_hanging, strikes_fault_projected, *strike_labels_fault, 
        #           strikes_hanging_trans_projected, *strike_labels_hanging_trans)
        # self.add(strikes_fault_projected, *strike_labels_fault)
        # # test if 3D strikes work 
        # self.add(strikes_hanging, strikes_foot, Surf, strikes_hanging_trans)
        # # self.move_camera(phi= 90*DEGREES, theta= 0)
        # self.add(strikes_hanging_trans, strikes_foot, Surf)
        # self.play(strikes_hanging_trans.animate.shift([0, -0.625/np.tan(np.radians(30)), -0.625]))
        # self.wait(1)
        # self.play(strikes_hanging_trans.animate.shift([np.sqrt(0.125), np.sqrt(0.125), 0]))
        # self.begin_ambient_camera_rotation(about='theta', rate=0.75)
        # self.wait(4)
        # self.stop_ambient_camera_rotation()
        # self.add(disp_vector, sprung)
        

        # add projected strikes and their labels
        self.set_camera_orientation(zoom = 1, theta= 0*DEGREES, phi= 0*DEGREES)
        self.play(Create(strikes_hanging_projected), Create(strikes_foot_projected))
        self.play(Create(strikes_fault_projected))
        self.wait(1)
        self.wait(1)
        self.play(*self.Map(strike_labels_hanging, Write))
        self.wait(1)
        self.play(*self.Map(strike_labels_foot, Write))
        self.wait(1)
        self.play(*self.Map(strike_labels_fault, Write))
        self.wait(2)
        
        # # remove projected strikes and labels and move camera to start rotation
        self.play(Uncreate(strikes_hanging_projected), 
                  Uncreate(strikes_foot_projected), 
                  Uncreate(strikes_fault_projected), 
                  *self.Map(strike_labels_hanging, Unwrite), 
                  *self.Map(strike_labels_foot, Unwrite), 
                  *self.Map(strike_labels_fault, Unwrite))
        self.move_camera(theta = -45*DEGREES, phi = 60*DEGREES)
        self.wait(1)
        
        # # add 3D Strikes and the fault surface and move camera to side to show height differencies
        self.play(Create(strikes_hanging), Create(strikes_foot), Create(Surf))
        self.wait(2)
        self.move_camera(theta= 0, phi = 90*DEGREES)
        self.play(Create(sprung), Write(label_sprung))
        self.wait(1)
        self.play(Create(disp_vector))
        self.wait(1)
        self.play(strikes_hanging.animate.shift([0, -0.625/np.tan(np.radians(30)), -0.625]))
        self.play(Uncreate(sprung), Uncreate(label_sprung), Uncreate(disp_vector))
        self.wait(1)
        # self.move_camera(theta = -45*DEGREES, phi = 60*DEGREES)
        # start = strikes_hanging_trans[-1].get_center()
        # strike_slip = Arrow3D(start, start+[np.sqrt(0.125), 0, 0], thickness=0.02, height=0.05, base_radius=0.05).set_color(PURE_RED)
        # self.play(Create(strike_slip))
        # self.wait(1)
        # self.play(strikes_hanging_trans.animate.shift([np.sqrt(0.125), 0, 0]))
        # self.play(Uncreate(strike_slip))
        # self.wait(1)
        
        
        # move cam to 3D view, make lateral translation animation
        self.move_camera(theta = -45*DEGREES, phi = 60*DEGREES)
        self.wait(1)
        self.play(strikes_hanging.animate.shift([1, 0, 0]))
        self.play(strikes_hanging.animate.shift([-2, 0, 0]))
        self.play(strikes_hanging.animate.shift([1, 0, 0]))
        self.wait(1)
        
        
        
        
        