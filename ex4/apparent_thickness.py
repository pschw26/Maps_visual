from manim import *
from manim.utils.color import rgb_to_color

''' Interpreter path for manim environment: C:/Users/pschw/AppData/Local/Programs/Python/Python310/python.exe '''

class app_dip(ThreeDScene):
    
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
        
        strike = Line(start= [-2, 2, 0], end= [2, -2, 0])
        dip = Line(start= [-1, -1, 0], end=ORIGIN)
        label = MathTex('45').move_to([-1.5, -0.5, 0]).rotate(PI/2, OUT).scale(1.5)
        
        
        surf_l1 = Surface(
            lambda u, v: axes.c2p(*np.array([u, v, u])),
            u_range=[-2, 2],
            v_range=[-2, 2],
            resolution=(32, 32))
        surf_l1.set_color(BLUE)
        
        surf_l2 = Surface(
            lambda u, v: axes.c2p(*np.array([u, v, u])),
            u_range=[-2, 2],
            v_range=[-2, 2],
            resolution=(32, 32))
        surf_l2.set_color(PURPLE).move_to([-np.sqrt(2), 0, 0])
        
        surf_cross1 = Surface(
            lambda u, v: axes.c2p(*np.array([u, 0, v])),
            u_range=[-2, 2],
            v_range=[-2, 2],
            resolution=(32, 32))
        surf_cross1.set_color(WHITE).set_opacity(0.5)
        
        # create copy of true dip section AB
        surf_cross2 = surf_cross1.copy()
        
        t = ValueTracker(0)
        # always redrawn surface with conditional coloring RED -> ORANGE
        surf_cross2.add_updater(lambda m: m.set_color(
        rgb_to_color((255, 
                      255*np.cos(np.radians(t.get_value())), 
                      255*np.cos(np.radians(t.get_value()))))))
        self.add(t)
        t.add_updater(lambda mobject, dt: mobject.increment_value(dt))
    
        
        # cross sections
        AB_section_coords = [np.array([2, 0, 2]), np.array([2-np.sqrt(2), 0, 2]), np.array([-2, 0, -2+np.sqrt(2)]), np.array([-2, 0, -2])]
        CD_section_coords = [np.array([2, 0, 2]), np.array([2-np.sqrt(2), -np.sqrt(2), 2]), np.array([0, -2, np.sqrt(2)]), np.array([0, -2, 0])]
        
        lines_section_AB = []
        lines_section_CD = []
        
        for i in range(3):
            line = Line(start = AB_section_coords[i], end = AB_section_coords[i+1]).set_color(WHITE)
            lines_section_AB.append(line)
            line = Line(start = CD_section_coords[i], end = CD_section_coords[i+1])
            lines_section_CD.append(line)
        lines_section_AB.append(Line(start = AB_section_coords[-1], end = AB_section_coords[0]).set_color(WHITE))
        lines_section_CD.append(Line(start = CD_section_coords[-1], end = CD_section_coords[0]))
        
        
        section_AB = VGroup(*lines_section_AB)
        
        # rotation of the section CD parallel to AB
        section_CD = VGroup(*lines_section_CD)

        # # Erste Rotation: Orientierung in XY-Ebene anpassen
        # section_CD.rotate(-PI/4, axis=[0, 0, 1], about_point=[2, 0, 0])
        
        # rotation of the section parallel to dip of AB
        apparent_dip_deg = 45
        true_dip_deg = np.degrees(np.arctan(1 / np.sqrt(2) * np.tan(np.radians(apparent_dip_deg))))
        dip_diff = -(apparent_dip_deg - true_dip_deg) * DEGREES
        
        # # Rotation to make it parallel to section AB
        # section_CD.rotate(dip_diff, axis=[0, 1, 0], about_point=[2, 0, 2])
            
        # self.add(*lines_section_AB, section_CD)
        
        x_label = MathTex("x").move_to(axes.c2p(5, 0, 0) + RIGHT)
        y_label = MathTex("y").move_to(axes.c2p(0, 5, 0) + UP)
        z_label = MathTex("z").move_to(axes.c2p(0, 0, 5) + OUT)

        # Add everything to the scene
        surfaces = VGroup([surf_l1, surf_l2, surf_cross1, surf_cross2])#.rotate(np.degrees(np.arctan(0.5))*DEGREES, axis=([0,1,0]))
        
        # self.add(*lines_section_AB, *lines_section_CD)
        # self.add( x_label, y_label, z_label)
        # self.add(axes, surfaces)
        
        phi, theta, focal_distance, gamma, distance_to_origin = self.camera.get_value_trackers()
        # Set  init camera orientation
        
        self.add(axes, x_label, y_label, z_label)
        self.set_camera_orientation(zoom=1, theta=0* DEGREES, phi=60 * DEGREES)
        
        
        # create surfaces while rotating
        self.begin_ambient_camera_rotation(rate = 0.75, about='theta')
        self.wait(2)
        self.play(Create(surf_l1), Create(surf_l2))
        self.wait(1)
        self.stop_ambient_camera_rotation()
        
        
        # create and rotate cross section planes
        self.play(Create(surf_cross1), Create(surf_cross2))
        self.wait(1)
        self.play(
        t.animate.set_value(50),
        Rotate(surf_cross2, angle=PI/4, axis=([0, 0, 1]), about_point=([2, 0, 0]), run_time=5),
        run_time=5)
        
        
        # create cross sections 
        section_CD.set_color(surf_cross2.get_color())
        self.play(Create(section_AB), Create(section_CD))
        self.move_camera(theta=270*DEGREES, run_time=3)
        self.play(Uncreate(surfaces), 
                  Rotate(section_CD, angle=-PI/4, axis=[0, 0, 1], about_point=[2, 0, 0]), 
                  run_time=2)
        self.move_camera(phi = 90 * DEGREES, zoom=1.5)
        self.wait(1)
        self.play(Rotate(section_CD, angle= dip_diff, axis=[0, 1, 0], about_point=[2, 0, 2]),
                  run_time=2)
        self.wait(2)
        
        
        


        
