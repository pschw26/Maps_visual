from manim import *
from manim.utils.color.core import ManimColor
import numpy as np
import matplotlib.cm as cm


class Folds(ThreeDScene):
    
    def intersection_lines(line1, line2):
        array_1 = np.array()
        
    def f(self, u, v):
        return np.array([u, v, np.sin(2*u)])
    
    def h(self, u, v, i):
        return np.array([3*np.pi/4-i*np.pi/2, u, v])
    
    def g_i(self, u, v, i):
        return np.array([u, v, (-1)**i*1/(np.sin(np.pi/8))*u])
    
    def get_intersection_point(self, line1, line2):
        """
        Berechnet den Schnittpunkt zweier 2D-Linien
        """
        # Hole Start- und Endpunkte
        p1, p2 = line1.get_start()[:2], line1.get_end()[:2]
        p3, p4 = line2.get_start()[:2], line2.get_end()[:2]

        # Rechne den Schnittpunkt aus (2D)
        denom = (p1[0] - p2[0]) * (p3[1] - p4[1]) - (p1[1] - p2[1]) * (p3[0] - p4[0])
        if denom == 0:
            raise ValueError("Linien sind parallel – kein Schnittpunkt!")

        # Formel für den Schnittpunkt zweier Geraden
        x_num = (p1[0]*p2[1] - p1[1]*p2[0]) * (p3[0] - p4[0]) - (p1[0] - p2[0]) * (p3[0]*p4[1] - p3[1]*p4[0])
        y_num = (p1[0]*p2[1] - p1[1]*p2[0]) * (p3[1] - p4[1]) - (p1[1] - p2[1]) * (p3[0]*p4[1] - p3[1]*p4[0])
        x = x_num / denom
        y = y_num / denom

        return np.array([x, y, line1.get_center()[2]])  # Manim erwartet 3D-Vectoren   
    
    
    def construct(self):
        # params 
        rot_angle  = 20*DEGREES
        resol = 64
        strikes = []
        limb_planes = []
        FA_planes = []
        intersect_points = []
        fold_axes = []
        
        axes = ThreeDAxes(
                x_range=[-5, 5],
                y_range=[-5, 5],
                z_range=[-5, 5],
                x_length=10,
                y_length=10,
                z_length=10,
            )
        Folds = Surface(
            lambda u, v: axes.c2p(*self.f(u, v)),
            u_range = [-np.pi, np.pi],
            v_range = [-3.5, 3.5],
            resolution = resol).set_style(fill_opacity = 1).set_color(BLUE)
        
        for i in range(5):
            if i != 2:
                FAP = Surface(
                    lambda u, v: axes.c2p(*self.h(u, v, i)),
                    u_range = [-3.5, 3.5],
                    v_range = [-3.5, 3.5],
                    resolution = resol).set_style(fill_opacity = 0.5).set_color(RED)
                FA_planes.append(FAP)
                        
        for i in range(5):
            surf_i = Surface(
                lambda u, v: axes.c2p(*self.g_i(u, v, i)),
                u_range = [-1, 1],
                v_range = [-np.pi, np.pi],
                resolution = resol
                )
#             surf_i.rotate(rot_angle, axis=([1, 0, (-1)**i*np.tan(1/(np.sin(np.pi/8)))]))
            for j in range(1,6):
                # create strikelines on surface # TODO!!
                if (j==4):
                    if i%2 == 1:
                        strike_ij = Line(start=self.g_i((j-3)/3*(np.sin(np.pi/8)), 6, i), 
                                     end=self.g_i((j-3)/3*(np.sin(np.pi/8)), -3.5, i))
                    else:
                        strike_ij = Line(start=self.g_i((j-3)/3*(np.sin(np.pi/8)), 3.5, i), 
                                         end=self.g_i((j-3)/3*(np.sin(np.pi/8)), -6, i))
                elif (j==2):
                    if i%2 == 1:
                        strike_ij = Line(start=self.g_i((j-3)/3*(np.sin(np.pi/8)), 3.5, i), 
                                         end=self.g_i((j-3)/3*(np.sin(np.pi/8)), -6, i))
                    else:
                        strike_ij = Line(start=self.g_i((j-3)/3*(np.sin(np.pi/8)), 6, i), 
                                     end=self.g_i((j-3)/3*(np.sin(np.pi/8)), -3.5, i))
                elif (j==3):
                    strike_ij = Line(start=self.g_i((j-3)/3*(np.sin(np.pi/8)), 7, i), 
                                     end=self.g_i((j-3)/3*(np.sin(np.pi/8)), -7, i))
                else:
                    strike_ij = Line(start=self.g_i((j-3)/3*(np.sin(np.pi/8)), 3.5, i), 
                                     end=self.g_i((j-3)/3*(np.sin(np.pi/8)), -3.5, i))
                # shift line with surface 
                strike_ij.shift((strike_ij.get_center() + [-np.pi + i*np.pi/2, 0, 0]))
                # rotate strikeline on surface
                strike_ij.rotate((-1)**i*rot_angle, axis=[(-1)**i/(np.sin(np.pi/8)), 0, 1])
                # rotate strikeline to be horizontal
                strike_ij.rotate(-1*18.95*DEGREES, axis=[1, 0, 0])
                strikes.append(strike_ij)
                
            surf_i.move_to(([-np.pi + i*np.pi/2, 0, 0]))
            surf_i.rotate(rot_angle, axis=([1, 0, 0]))
