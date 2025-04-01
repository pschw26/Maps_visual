from manim import *
import numpy as np
import sys


class CreateTopo(ThreeDScene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # Initialize the parent class
        self.order = 5
        self.params = [np.random.rand()*0.5*(-1)**np.random.randint(2) for i in range(self.order)]
        self.res = 32
        
        
    def func(self, u, v):
        return np.array([
            u, 
            v, 
            (sum([self.params[i]*u**i for i in range(self.order//2)]) * sum([self.params[-i]*v**i for i in range(1, (self.order//2)+1)]))+0.5
        ])

    def construct(self):
        # Define 3D axes
        axes = ThreeDAxes(
            x_range=[-5, 5],
            y_range=[-5, 5],
            z_range=[-5, 5],  # Adjust z_range to fit your surface
            x_length=10,
            y_length=10,
            z_length=10,
        )

        # Define surface
        surface = Surface(
            lambda u, v: axes.c2p(*self.func(u, v)),
            u_range=[-2, 2],
            v_range=[-2, 2],
            resolution=(self.res, self.res),  # Higher resolution for smoother surface
        )
        
        surface2 = Surface(
            lambda u, v: axes.c2p(*np.array([u, v, 0.5*(u+v)])),
            u_range=[-2, 2],
            v_range=[-2, 2],
            resolution=(self.res, self.res),
            color=BLUE# Higher resolution for smoother surface
        )
        
        surface3 = Surface(
            lambda u, v: axes.c2p(*np.array([u, v, 0])),
            u_range=[-2, 2],
            v_range=[-2, 2],
            resolution=(int(self.res/2), int(self.res/2)),# Higher resolution for smoother surface
        )
        
        
        X, Y = np.meshgrid(np.linspace(-2, 2, self.res*3), np.linspace(-2, 2, self.res*3))
        prod = np.column_stack([X.ravel(), Y.ravel()])
        surf1 = np.array([(lambda u, v: axes.c2p(*np.array([u, v, self.func(u, v)[-1]])))(element[0], element[1])for element in prod])
        surf2 = np.array([(lambda u, v: axes.c2p(*np.array([u, v, 0.5*(u+v)])))(element[0], element[1])for element in prod])
        
        tolerance = 0.002  # Adjust as needed
        matches = np.all(np.isclose(surf1, surf2, atol=tolerance), axis=1)

        # Extract the intersection points
        outcrop_points = surf1[matches]
#         print(outcrop_points.shape)
        dots = VGroup(*[Dot3D(point=point, radius=0.01) for point in outcrop_points])
        outcrop = []
        for i in range(len(outcrop_points)-1):
            line = Line(start=outcrop_points[i], end=outcrop_points[i+1])
            line.set_color(BLUE)
            outcrop.append(line)

        coords = [(0.2, -1.0), (-0.6, 0.15), (-0.3, -0.8)]
        labels = ['B', 'A', 'C', 'B\prime', 'A\prime', 'C\prime']
        point_group1 = []
        point_group2 = []
        lines = []
        tex_labels = []
        rot_dir = OUT
        scale_label = 0.4
        
        for i in range(3):
            p = Dot3D(point=np.array([coords[i][0], coords[i][1], self.func(coords[i][0], coords[i][1])[-1]]),
                radius = 0.04,)
            label = (MathTex(labels[i]).scale(scale_label).next_to(p, UP))
            label.set_color(RED)
            label.rotate(PI/2, axis=RIGHT)
            label.rotate(-PI/4, axis=rot_dir)
            point_group1.append(p)
            tex_labels.append(label)
            p.set_color(RED)
            
            line = DashedVMobject(Line(start=p, end=np.array([coords[i][0], coords[i][1], 0.5*(coords[i][0]+coords[i][1])])), num_dashes=10)
            lines.append(line)
            
            p_prime = Dot3D(point=np.array([coords[i][0], coords[i][1], 0.5*(coords[i][0]+coords[i][1])]), radius=0.04)
            label = (MathTex(labels[i+3]).scale(scale_label).next_to(p_prime, DOWN))
            label.set_color(BLUE)
            label.rotate(PI/2, axis=RIGHT)
            label.rotate(-PI/4, axis=rot_dir)
            point_group2.append(p_prime)
            tex_labels.append(label)
            p_prime.set_color(BLUE)
        
        prime_labels = tex_labels[1::2]
        sandstone_1d = DashedVMobject(Line(ORIGIN-2*np.array([1, 0, 0.5]), ORIGIN+2*np.array([1, 0, 0.5])))
        AC = Line(start=point_group2[1], end=point_group2[2])
        P = Dot3D(point=np.array([coords[1][0], coords[1][1], 0.5*(coords[1][0]+coords[1][1])]), radius=0.04)
        P.set_color(RED)
        P_set_coords = AC.point_from_proportion(0.5)
        P_set = Dot3D(P_set_coords, radius=0.04)
        P_set.set_color(RED)
        BP = DashedVMobject(Line(start=point_group2[0] , end = P_set))
        P_coords = np.array([coords[1][0], coords[1][1], 0.5*(coords[1][0]+coords[1][1])])
        C_prime_coords = np.array([coords[2][0], coords[2][1], 0.5*(coords[2][0]+coords[2][1])])
        B_coords = np.array([coords[0][0], coords[0][1], 0.5*(coords[0][0]+coords[0][1])])
        
        # Apply the color function to the surface
        surface.set_style(fill_opacity = 1, stroke_color=GRAY)
#         surface2.set_style(fill_opacity = 0.8, stroke_color=PURPLE)
        surface3.set_style(fill_opacity = 0.8, stroke_color=WHITE)
        surface.set_fill(GRAY)
#         surface2.set_fill(PURPLE)
        surface3.set_fill(WHITE)
        
        # Add axes and surface to the scene
        x_label = MathTex("x").move_to(axes.c2p(4, 0, 0) + RIGHT)
        y_label = MathTex("y").move_to(axes.c2p(0, 4, 0) + UP)
        z_label = MathTex("z").move_to(axes.c2p(0, 0, 4) + OUT)

        # Add everything to the scene
        self.add(axes, x_label, y_label, z_label)
        self.add(axes)
        
        
        # for cam rotation: 45° correspond to 0.75 rate for 1 s
        
        # Animation routine 
#         phi, theta, focal_distance, gamma, distance_to_origin = self.camera.get_value_trackers()
#         # Set  init camera orientation
#         self.set_camera_orientation(distance=0, theta=0 * DEGREES, phi=60 * DEGREES)
#         # implement topography
#         self.play(Create(surface))
#         self.wait()
#         self.begin_ambient_camera_rotation(rate=-1.5, about='theta')
#         self.wait(1.5)
#         self.stop_ambient_camera_rotation()
#         self.move_camera(zoom=3)
#         # show points on topography 
#         self.play(Create(VGroup(*point_group1)))
#         self.play(Write(VGroup(*tex_labels[0::2])))
#         self.wait()
#         self.move_camera(zoom=1)
#         # show sealevel surface
#         self.play(Create(surface3))
#         self.wait()
#         # show underground
#         self.move_camera(phi=90*DEGREES)
#         self.move_camera(zoom=2)
#         self.wait()
#         # show boreholes
#         self.play(Create(VGroup(*lines)))
#         self.wait()
#         # show points on sandstone layer
#         self.play(Create(VGroup(*point_group2)))
#         self.play(Write(*prime_labels))
#         self.wait()
#         self.begin_ambient_camera_rotation(rate=1.5, about=theta)
#         self.wait(0.75)
#         [label.rotate(PI/4, axis=OUT)for label in prime_labels]
#         self.stop_ambient_camera_rotation()
#         self.play(Create(sandstone_1d))
#         self.remove(sandstone_1d)
        
        # show connection line of three points 
#         self.set_camera_orientation(zoom=2, theta=-45*DEGREES, phi=90*DEGREES)
#         self.add(*point_group2)
#         self.add(*prime_labels)
#         self.add(DashedVMobject(Line(ORIGIN-2*np.array([1, 0, 0.5]), ORIGIN+2*np.array([1, 0, 0.5]))))
#         [label.rotate(PI/2, axis=OUT)for label in prime_labels]
        
        
        self.set_camera_orientation(zoom=2.5, theta=-45*DEGREES, phi=45*DEGREES)
        self.add(*point_group2)
        self.add(*prime_labels)
        [label.rotate(-PI/2, axis=RIGHT)for label in prime_labels]
        self.add(AC)
        self.begin_ambient_camera_rotation(rate=-1.5)
        self.wait(1)
        self.stop_ambient_camera_rotation()
        self.play(P.animate.shift(C_prime_coords - P_coords))
        self.remove(P)
        self.wait(2)
        self.play(Create(P_set))
        self.wait(2)
        self.play(Create(DashedVMobject(Line(B_coords-2*(P_set_coords - B_coords), B_coords+2*(P_set_coords - B_coords)))))
        
        
#         # show sandstone layer       
#         self.play(Create(surface2))
#         self.begin_ambient_camera_rotation(rate=0.75, about='theta')
#         self.wait(3)
#         self.stop_ambient_camera_rotation()
#         self.move_camera(phi=30*DEGREES)
#         # show outcrop
#         self.play(Create(VGroup(*outcrop)))
#         self.wait()
#         self.move_camera(zoom=1)
#         self.wait()

    






