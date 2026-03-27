from manim import *
import numpy as np
import mpmath

class ExtendedBeyondViewportRiemannZetaPlot(Scene):
    def construct(self):
        # Title
        title = Text("Riemann Zeta Function", font_size=36, color=YELLOW).to_edge(UP, buff=0.5)
        self.play(Write(title))
        
        # Complex plane with a visible range for the viewport
        # We keep the visible range smaller, but calculate beyond this range
        visible_complex_plane = NumberPlane(
            x_range=[-10, 10, 1],
            y_range=[-10, 10, 1],
            background_line_style={"stroke_color": BLUE_D, "stroke_opacity": 0.5}
        )
        visible_complex_plane.add_coordinates()  # Adds integer labels to major points
        self.play(Create(visible_complex_plane))
        
        # Equation for the Riemann Zeta function
        zeta_equation = MathTex(r"\zeta(s) = \sum_{n=1}^{\infty} \frac{1}{n^s}")
        zeta_equation.to_edge(LEFT, buff=0.5).shift(UP * 2)
        self.play(Write(zeta_equation))
        
        # Define function to calculate Riemann Zeta values in the complex plane
        def zeta_func(point):
            x, y = point[:2]
            c = x + y * 1j  # Convert point to complex number
            try:
                zeta_val = mpmath.zeta(c)  # Use mpmath to get zeta value
                return complex(zeta_val).real, complex(zeta_val).imag  # Return real and imag as tuple
            except:
                return 0, 0
        
        # Generate curves with an extended calculation range
        curves = VGroup()  # Group to hold all curves
        for angle in np.linspace(0, 2 * np.pi, 80):  # High density for smooth curves
            curve_points = []
            for radius in np.linspace(0.1, 12, 1200):  # Extended radius to 12, with 350 points for longer lines
                x, y = radius * np.cos(angle), radius * np.sin(angle)
                real, imag = zeta_func((x, y, 0))
                curve_points.append(visible_complex_plane.c2p(real, imag))
            curve = VMobject()
            curve.set_points_smoothly(curve_points)
            curve.set_stroke(color=YELLOW, width=1.0)
            curves.add(curve)
        
        # Show curves
        self.play(Create(curves, run_time=7))

        # Hold final frame for a few seconds
        self.wait(3)

        # Fade out elements
        self.play(FadeOut(curves), FadeOut(zeta_equation), FadeOut(visible_complex_plane), FadeOut(title))

# To run this in a Jupyter Notebook or a Manim command line environment
# use the following command: %%manim -qm ExtendedBeyondViewportRiemannZetaPlot