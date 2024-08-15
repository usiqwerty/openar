from math import cos, pi, atan, sqrt, radians

import cv2
import numpy as np

import device_config

radius = device_config.screen_size[0] // 2


def get_window_warp(app_size: tuple[int, int], screen_size: tuple[int, int], angle: float):
    screen_width, screen_height = screen_size
    width, height = app_size

    window_angle = angle

    beta = atan(width / 2 / radius)
    gamma = pi / 2 - window_angle - beta

    left = cos(gamma) > 0
    sign = -1 if left else 1

    dist_to_edge = sqrt(radius ** 2 + (width / 2) ** 2)

    dist_to_edge_projection = dist_to_edge * cos(gamma)
    window_width_projection = width * cos(window_angle)

    x1 = screen_width / 2 + sign * dist_to_edge_projection
    y1 = screen_height / 2 - height / 2
    x2 = x1 + window_width_projection
    y2 = screen_height / 2 + height / 2

    xshift = screen_width / 2 - width / 2 - x1
    return [[xshift + x1, y1], [xshift + x2, y1], [xshift + x1, y2], [xshift + x2, y2]], (
    int(window_width_projection), int(y2 - y1)), xshift


def transform_image(image: np.ndarray, angle: float):
    init_height, init_width, c = image.shape
    screen_width, screen_height = device_config.screen_size
    target_points, new_size, xshift = get_window_warp((init_width, init_height), (screen_width, screen_height),
                                                      radians(angle))

    new_width, new_height = new_size
    pts1 = np.float32([
        [(screen_width - init_width) / 2, (screen_height - init_height) / 2],
        [(screen_width + init_width) / 2, (screen_height - init_height) / 2],
        [(screen_width - init_width) / 2, (screen_height + init_height) / 2],
        [(screen_width + init_width) / 2, (screen_height + init_height) / 2],
    ])
    transform = cv2.getPerspectiveTransform(pts1, np.float32(target_points), cv2.DECOMP_SVD)

    r = cv2.warpPerspective(image, transform, (new_width, new_height))
    x = int(target_points[0][0])
    y = int(target_points[0][1])
    return r, (x - int(xshift), y)
