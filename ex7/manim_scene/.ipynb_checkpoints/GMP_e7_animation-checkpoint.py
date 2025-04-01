from manim import *
import numpy as np

class Folds(ThreeDScene):
    
    @staticmethod
    def cartesian_prod(x, y, res):
        X, Y = np.meshgrid(np.linspace(-x, x, res), np.linspace(-y, y, res))
        return np.column_stack((X.ravel(), Y.ravel()))
        
    def f(self, u, v):
        return np.array([u, v, np.sin(2*u)])
    
    
    def construct(self):
        axes = ThreeDAxes(x_range=[-np.pi, np.pi], x_length=8)
        Folds = Surface(
            lambda u, v: axes.c2p(*self.f(u, v)),
            u_range = [-np.pi, np.pi],
            v_range = [-np.pi, np.pi],
            resolution = 32)
        
#         lines = []
#         for i in range(3):
#             
#             line = (Line(start=([-np.pi + i*3*np.pi/4, -np.pi, 0]), end=([-np.pi + i*3*np.pi/4, np.pi, 0])))
#             self.add(line)
#             line.rotate(20*DEGREES, axis=([1, 0, 0]))
#             for n in range(3)
        line = Line(start=([-np.pi, -np.pi, 0]), end=([-np.pi, np.pi, 0]))
        line.rotate(20*DEGREES, axis=([1, 0, 0]))
        self.add(line)
        
        Folds.rotate(20*DEGREES, axis=([1, 0, 0]))
        
        x_label = MathTex("x").move_to(axes.c2p(4, 0, 0) + RIGHT)
        y_label = MathTex("y").move_to(axes.c2p(0, 4, 0) + UP)
        z_label = MathTex("z").move_to(axes.c2p(0, 0, 4) + OUT)
        

        
#         cross_section = Surface(
#             lambda u, v: axes.c2p(*np.array([u, 2, v])),
#             u_range= [-3, 3],
#             v_range = [-3, 3],
#             resolution=32)
#         cross_section.set_style(fill_opacity=0.5)
#         
#         fold_section = ParametricFunction(
#             lambda t: axes.c2p(*np.array([t, 2, np.sin(2*t)+(2*np.tan(20*DEGREES))])),
#             t_range= [-3, 3])
#         fold_section.set_color(RED)
        
        
        
        self.set_camera_orientation(theta=90*DEGREES, phi=45*DEGREES)
        self.add(axes, Folds)
        
        
        
        