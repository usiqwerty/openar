import os
import cv2

camera_size = (720*2, 720)
screen_size = (1280, 720)

eye_shift = camera_size[0]//50
imshow_delay = 10

root_path = os.path.dirname(os.path.abspath(__file__))

if os.name == "posix":
    camera_api = cv2.CAP_V4L2
elif os.name == "nt":
    camera_api = cv2.CAP_DSHOW

enable_hand_tracking = False
