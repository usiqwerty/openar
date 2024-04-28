import numpy as np

from gui.abstract.app import Application
from gui.elements.text import Text


class App(Application):
    def __init__(self):
        super().__init__()
        self.size = (200, 700)
        self.position = (200, 200)
        self.frame = np.ndarray((*self.size, 4))
        self.name = "Camera Recorder"
        self.permissions = ["PERM_DISPLAY"]

        self.elements = [
            Text("Video is recording while this app is running")
        ]

    def on_start(self):
        self.system_api.record_display_video(10)
