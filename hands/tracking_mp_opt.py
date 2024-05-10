import cv2
import mediapipe as mp
import numpy as np
from cvzone.SelfiSegmentationModule import SelfiSegmentation

from hands.gesture import Gesture
from video.camera import Camera

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=2,
                       min_detection_confidence=0.5,
                       min_tracking_confidence=0.5)

segmentor = SelfiSegmentation()


class HandTracker:
    frame: np.ndarray
    mask: np.ndarray
    camera: Camera
    x: int
    y: int
    fingers: list[list[int]]
    on_gesture_callback = lambda s, x: None

    def __init__(self, camera: Camera):
        self.camera = camera
        self.frame = np.zeros((100, 100, 3))
        self.x = 0
        self.y = 0
        self.hands = np.zeros((10, 10, 4), dtype=np.uint8)
        self.fingers = []

    def remove_background(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        ret, mask = cv2.threshold(gray, 5, 255, cv2.THRESH_TRIANGLE)
        mask = cv2.bitwise_not(mask)
        kernel = np.ones((9, 9), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        result = img.copy()
        result = cv2.cvtColor(result, cv2.COLOR_BGR2BGRA)
        result[:, :, 3] = mask
        return result, mask

    def find_and_get_hands(self, image):
        results = hands.process(image)

        lmList = []
        miny = 0
        minx = 0
        maxy = 0
        maxx = 0
        mask = np.zeros((10, 10))
        if results.multi_hand_landmarks:
            myHand = results.multi_hand_landmarks[0]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                image = cv2.drawMarker(image, (cx, cy), (255, 0, 0))
        if (len(lmList) >= 20):
            xlist = []
            ylist = []

            for ids in lmList:
                xlist.append(ids[1])
                ylist.append(ids[2])

            minx = min(xlist) - 40
            maxx = max(xlist) + 40
            miny = min(ylist) - 40
            maxy = max(ylist) + 40

            minx = max(minx, 1)
            maxx = max(maxx, 1)
            maxy = max(maxy, 1)
            miny = max(miny, 1)

            image = image[miny:maxy, minx:maxx]
            image, mask = self.remove_background(image)

        return image, lmList, miny, minx, maxy, maxx, mask

    def job(self):
        is_gesture = False
        while True:
            hands, fingers, miny, minx, maxy, maxx, mask = self.find_and_get_hands(self.camera.frame[:, :, :3].copy())
            self.x = minx
            self.y = miny

            self.hands = cv2.cvtColor(mask.astype(np.uint8), cv2.COLOR_GRAY2BGRA)
            self.hands[:, :, 3] = mask.astype(np.uint8)

            if fingers:
                self.big = np.array(fingers[4][1:])
                self.index = np.array(fingers[8][1:])
                self.middle = np.array(fingers[12][1:])
                self.ring = np.array(fingers[16][1:])
                self.pinky = np.array(fingers[20][1:])

                double = np.linalg.norm(self.big - self.index)
                triple = np.linalg.norm(self.big - self.index + self.big - self.middle)

                maximum = np.linalg.norm(self.big - self.pinky)

                double_closeness = int(100 * double / maximum)
                triple_closeness = int(100 * triple / maximum)
                threshold = 30

                finger_x = self.index[0]
                finger_y = self.index[1]

                print(double_closeness, triple_closeness)
                if triple_closeness < threshold*2:
                    is_gesture = True
                    self.on_gesture_callback(Gesture(name="triple", index_finger=(finger_x, finger_y)))
                elif double_closeness < threshold:
                    is_gesture = True
                    self.on_gesture_callback(Gesture(name="double", index_finger=(finger_x, finger_y)))
                else:
                    if is_gesture:
                        is_gesture = False
                        self.on_gesture_callback(Gesture(name="none", index_finger=(finger_x, finger_y)))
            else:
                if is_gesture:
                    is_gesture = False
                    self.on_gesture_callback(Gesture(name="none", index_finger=(finger_x, finger_y)))