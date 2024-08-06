from abc import abstractmethod

import numpy as np


class UIWidget:
    """
    Basic element of user interface in application
    """
    x: int
    y: int
    width: int
    height: int

    @abstractmethod
    def draw(self) -> np.ndarray:
        """
        Render widget content
        @return: Ready widget image
        """

    def on_click(self, x: int, y: int) -> None:
        """
        Process two-finger pinch gesture
        :param x: index finger X coordinate
        :param y: index finger Y coordinate
        """
        pass
