import numpy as np

from gui.abstract.app import Application
from gui.elements.text import Text
from video.rendering import overlay_images


class App(Application):
    def render(self) -> np.ndarray:
        for (x, y, element) in self.elements:
            overlay_images(self.frame, element.draw(), x, y)

        return self.frame

    def on_start(self):
        self.elements.append((0, 100, Text("The About App", font_size=3)))

    def __init__(self):
        super().__init__()
        self.name = "About"
        self.size = (500, 700)
        self.frame = np.full((*self.size, 4), (0, 255, 255, 255))
        self.elements = []