#             print(np.tan(1/(np.sin(np.pi/8))))
            surf_i.set_color(PURPLE)
            surf_i.set_style(fill_opacity = 0.5)
            limb_planes.append(surf_i)
            # self.add(surf_i)
            
        # give strikes a viridis color based on z coordinate 
        norm = lambda z: (z - min(z_values)) / (max(z_values) - min(z_values))  # in [0, 1]
        colormap = cm.get_cmap("viridis")
                
        z_values = list(map(lambda x: x.get_center()[2], strikes))
        for i,z in enumerate(z_values):
            # Farbe aus Colormap holen (als RGB)
            rgba = colormap(norm(z))
            rgb = (float(rgba[0]), float(rgba[1]), float(rgba[2]), 1.0)
            color = ManimColor.from_rgb(rgb)  
            strikes[i].set_color(color)
            
            
            
            
        shift_val = 2.2  
    
        for i in range(2):
            strikes[3+i*10].shift([0, strikes[2].get_end()[1]-strikes[3+10*i].get_end()[1]+shift_val, 0])
            strikes[6+i*10].shift([0, strikes[2].get_end()[1]-strikes[6+10*i].get_end()[1]+shift_val, 0])
            # shift lower layer of strikes 
            strikes[8+i*10].shift([0, strikes[7].get_start()[1]-strikes[8+10*i].get_start()[1]-shift_val, 0])
            strikes[11+i*10].shift([0, strikes[7].get_start()[1]-strikes[11+10*i].get_start()[1]-shift_val, 0])
        strikes[1].shift([0, strikes[2].get_end()[1]-strikes[1].get_end()[1]+shift_val, 0])
        strikes[23].shift([0, strikes[7].get_end()[1]-strikes[23].get_end()[1]+shift_val, 0])
            
        
        # get strike intersection points
        for i in range(4):
            # shift upper layer of strikes
            p = self.get_intersection_point(strikes[3+i*5], strikes[6+i*5])
            q = self.get_intersection_point(strikes[4+i*5], strikes[5+i*5])
            r = self.get_intersection_point(strikes[2+i*5], strikes[2+(i+1)*5])
            # Schnittpunkt visualisieren)
            dot_p = Dot3D(p, color=RED, radius=0.05)
            dot_q = Dot3D(q, color=RED, radius=0.05)
            dot_r = Dot3D(r, color=RED, radius=0.05)
            intersect_points.extend([dot_p, dot_q, dot_r])
            if i%2 == 1:
                FA_i = Arrow3D(p, q, color=RED) 
                FA_j = Arrow3D(r, p, color=RED)
            else:
                FA_i = Arrow3D(q, p, color=RED) 
                FA_j = Arrow3D(p, r, color=RED) 
            fold_axes.extend([FA_i, FA_j])
            # self.add(FA_i, FA_j)    
        
        # self.add(*strikes)
                

        surf_0 = Surface(
            lambda u, v: axes.c2p(*np.array([u, v, 1])),
            u_range=[-np.pi, np.pi],
            v_range=[-np.pi, np.pi],
            resolution= resol)
        surf_0.set_color(GRAY)
        surf_0.set_style(fill_opacity = 1)
        # self.add(surf_0)

        Folds.rotate(rot_angle, axis=([1, 0, 0]))


        x_label = MathTex("x").move_to(axes.c2p(5, 0, 0) + RIGHT)
        y_label = MathTex("y").move_to(axes.c2p(0, 5, 0) + UP)
        z_label = MathTex("z").move_to(axes.c2p(0, 0, 5) + OUT)
        
        # get_outcrop line:
