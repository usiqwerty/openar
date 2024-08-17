from core.permissive import PermissiveCore
from core.system import System
from video.camera import Camera
from video.display import Display
from hands.tracking_mp_opt import HandTracker


class Headset:
    """
    Аппаратная конфигурация устройства
    """
    system: System
    camera: Camera
    display: Display

    def __init__(self, show_frame):
        self.camera = Camera()
        self.show_frame = show_frame
        self.permissive = PermissiveCore(self)

        self.system = System(self.permissive, HandTracker(self.camera))
        self.display = Display(self.camera, self.system, self.show_frame)
        self.system.silent_add_thread('display', self.display.show_video)

    def run(self):
        self.system.run()
