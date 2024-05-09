import numpy as np


# @njit(parallel=True)
def overlay_images(background: np.ndarray, overlay: np.ndarray, x: int, y: int):
    height, width, _ = background.shape
    over_hei, over_wid, _ = overlay.shape

    lost_x = max(-x, 0)
    lost_y = max(-y, 0)

    bg_x_start = x + lost_x
    bg_y_start = y + lost_y
    bg_x_end = max(min(bg_x_start - lost_x + over_wid, width), 0)
    bg_y_end = max(min(bg_y_start - lost_y + over_hei, height), 0)

    over_x_start = lost_x
    over_y_start = lost_y
    over_x_end = over_x_start+bg_x_end - bg_x_start
    over_y_end = over_y_start + bg_y_end - bg_y_start

    alpha = (overlay[lost_y:over_y_end, lost_x:over_x_end, 3] / 255).astype(np.uint8)

    for c in range(0, 3):
        background[bg_y_start:bg_y_end, bg_x_start:bg_x_end, c] += (overlay[over_y_start:over_y_end,
                                                                    over_x_start:over_x_end, c] - background[
                                                                                                  bg_y_start:bg_y_end,
                                                                                                  bg_x_start:bg_x_end,
                                                                                                  c]) * alpha
