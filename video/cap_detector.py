import cv2

for thing in dir(cv2):
    if thing.startswith("CAP_") and not thing.startswith("CAP_PROP_"):
        cap_backend = getattr(cv2, thing)
        cap = cv2.VideoCapture(0, cap_backend)
        succ, frame = cap.read()
        if succ:
            print(thing)
        cap.release()