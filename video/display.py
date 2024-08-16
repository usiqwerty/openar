import cv2
import numpy as np

from core.system import System
from device_config import camera_size, imshow_delay, screen_size
from hands.tracking_mp_opt import HandTracker
from video.camera import Camera
from video.rendering import overlay_images
from video.virtual3d import transform_image

camera_width, camera_height = camera_size

camera_center = camera_width // 2

UP = 2490368
DOWN = 2621440
LEFT = 2424832
RIGHT = 2555904
step = 5


class Display:
    detector: HandTracker
    camera: Camera
    system: System
    camera_frame: np.ndarray
    sight_direction: tuple[float, float]

    def __init__(self, camera: Camera, system: System):
        self.camera = camera
        self.system = system
        self.detector = system.hand_tracker
        self.sight_direction = (0, 0)

    def show_video(self):
        print('Display job started')
        while True:
            self.camera.pull_frame()
            self.camera_frame = self.camera.frame

            sx, sy = self.sight_direction
            for widget in self.system.user_apps + self.system.system_apps:
                app_frame = widget.render()

                x, y = widget.angular_position

                ang = x - sx, y - sy
                final_frame, pos = transform_image(app_frame, ang)
                overlay_images(self.camera_frame, final_frame, pos[0], pos[1])

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
            elif cv2.waitKeyEx(imshow_delay) == LEFT:
                sx -= step
            elif cv2.waitKeyEx(imshow_delay) == RIGHT:
                sx += step
            elif cv2.waitKeyEx(imshow_delay) == UP:
                sy += step
            elif cv2.waitKeyEx(imshow_delay) == DOWN:
                sy -= step
            sx = min(max(-80.0, sx), 80.0)
            sy = min(max(-80.0, sy), 80.0)
            self.sight_direction = (sx, sy)
