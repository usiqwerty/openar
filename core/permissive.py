import time
from types import NoneType
from typing import Callable

import cv2

from core.app_storage import AppManifest
from core.permissions import Permission


class PermissiveCore:
    """
    Generates system API accessor object
    """

    def __init__(self, headset):
        self.headset = headset

    def generate_api_accessor(self, permissions: list[Permission]):
        """
        Creates API accessor object
        @param permissions: list of app permissions to be granted
        @return: SystemAPI object which gives access to OpenAR system tools
        """
        perms = [None, None, None]
        for permission in permissions:
            if permission == Permission.HEADSET:
                perms[0] = self.headset
            if permission == Permission.DISPLAY:
                perms[1] = self.headset.display
            if permission == Permission.INSTALLED_APPLICATIONS:
                perms[2] = self.headset.system.app_storage.get_installed_apps
        return SystemApi(*perms)


class SystemApi:
    """
    System api allows user apps to access OpenAR system
    """
    def __init__(self, headset, display, get_installed_apps):
        self.headset = headset
        self.display = display
        self.get_installed_apps: Callable[[], list[AppManifest]] = get_installed_apps

    def record_display_video(self, length: int):
        if isinstance(self.display, NoneType):
            raise PermissionError("Have no permission to capture display")

        time.sleep(3)
        w, h, c = self.display.camera_frame.shape

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')

        w, h = h, w
        print(w, h)
        fps = 30
        video = cv2.VideoWriter("../video.avi", fourcc, fps, (w, h))

        c = 0
        while c < length * fps:
            video.write(self.display.camera_frame)
            c += 1
            time.sleep(1 / fps)

        print(f"{c} frames written")
        video.release()
