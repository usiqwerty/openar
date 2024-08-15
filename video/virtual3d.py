from math import cos, pi, atan, sqrt, radians

import cv2
import numpy as np

import device_config

radius = device_config.screen_size[0] // 2


def calculate_coodrinate_by_angle(screen_side: int, window_side: int, angle: float):
    window_angle = angle
    beta = atan(window_side / 2 / radius)
    gamma = pi / 2 - window_angle - beta

    left = cos(gamma) > 0
    sign = -1 if left else 1

    dist_to_edge = sqrt(radius ** 2 + (window_side / 2) ** 2)
    dist_to_edge_projection = dist_to_edge * cos(gamma)
    window_side_projection = window_side * cos(window_angle)
    x1 = screen_side / 2 + sign * dist_to_edge_projection
    x2 = x1 + window_side_projection

    x1_init = screen_side / 2 - window_side / 2
    xshift = x1_init - x1

    return x1, x2, xshift


def get_window_warp(app_size: tuple[int, int], screen_size: tuple[int, int], angular_position: tuple[float, float]):
    screen_width, screen_height = screen_size
    width, height = app_size
    xangle, yangle = angular_position
    x1, x2, xshift = calculate_coodrinate_by_angle(screen_width, width, xangle)
    y1, y2, yshift = calculate_coodrinate_by_angle(screen_height, height, yangle)

    # y1 = screen_height / 2 - height / 2
    # y2 = screen_height / 2 + height / 2

    return ([[xshift + x1, yshift + y1],
             [xshift + x2, yshift + y1],
             [xshift + x1, yshift + y2],
             [xshift + x2, yshift + y2]],
            (int(x2 - x1), int(y2 - y1)),
            (xshift, yshift))


def transform_image(image: np.ndarray, angular_position: tuple[float, float]):
    init_height, init_width, c = image.shape
    screen_width, screen_height = device_config.screen_size
    radian_ang_pos = (radians(angular_position[0]), radians(angular_position[1]))
    target_points, new_size, (xshift, yshift) = get_window_warp((init_width, init_height),
                                                                (screen_width, screen_height),
                                                                radian_ang_pos)

    new_width, new_height = new_size
    pts1 = [
        [(screen_width - init_width) / 2, (screen_height - init_height) / 2],
        [(screen_width + init_width) / 2, (screen_height - init_height) / 2],
        [(screen_width - init_width) / 2, (screen_height + init_height) / 2],
        [(screen_width + init_width) / 2, (screen_height + init_height) / 2],
    ]
    print(pts1)
    print(target_points)
    print(xshift, yshift)
    transform = cv2.getPerspectiveTransform(np.float32(pts1), np.float32(target_points), cv2.DECOMP_LU)

    r = cv2.warpPerspective(image, transform, (new_width, new_height))
    x = int(target_points[0][0] - xshift)
    y = int(target_points[0][1] - yshift)
    # cv2.imshow("full", r)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     cv2.destroyAllWindows()
    #     exit(0)
    return r, (x, y)
