from core.permissive import PermissiveCore
from core.system import System
from video.camera import Camera
from video.display import Display


class Headset:
    """
    Аппаратная конфигурация устройства
    """
    system: System
    camera: Camera
    display: Display

    def __init__(self):
        self.camera = Camera()
        self.permissive = PermissiveCore(self)
        self.system = System(self.permissive)
        self.display = Display(self.camera, self.system)
        self.system.silent_add_thread('display', self.display.show_video)

    def run(self):
        self.system.run()