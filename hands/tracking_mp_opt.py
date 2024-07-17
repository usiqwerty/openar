import cv2
import numpy as np

from hands.extractor import find_and_get_hands
from hands.gesture import Gesture, GestureName
from video.camera import Camera


class HandTracker:
    frame: np.ndarray
    mask: np.ndarray
    camera: Camera

    x: int
    "min x position of hand image"

    y: int
    "min y position of hand image"

    hands: np.ndarray
    "hands image to be overlay"

    on_gesture_callback = lambda s, x: None
    "called if gesture is shown"
    threshold = 30

    def __init__(self, camera: Camera):
        self.camera = camera
        self.frame = np.zeros((100, 100, 3))
        self.x = 0
        self.y = 0
        self.hands = np.zeros((10, 10, 4), dtype=np.uint8)

    def job(self):
        is_gesture = False

        finger_x = 0
        finger_y = 0
        while True:
            hands, fingers, min_y, min_x, max_y, max_x, mask = find_and_get_hands(self.camera.frame[:, :, :3].copy())
            self.x = min_x
            self.y = min_y

            self.hands = cv2.cvtColor(mask.astype(np.uint8), cv2.COLOR_GRAY2BGRA)
            self.hands[:, :, 3] = mask.astype(np.uint8)

            if fingers:
                finger_x, finger_y, is_gesture = self.recognize_gesture(fingers, is_gesture)
            else:
                if is_gesture:
                    is_gesture = False
                    self.on_gesture_callback(Gesture(name=GestureName.NoGesture, index_finger=(finger_x, finger_y)))

    def recognize_gesture(self, fingers, is_gesture):
        big = np.array(fingers[4][1:])
        index = np.array(fingers[8][1:])
        middle = np.array(fingers[12][1:])
        ring = np.array(fingers[16][1:])
        pinky = np.array(fingers[20][1:])

        double = np.linalg.norm(big - index)
        triple = np.linalg.norm(big - index + big - middle)
        maximum = np.linalg.norm(big - pinky)

        double_closeness = int(100 * double / maximum)
        triple_closeness = int(100 * triple / maximum)

        finger_x = int(index[0])
        finger_y = int(index[1])

        # TODO: call back outside this method
        if triple_closeness < self.threshold * 2:
            is_gesture = True
            self.on_gesture_callback(Gesture(name=GestureName.Triple, index_finger=(finger_x, finger_y)))
        elif double_closeness < self.threshold:
            is_gesture = True
            self.on_gesture_callback(Gesture(name=GestureName.Double, index_finger=(finger_x, finger_y)))
        else:
            if is_gesture:
                is_gesture = False
                self.on_gesture_callback(Gesture(name=GestureName.NoGesture, index_finger=(finger_x, finger_y)))
        return finger_x, finger_y, is_gesture
