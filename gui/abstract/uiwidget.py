from abc import abstractmethod

import numpy as np


class UIWidget:
    """
    Basic element of user interface in application
    """
    x: int
    y: int

    @abstractmethod
    def draw(self) -> np.ndarray:
        """
        Render widget content
        @return: Ready widget image
        """
