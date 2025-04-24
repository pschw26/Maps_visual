from manim import *
import numpy as np

class Folds(ThreeDScene):
    
    def intersection_lines(line1, line2):
        array_1 = np.array()
        
    def f(self, u, v):
        return np.array([u, v, np.sin(2*u)])
    
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
        resol = 36
        strikes = []
        
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
                    strike_ij = Line(start=self.g_i((j-3)/3*(np.sin(np.pi/8)), 6, i), 
                                     end=self.g_i((j-3)/3*(np.sin(np.pi/8)), -6, i))
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
            surf_i.set_color(RED)
            surf_i.set_style(fill_opacity = 0.5)
            self.add(surf_i)
            
        colors = [BLUE, GREEN, YELLOW, ORANGE, RED]
        
        for i,strike in enumerate(strikes):
            if i//5 == 0:
                strike.set_stroke(width=1)
            elif i//5 == 1:
                strike.set_stroke(width=2)
            elif i//5 == 2:
                strike.set_stroke(width=3)
            elif i//5 == 3:
                strike.set_stroke(width=4)
            elif i//5 == 4:
                strike.set_stroke(width=5)
            strike.set_color(colors[i%5])
            
        for i in range(2):
            strikes[3+i*10].shift([0, strikes[2].get_end()[1]-strikes[3+10*i].get_end()[1]+0.9, 0])
            strikes[6+i*10].shift([0, strikes[2].get_end()[1]-strikes[6+10*i].get_end()[1]+0.9, 0])
            # shift lower layer of strikes 
            strikes[8+i*10].shift([0, strikes[7].get_start()[1]-strikes[8+10*i].get_start()[1]-0.9, 0])
            strikes[11+i*10].shift([0, strikes[7].get_start()[1]-strikes[11+10*i].get_start()[1]-0.9, 0])
        strikes[1].shift([0, strikes[2].get_end()[1]-strikes[1].get_end()[1]-0.9, 0])
        strikes[23].shift([0, strikes[7].get_end()[1]-strikes[23].get_end()[1]+0.9, 0])
            
        
        # get strike intersection points
        for i in range(4):
            # shift upper layer of strikes
            p = self.get_intersection_point(strikes[3+i*5], strikes[6+i*5])
            q = self.get_intersection_point(strikes[4+i*5], strikes[5+i*5])
            # Schnittpunkt visualisieren
            # dot_p = Dot3D(p, color=RED)
            # dot_q = Dot3D(q, color=RED)
            if i%2 == 1:
                FA_i = Arrow3D(p, q, color=RED) 
            else:
                FA_i = Arrow3D(q, p, color=RED) 
            self.add(FA_i)    
        
        self.add(*strikes)
                

        surf_0 = Surface(
            lambda u, v: axes.c2p(*np.array([u, v, 1])),
            u_range=[-np.pi, np.pi],
            v_range=[-np.pi, np.pi],
            resolution= resol)
        surf_0.set_color(GRAY)
        surf_0.set_style(fill_opacity = 1)
        self.add(surf_0)

        Folds.rotate(rot_angle, axis=([1, 0, 0]))


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
        # self.add(outcrop_group.rotate(15*DEGREES, axis=[1, 0, 0]))
        
        
#         self.camera.frame_center= [0 ,0 , 1]
        self.set_camera_orientation(theta=0*DEGREES, phi=90*DEGREES, zoom=1)
        self.add(axes, x_label, y_label, z_label)
        # self.begin_ambient_camera_rotation(about='theta', rate=-0.75)
        # self.wait(2)
        # self.stop_ambient_camera_rotation()
        # self.move_camera(phi = 90*DEGREES, theta = 0)
        # self.wait(1)
        # self.move_camera(phi = 0, theta = 0)
          
        
        
        
        