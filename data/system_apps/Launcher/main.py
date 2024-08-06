from gui.abstract.app import Application
from gui.elements.text import Text


class App(Application):
    def on_start(self):
        installed_apps = self.system_api.get_installed_apps()

        y = 10
        line_height = 50

        for app in installed_apps:
            self.elements.append(Text(app.name, x=10, y=y))
            y += self.elements[-1].height
