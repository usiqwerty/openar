import numpy as np

from device_config import screen_size
from gui.abstract.uiwidget import UIWidget
from core.permissive import SystemApi
from video.rendering import overlay_images


class Application:
    """
    OpenAR Application
    """
    name: str
    screen_size = screen_size
    position: tuple[int, int]
    size: tuple[int, int]
    background: tuple[int, int, int, int]
    elements: list[UIWidget]
    permissions: list[str]
    system_api: SystemApi

    def __init__(self, manifest: dict):
        self.position = (0, 0)
        self.background = (255, 255, 255, 255)
        self.elements = []
        self.permissions = []
        self.name = manifest["name"]
        self.permissions = manifest['permissions']
        self.size = tuple(manifest["size"][::-1])
        self.frame = np.ndarray((*self.size, 4))

    def on_start(self):
        """
        Application startup handler
        """
        pass

    def render(self) -> np.ndarray:
        """
        Draw frame layer in RGBA mode
        """
        frame = np.full((*self.size, 4), self.background)
        for element in self.elements:
            overlay_images(frame, element.draw(), element.x, element.y)

        return frame

    def on_touch(self, touch_position: tuple[int, int]):
        """
        Handle touch action
        @param touch_position: Coordinates
        """
        pass

    def on_resize(self, delta_size: tuple[int, int]):
        """
        Handle window resize action
        @param delta_size: window size change
        """
        pass
