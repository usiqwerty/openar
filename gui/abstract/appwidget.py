from abc import abstractmethod

from device_config import screen_size


class AppWidget:
    """
    A brief application to display information
    """
    screen_size = screen_size
    position: tuple[int, int]
    size: tuple[int, int]

    def __init__(self):
        self.position = (0, 0)

    @abstractmethod
    def render(self):
        """
        Render AppWidget content in RGBA mode
        """
        pass

    def on_touch(self, touch_position: tuple[int, int]):
        """
        Handle touch action
        @param touch_position: Coordinates
        @return:
        """
        pass
