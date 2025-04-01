from manim import *
import numpy as np

class Folds(ThreeDScene):
    
    @staticmethod
    def cartesian_prod(x, y, res):
        X, Y = np.meshgrid(np.linspace(-x, x, res), np.linspace(-y, y, res))
        return np.column_stack((X.ravel(), Y.ravel()))
        
    def f(self, u, v):
        return np.array([u, v, np.sin(2*u)])
    
    def g_i(self, u, v, i):
        return np.array([u, v, (-1)**i*1/(np.sin(np.pi/8))*u])
    
    
    def construct(self):
        # params 
        rot_angle  = 20*DEGREES
        resol = 36
        
        axes = ThreeDAxes(x_range=[-np.pi, np.pi], x_length=2*np.pi)
        Folds = Surface(
            lambda u, v: axes.c2p(*self.f(u, v)),
            u_range = [-np.pi, np.pi],
            v_range = [-3.5, 3.5],
            resolution = resol).set_style(fill_opacity = 1).set_color(BLUE)
                    
        for i in range(5):
            surf_i = Surface(
                lambda u, v: axes.c2p(*self.g_i(u, v, i)),
                u_range = [-1, 1],
                v_range = [-np.pi, np.pi],
                resolution = resol
                )
#             surf_i.rotate(rot_angle, axis=([1, 0, (-1)**i*np.tan(1/(np.sin(np.pi/8)))]))
            for j in range(6):
                # create strikelines on surface 
                strike_ij = Line(start=self.g_i((j-3)/3*(np.sin(np.pi/8)), 3.5, i), end=self.g_i((j-3)/3*(np.sin(np.pi/8)), -3.5, i))
                # shift line with surface 
                strike_ij.shift((strike_ij.get_center() + [-np.pi + i*np.pi/2, 0, 0]))
                # rotate strikeline on surface
                strike_ij.rotate((-1)**i*rot_angle, axis=[(-1)**i/(np.sin(np.pi/8)), 0, 1])
                # rotate strikeline to be horizontal
                strike_ij.rotate(-1*rot_angle, axis=[1, 0, 0])
#                 self.add(strike_ij)
            surf_i.move_to(([-np.pi + i*np.pi/2, 0, 0]))
            surf_i.rotate(rot_angle, axis=([1, 0, 0]))
#             print(np.tan(1/(np.sin(np.pi/8))))
            surf_i.set_color(RED)
            surf_i.set_style(fill_opacity = 0.5)
#             self.add(surf_i)
            
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
#         
#         for i in range(2):
#             self.add(Line(start=strikes[i], end=strikes[i+1]))
#             self.add(Line(start=strikes[i+3], end=strikes[i+4]))

        surf_0 = Surface(
            lambda u, v: axes.c2p(*np.array([u, v, 1])),
            u_range=[-np.pi, np.pi],
            v_range=[-np.pi, np.pi],
            resolution= resol)
        surf_0.set_color(GRAY)
        surf_0.set_style(fill_opacity = 1)
        self.add(surf_0)
        #             line_0.rotate(20*DEGREES, axis=([1, 0, 0]))
#             for n in range(3):
#                 if i == 0:
#                     x = -np.pi + i*np.pi/2 + np.pi/16 + n*np.pi/16
#                 else:
#                     x = -np.pi + i*np.pi/2 - np.pi/16 + n*np.pi/16
#                 line_1 = Line(start=([x, -np.pi, np.sin(2*x)]), end=([x, np.pi, np.sin(2*x)]))
# #                 line_1.rotate(20*DEGREES, axis=([1, 0, 0]))
#                 self.add(line_1)

#         line = Line(start=([-np.pi, -np.pi, 0]), end=([-np.pi, np.pi, 0]))
#         line.rotate(20*DEGREES, axis=([1, 0, 0]))
#         self.add(line)
#         
        Folds.rotate(rot_angle, axis=([1, 0, 0]))
#         
        x_label = MathTex("x").move_to(axes.c2p(3.2, 0, 0) + RIGHT)
        y_label = MathTex("y").move_to(axes.c2p(0, 3.2, 0) + UP)
        z_label = MathTex("z").move_to(axes.c2p(0, 0, 3.2) + OUT)
        
        # get_outcrop line:
        
        X, Y = np.meshgrid(np.linspace(-np.pi, np.pi, resol*6), np.linspace(-np.pi, np.pi, resol*6))
        prod = np.column_stack([X.ravel(), Y.ravel()])
        surf1 = np.array([(lambda u, v: axes.c2p(*np.array([u, v, v*np.sin(-rot_angle)+1])))(element[0], element[1])for element in prod])
        surf2 = np.array([(lambda u, v: axes.c2p(*np.array([u, v, self.f(u, v)[-1]])))(element[0], element[1])for element in prod])
        
        tolerance = 0.002  # Adjust as needed
        matches = np.all(np.isclose(surf1, surf2, atol=tolerance), axis=1)

        
        # Extract the intersection points
        outcrop_points = surf2[matches]
#         print(outcrop_points[:5])
        outcrop_points_sorted=  outcrop_points[np.argsort(outcrop_points[:,0])]
#         print(outcrop_points_sorted[:5])
        dots = VGroup(*[Dot3D(point=point, radius=0.01) for point in outcrop_points_sorted])
#         self.add(*dots)
        outcrop = []
        for i in range(len(outcrop_points_sorted)-1):
            if abs(outcrop_points_sorted[i+1][0] - outcrop_points_sorted[i][0]) < 1:
                line = Line(start=outcrop_points_sorted[i], end=outcrop_points_sorted[i+1])
                line.set_color(BLUE)
    #             self.add(line)
                outcrop.append(line.move_to(line.get_center() + [0, 0, 0.45]))
        outcrop_group = VGroup(outcrop)
        self.add(outcrop_group.rotate(15*DEGREES, axis=[1, 0, 0]))
        # test surfaces:
        
#         s1 = Surface(
#             lambda u, v: axes.c2p(*np.array([u, v, v*np.sin(-rot_angle)+1])),
#             u_range=[-np.pi, np.pi],
#             v_range=[-np.pi, np.pi],
#             resolution=resol).set_color(GRAY)
#         self.add(s1)
#         
#         s2 = Surface(
#             lambda u, v: axes.c2p(*np.array([u, v, self.f(u, v)[-1]])),
#             u_range=[-np.pi, np.pi],
#             v_range=[-np.pi, np.pi],
#             resolution=resol).set_color(BLUE)
#         self.add(s2)
        
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
        
        
#         self.camera.frame_center= [0 ,0 , 1]
        self.set_camera_orientation(theta=0*DEGREES, phi=0*DEGREES, zoom=1)
        self.add(axes,x_label, y_label, z_label, Folds)
#         self.begin_ambient_camera_rotation(about='theta', rate=-0.75)
#         self.wait(2)
#         self.stop_ambient_camera_rotation()
#         self.wait(1)
#          
        
        
        
        