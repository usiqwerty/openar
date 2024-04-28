from abc import abstractmethod

import numpy as np


class UIWidget:
    x: int
    y: int

    @abstractmethod
    def draw(self) -> np.ndarray:
        pass