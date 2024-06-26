import cv2
import numpy as np

from device_config import camera_size, eye_shift, camera_api

camera_width, camera_height = camera_size


class Camera:
    """
    Camera view service
    """
    frame: np.ndarray

    def __init__(self):
        stream = cv2.VideoCapture(0, camera_api)
        stream.set(cv2.CAP_PROP_FRAME_WIDTH, camera_width)
        stream.set(cv2.CAP_PROP_FRAME_HEIGHT, camera_height)
        # stream.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3)
        stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc(*"MJPG"))

        self.stream = stream
        self.frame = np.zeros([camera_width, camera_height, 4], dtype=np.uint8)

    def pull_frame(self):
        success, actual_image = self.stream.read()

        if not success:
            return

        actual_image = actual_image[:, eye_shift:-eye_shift]
        cv2.cvtColor(actual_image, cv2.COLOR_RGB2RGBA, actual_image)
        self.frame = actual_image

    def job(self):
        print("Camera job started")
        while True:
            self.pull_frame()
