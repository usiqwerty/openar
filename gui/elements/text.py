import numpy
import numpy as np
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from gui.abstract.uiwidget import UIWidget


class Text(UIWidget):
    """
    UI Text element
    """

    def __init__(self, text, font_size=24, font_face="LSANS.TTF", thickness=1, x=0, y=0):
        self.text = text
        self.font_size = font_size
        self.font_face = font_face
        self.thickness = thickness
        self.color = (0, 0, 0, 255)
        self.x = x
        self.y = y
        self.height = int(self.font_size * 4 / 3)
        self.width = int(1.6 * self.height * len(self.text))

    def draw(self) -> np.ndarray:
        """
        Draw text element
        @return:
        """
        # TODO: определять размер текста,
        #  чтобы правильно задать размер блока

        pil_canvas = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        drawer = ImageDraw.ImageDraw(pil_canvas)

        font = ImageFont.truetype("fonts/" + self.font_face, self.font_size)

        drawer.text((0, 0), self.text, font=font, fill=(0, 0, 0))
        return numpy.array(pil_canvas)
