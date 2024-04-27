from abc import abstractmethod

import numpy as np

from device_config import screen_size


class Application:
    """
    OpenAR Application
    """
    name: str
    screen_size = screen_size
    position: tuple[int, int]
    size: tuple[int, int]

    def __init__(self):
        self.position = (0, 0)

    def on_start(self):
        """
        Application startup handler
        """
        pass

    @abstractmethod
    def render(self) -> np.ndarray:
        """
        Draw frame layer in RGBA mode
        """
        pass

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
