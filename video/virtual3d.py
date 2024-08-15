from math import cos, pi, atan

import cv2
import numpy as np

import device_config

distance = 1000


def get_window_warp(app_size: tuple[int, int], screen_size: tuple[int, int], angle: float):
    screen_with, screen_height = screen_size
    width, heigth = app_size

    left = angle < 0
    window_angle = abs(angle)

    beta = atan(width / 2 / distance)
    gamma = pi / 2 - window_angle - beta

    dist_from_center = (distance ** 2 + (width / 2) ** 2) * cos(gamma)

    sign = -1 if left else 1
    x1 = screen_with / 2 - width / 2  # + sign * dist_from_center
    y1 = screen_height / 2 - heigth / 2
    x2 = x1 + width  # * cos(window_angle)
    y2 = screen_height / 2 + heigth / 2

    return [[x1, y1], [x2, y1], [x1, y2], [x2, y2]]


def transform_image(image: np.ndarray):
    height, width, c = image.shape
    screen_width, screen_height = device_config.screen_size
    target_points = get_window_warp((width, height), (screen_width, screen_height), 0)

    pts1 = np.float32([
        [(screen_width - width) / 2, (screen_height - height) / 2],
        [(screen_width + width) / 2, (screen_height - height) / 2],
        [(screen_width - width) / 2, (screen_height + height) / 2],
        [(screen_width + width) / 2, (screen_height + height) / 2],
    ])
    transform = cv2.getPerspectiveTransform(pts1, np.float32(target_points))

    return cv2.warpPerspective(image, transform, (width, height))
