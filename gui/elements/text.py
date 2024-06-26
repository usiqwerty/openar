import cv2
import numpy as np

from gui.abstract.uiwidget import UIWidget


class Text(UIWidget):
    """
    UI Text element
    """

    def __init__(self, text, font_size=1, font_face=cv2.FONT_HERSHEY_SIMPLEX, thickness=1, x=0, y=0):
        self.text = text
        self.font_size = font_size
        self.font_face = font_face
        self.thickness = thickness
        self.color = (0, 0, 0, 255)
        self.x = x
        self.y = y

    def draw(self) -> np.ndarray:
        """
        Draw text element
        @return:
        """
        # TODO: определять размер текста,
        #  чтобы правильно задать размер блока
        w, h = cv2.getTextSize(self.text, self.font_face, self.font_size, self.thickness)[0]
        canvas = np.zeros((2 * h, w, 4), dtype=np.uint8)
        return cv2.putText(canvas, self.text, (0, h), self.font_face, self.font_size, self.color)
