import typing

import cv2
import numpy as np
from mediapipe.python.solutions import hands as mp_hands


def remove_background(img: np.ndarray):
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


def find_and_get_hands(image: np.ndarray):
    results: SolutionResult = hands_processor.process(image)

    landmarks = []
    min_y = 0
    min_x = 0
    max_y = 0
    max_x = 0

    mask = np.zeros((10, 10))
    if results.multi_hand_landmarks:
        hand = results.multi_hand_landmarks[0]
        for lm_id, landmark in enumerate(hand.landmark):
            h, w, c = image.shape
            cx, cy = int(landmark.x * w), int(landmark.y * h)
            landmarks.append([lm_id, cx, cy])
            image = cv2.drawMarker(image, (cx, cy), (255, 0, 0))
    if len(landmarks) >= 20:
        min_x = 10000
        min_y = 10000
        max_x = 0
        max_y = 0

        for lm_id, x, y in landmarks:
            max_x = max(x, max_x)
            max_y = max(y, max_y)

            min_x = min(x, min_x)
            min_y = min(y, min_y)

        min_x = max(min_x - 40, 1)
        min_y = max(min_y - 40, 1)
        max_x += 40
        max_y += 40

        image = image[min_y:max_y, min_x:max_x]
        image, mask = remove_background(image)

    return image, landmarks, min_y, min_x, max_y, max_x, mask


SolutionResult = typing.NamedTuple("SolutionResult", [
    ("multi_hand_landmarks", list),
    ("multi_hand_world_landmarks", list),
    ("multi_handedness", list),

])
hands_processor = mp_hands.Hands(static_image_mode=False,
                                 max_num_hands=2,
                                 min_detection_confidence=0.5,
                                 min_tracking_confidence=0.5)
