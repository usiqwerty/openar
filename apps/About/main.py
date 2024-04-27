import numpy as np

from gui.abstract.app import Application
from gui.elements.text import Text


class App(Application):
    def __init__(self):
        super().__init__()
        self.name = "About"
        self.size = (500, 700)
        self.position = (0, 100)
        self.frame = np.full((*self.size, 4), (0, 255, 255, 255))

        self.elements += [
            (0, 100, Text("The About App", font_size=3)),
            (0, 200, Text("OpenAR v1.1 dev"))
        ]
