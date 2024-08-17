import cv2
import numpy as np

from device_config import imshow_delay


def show_frame(frame: np.ndarray):
    cv2.imshow("full", frame)
    if cv2.waitKey(imshow_delay) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        exit(0)