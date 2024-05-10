import cv2
import numpy as np

from device_config import camera_size, imshow_delay, screen_size
from core.system import System
from hands.tracking_mp_opt import HandTracker
from video.camera import Camera
from video.rendering import overlay_images

camera_width, camera_height = camera_size

camera_center = camera_width // 2


class Display:
    detector: HandTracker
    camera: Camera
    system: System
    camera_frame: np.ndarray

    def __init__(self, camera: Camera, system: System):
        self.camera = camera
        self.system = system
        self.detector = system.hand_tracker

    def show_video(self):
        print('Display job started')
        while True:
            self.camera.pull_frame()
            self.camera_frame = self.camera.frame
            orig = self.camera_frame.copy()
            for widget in self.system.user_apps + self.system.system_apps:
                overlay_images(self.camera_frame, widget.render(), widget.position[0], widget.position[1])

            overlay_images(self.camera_frame, self.detector.hands, self.detector.x, self.detector.y)
            eye_width = camera_width // 2

            left = self.camera_frame[:, :eye_width]
            right = self.camera_frame[:, -eye_width:]

            full_frame = np.concatenate((left, right), axis=1)

            final = cv2.resize(full_frame, screen_size)

            cv2.imshow("full", final)
            if cv2.waitKey(imshow_delay) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                exit(0)
