from core.headset import Headset
from widgets.fps import FPSCounter

device = Headset()

device.system.add_widget(FPSCounter())
device.system.app_storage.find_installed_apps()
device.system.run_app("Launcher", True)
device.run()
