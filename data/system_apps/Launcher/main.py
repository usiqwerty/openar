from gui.abstract.app import Application
from gui.elements.text import Text


class App(Application):
    def on_start(self):
        installed_apps = self.system_api.get_installed_apps()
        y = 10
        gap = 20

        for app in installed_apps:
            label = Text(app.name, x=10, y=y)
            label.on_click = lambda *pos: self.system_api.headset.system.run_app(app.package_name)
            self.elements.append(label)
            y += self.elements[-1].height + gap
