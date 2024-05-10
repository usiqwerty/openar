from core.headset import Headset
from widgets.fps import FPSCounter

device = Headset()

device.system.add_widget(FPSCounter())
device.system.run_app("apps.About")
device.run()
