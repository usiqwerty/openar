import numpy as np

from gui.abstract.app import Application
from gui.elements.text import Text


class App(Application):
    def __init__(self, manifest: dict):
        super().__init__(manifest)
        self.name = "About"
        self.size = (500, 700)
        self.position = (0, 100)
        self.frame = np.ndarray((*self.size, 4))

        self.elements = [
            Text("The About App", font_size=3, x=0, y=100),
            Text("OpenAR v1.1 dev", x=0, y=200)
        ]
