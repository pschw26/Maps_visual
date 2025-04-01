from manim import *

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
            lambda u, v: axes.c2p(*np.array([u, v, 0.5*u])),
            u_range=[-2, 2],
            v_range=[-2, 2],
            resolution=(32, 32))
        surf_l1.set_color(BLUE)
        
        surf_l2 = Surface(
            lambda u, v: axes.c2p(*np.array([u, v, 0.5*u])),
            u_range=[-2, 0],
            v_range=[-2, 0],
            resolution=(32, 32))
        surf_l2.set_color(PURPLE).move_to([-1, 0, 0.5])
        
        surf0 = Surface(
            lambda u, v: axes.c2p(*np.array([u, v, 1])),
            u_range=[-2, 2],
            v_range=[-2, 2],
            resolution=(32, 32))
        surf0.set_color(GRAY)
        
        
        x_label = MathTex("x").move_to(axes.c2p(5, 0, 0) + RIGHT)
        y_label = MathTex("y").move_to(axes.c2p(0, 5, 0) + UP)
        z_label = MathTex("z").move_to(axes.c2p(0, 0, 5) + OUT)

        # Add everything to the scene
        self.add( x_label, y_label, z_label)
        
        self.add(axes, surf_l1, surf_l2, surf0)
        phi, theta, focal_distance, gamma, distance_to_origin = self.camera.get_value_trackers()
        # Set  init camera orientation
        self.set_camera_orientation(zoom=1, theta=90 * DEGREES, phi=90 * DEGREES)
