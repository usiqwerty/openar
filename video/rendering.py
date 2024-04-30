import cv2
import numpy as np
from numba import njit


# @njit(parallel=True)
def overlay_images(background: np.ndarray, overlay: np.ndarray, x, y):
    height, width, _ = background.shape
    over_hei, over_wid, _ = overlay.shape
    y_end = min(y + over_hei, height)
    x_end = min(x + over_wid, width)
    over_y_end = y_end - y
    over_x_end = x_end - x

    alpha = overlay[:over_y_end, :over_x_end, 3] / 255.0

    for c in range(0, 3):
        fg = overlay[:over_y_end, :over_x_end, c] * alpha
        bg = background[y:y_end, x:x_end, c] * (1.0 - alpha)
        background[y:y_end, x:x_end, c] = bg + fg
