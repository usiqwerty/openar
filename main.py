from core.headset import Headset
# from widgets.fps import FPSCounter

device = Headset()

# device.system.add_widget(FPSCounter())
device.system.autorun.append("FPSCounter")
device.system.autorun.append("Launcher")
device.run()