#         X, Y = np.meshgrid(np.linspace(-np.pi, np.pi, resol*6), np.linspace(-np.pi, np.pi, resol*6))
#         prod = np.column_stack([X.ravel(), Y.ravel()])
#         surf1 = np.array([(lambda u, v: axes.c2p(*np.array([u, v, v*np.sin(-rot_angle)+1])))(element[0], element[1])for element in prod])
#         surf2 = np.array([(lambda u, v: axes.c2p(*np.array([u, v, self.f(u, v)[-1]])))(element[0], element[1])for element in prod])
        
#         tolerance = 0.002  # Adjust as needed
#         matches = np.all(np.isclose(surf1, surf2, atol=tolerance), axis=1)

        
#         # Extract the intersection points
#         outcrop_points = surf2[matches]
# #         print(outcrop_points[:5])
#         outcrop_points_sorted=  outcrop_points[np.argsort(outcrop_points[:,0])]
# #         print(outcrop_points_sorted[:5])
#         dots = VGroup(*[Dot3D(point=point, radius=0.01) for point in outcrop_points_sorted])
# #         self.add(*dots)
#         outcrop = []
#         for i in range(len(outcrop_points_sorted)-1):
#             if abs(outcrop_points_sorted[i+1][0] - outcrop_points_sorted[i][0]) < 1:
#                 line = Line(start=outcrop_points_sorted[i], end=outcrop_points_sorted[i+1])
#                 line.set_color(BLUE)
#     #             self.add(line)
#                 outcrop.append(line.move_to(line.get_center() + [0, 0, 0.45]))
#         outcrop_group = VGroup(outcrop)
        # self.add(outcrop_group.rotate(15*DEGREES, axis=[1, 0, 0]))
        
        
#         self.camera.frame_center= [0 ,0 , 1]
        # self.set_camera_orientation(theta=0*DEGREES, phi=0*DEGREES, zoom=1)
        # self.add(axes, x_label, y_label, z_label, *intersect_points, *strikes)
        # self.begin_ambient_camera_rotation(about='theta', rate=-0.75)
        # self.wait(4)
        # self.stop_ambient_camera_rotation()
        # self.move_camera(phi = 90*DEGREES, theta = 0)
        # self.wait(1)
        # self.move_camera(phi = 0, theta = 0)
         
        # problem intro; show folds and surface 
        self.add(axes, x_label, y_label, z_label)
        self.set_camera_orientation(theta=0*DEGREES, phi=60*DEGREES, zoom=1)
        self.begin_ambient_camera_rotation(about='theta', rate=0.75)
        self.wait(1)
        self.play(Create(Folds))
        self.wait(1)
        self.play(Create(surf_0))
        self.wait(2)

        
        # create fold limb plaes and add strikes on them
        self.play(*[Create(s) for s in strikes], run_time=3)
        self.move_camera(phi=90*DEGREES)
        self.wait(4)
        self.stop_ambient_camera_rotation()
        
        # add intersection points and construct FA's show limb planes
        self.play(*[Create(p) for p in intersect_points])
        self.wait(1)
        self.move_camera(phi=60*DEGREES, zoom=1.5)
        self.play(Uncreate(surf_0))
        self.play(*[Create(p) for p in limb_planes])
        self.begin_ambient_camera_rotation(about='theta', rate=0.75)
        self.wait(4)
        self.stop_ambient_camera_rotation()
        self.play(*[Uncreate(p) for p in limb_planes])
        self.wait(1)

        
        
        self.begin_ambient_camera_rotation(about='theta', rate= 0.75)
        self.wait(1)
        self.play(Uncreate(Folds))
        self.wait(1)
        self.play(*[Create(p) for p in fold_axes[::2]], run_time=5)
        self.wait(2)
        self.stop_ambient_camera_rotation()
        self.move_camera(phi=0, theta=0, zoom=0.75)
        self.wait(2)
        self.play(*[Create(p) for p in fold_axes[1::2]], run_time=3)
        self.wait(1)
        self.move_camera(phi=60*DEGREES, theta=45*DEGREES, zoom=1)
        self.play(*[Create(p) for p in FA_planes])
        self.begin_ambient_camera_rotation(about='theta', rate= 0.75)
        self.wait(1)
        self.play(Create(Folds), Create(surf_0))
        self.wait(3)
        self.stop_ambient_camera_rotation()
        self.move_camera(phi=0, theta=0, zoom=0.75)
        self.wait(2)
        
                
        
        
        
        
        
        