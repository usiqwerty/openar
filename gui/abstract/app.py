import numpy as np

from device_config import screen_size
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
    elements: list

    def __init__(self):
        self.position = (0, 0)
        self.background = (240, 240, 240, 255)
        self.elements = []

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
        for (x, y, element) in self.elements:
            overlay_images(frame, element.draw(), x, y)

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