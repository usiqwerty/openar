import numpy as np


# @njit(parallel=True)
def overlay_images(background: np.ndarray, overlay: np.ndarray, x: int, y: int):
    bg_height, bg_width, _ = background.shape
    over_height, over_width, _ = overlay.shape

    lost_width = max(-x, 0)
    lost_height = max(-y, 0)

    bg_x_start = x + lost_width
    bg_y_start = y + lost_height
    bg_x_end = max(min(bg_x_start + (over_width - lost_width), bg_width), 0)
    bg_y_end = max(min(bg_y_start + (over_height - lost_height), bg_height), 0)

    over_x_start = lost_width
    over_y_start = lost_height
    over_x_end = over_x_start + bg_x_end - bg_x_start
    over_y_end = over_y_start + bg_y_end - bg_y_start

    alpha = (overlay[over_y_start:over_y_end, over_x_start:over_x_end, 3] / 255).astype(np.uint8)

    for c in range(0, 3):
        background[bg_y_start:bg_y_end, bg_x_start:bg_x_end, c] += \
            (overlay[over_y_start:over_y_end, over_x_start:over_x_end, c] -
             background[bg_y_start:bg_y_end, bg_x_start:bg_x_end, c]) * alpha
