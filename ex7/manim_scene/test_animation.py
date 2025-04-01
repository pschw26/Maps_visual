from manim import *
import numpy as np

class OVScene(ThreeDScene):
    
    @staticmethod
    def cartesian_prod(x, y, res):
        X, Y = np.meshgrid(np.linspace(-x, x, res), np.linspace(-y, y, res))
        return np.column_stack((X.ravel(), Y.ravel()))
        
    def f(self, u, v):
        return np.array([u, v, np.sin(2*u)])
    
    def g_i(self, u, v, i):
        return np.array([u, v, (-1)**i*1/(np.sin(np.pi/8))*u])
    
    
    def construct(self):
        
        rot_angle = 20*DEGREES
        
        axes = ThreeDAxes(x_range=[-np.pi, np.pi], x_length=2*np.pi)
        Folds = Surface(
            lambda u, v: axes.c2p(*self.f(u, v)),
            u_range = [-np.pi, np.pi],
            v_range = [-3.5, 3.5],
            resolution = 32)
                    
        for i in range(5):
            surf_i = Surface(
                lambda u, v: axes.c2p(*self.g_i(u, v, i)),
                u_range = [-1, 1],
                v_range = [-np.pi, np.pi],
                resolution = 32
                )
#             for j in range(5):
#                 # create strikelines on surface 
#                 strike_ij = Line(start=self.g_i((j-3)/3*(np.sin(np.pi/8)), 3.5, i), end=self.g_i((j-3)/3*(np.sin(np.pi/8)), -3.5, i))
#                 # shift line with surface 
#                 strike_ij.shift((strike_ij.get_center() + [-np.pi + i*np.pi/2, 0, 0]))
#                 # rotate strikeline on surface
#                 strike_ij.rotate((-1)**i*rot_angle, axis=[(-1)**i/(np.sin(np.pi/8)), 0, 1])
#                 # rotate strikeline to be horizontal
#                 strike_ij.rotate(-1*rot_angle, axis=[1, 0, 0])
#                 self.add(strike_ij)
            surf_i.move_to(([-np.pi + i*np.pi/2, 0, 0]))
#             surf_i.rotate(rot_angle, axis=([1, 0, 0]))
            surf_i.set_color(RED)
            surf_i.set_style(fill_opacity = 0.5)
            self.add(surf_i)

            

#         for i in range(4):
#             strikes.append(Dot3D(([-np.pi + i*np.pi/2, np.pi, 1]), radius=0.05))
#             self.add(Dot3D(([-np.pi + i*np.pi/2, np.pi, 1]), radius=0.05))
#             if i < 2:
#                 strikes.append(Dot3D(([-np.pi + (4*i+1)*np.pi/4, np.pi + 2*((-1)*(np.sqrt(np.pi**2 - (np.sin(rot_angle)*np.pi)**2))), 1]), radius= 0.05))
#                 self.add(Dot3D(([-np.pi + (4*i+1)*np.pi/4, np.pi + 2*((-1)*(np.sqrt(np.pi**2 - (np.sin(rot_angle)*np.pi)**2))), 1]), radius= 0.05))
#         self.add(Line(start=strikes[0], end=strikes[1]))
#         self.add(Line(start=strikes[1], end=strikes[2]))
#         self.add(Line(start=strikes[3], end=strikes[4]))
#         self.add(Line(start=strikes[3], end=strikes[5]))
        
        surf_0 = Surface(
            lambda u, v: axes.c2p(*np.array([u, v, (u+v)*np.sin(-rot_angle)+1])),
            u_range=[-np.pi, np.pi],
            v_range=[-np.pi, np.pi],
            resolution= 32).set_color(GRAY).set_style(fill_opacity = 1)
        self.add(surf_0)
#         
#         
        x_label = MathTex("x").move_to(axes.c2p(3.2, 0, 0) + RIGHT)
        y_label = MathTex("y").move_to(axes.c2p(0, 3.2, 0) + UP)
        z_label = MathTex("z").move_to(axes.c2p(0, 0, 3.2) + OUT)
  
        
        phi, theta, focal_distance, gamma, distance_to_origin = self.camera.get_value_trackers()
        self.set_camera_orientation(theta=45*DEGREES, phi=60*DEGREES, zoom=1)
        self.add(axes,x_label, y_label, z_label)
#         self.begin_ambient_camera_rotation(about='theta', rate=0.75)
#         self.wait(4)
#         self.stop_ambient_camera_rotation()
#         self.wait(1)
#         
        
        

