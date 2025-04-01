
from manim import *

class MyScene(Scene):
    def construct(self):
        text = Tex(r"This is \LaTeX!")
        self.add(text)
        self.wait(2)
