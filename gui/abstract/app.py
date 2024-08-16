import numpy as np

import device_config
from core.app_storage import AppManifest
from core.permissions import Permission
from core.permissive import SystemApi
from device_config import screen_size
from gui.abstract.uiwidget import UIWidget
from video.rendering import overlay_images
from video.utils import in_rect


class Application:
    """
    OpenAR Application
    """
    name: str
    screen_size = screen_size
    size: tuple[int, int]
    background: tuple[int, int, int, int]
    elements: list[UIWidget]
    permissions: list[Permission]
    system_api: SystemApi
    angular_position: tuple[float, float]
    drag_angle: tuple[float, float] | None

    def __init__(self, manifest: AppManifest):
        self.angular_position = (0, 0)
        self.background = (255, 255, 255, 255)
        self.elements = []
        self.permissions = []
        self.name = manifest.name
        self.permissions = manifest.permissions
        self.size = manifest.size

        self.frame = np.ndarray((*self.size, 4), dtype=np.uint8)
        self.drag_angle = None

    def on_start(self):
        """
        Application startup handler
        """
        pass

    def render(self) -> np.ndarray:
        """
        Draw frame layer in RGBA mode
        """
        frame = np.full((*self.size[::-1], 4), self.background, dtype=np.uint8)
        for element in self.elements:
            overlay_images(frame, element.draw(), element.x, element.y)

        return frame

    def on_touch(self, touch_position: tuple[int, int]):
        """
        Handle touch action
        :param touch_position: Coordinates
        """
        touch_x = touch_position[0] # - self.position[0]
        touch_y = touch_position[1] # - self.position[1]

        for element in self.elements:
            if in_rect((touch_x, touch_y), (element.x, element.y), (element.width, element.height)):
                element.on_click(*touch_position)
                break

    def on_resize(self, delta_size: tuple[int, int]):
        """
        Handle window resize action
        :param delta_size: window size change
        """
        pass

    def on_drag(self, finger_direction: tuple[float, float]):
        """
        Handle window drag
        :param finger_direction: Index finger direction
        :return:
        """
        fx, fy = finger_direction

        if self.drag_angle:
            dx, dy = self.drag_angle
            x, y = self.angular_position
            # TODO: too accelerated, seems we don't have to add it to
            #  current coordinates
            self.angular_position = (x -( fx-dx), y-(fy-dy))  #(fx - dx, fy - dy)
            # self.drag_angle = finger_direction  # (fx - winx, fy - winy)
        else:
            # winx, winy = self.angular_position
            self.drag_angle =  finger_direction #(fx - winx, fy - winy)

    def on_release(self):
        """
        Called when gesture released
        :return:
        """
        self.drag_angle = None
