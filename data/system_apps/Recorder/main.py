from gui.abstract.app import Application
from gui.elements.text import Text


class App(Application):
    def on_start(self):
        self.elements = [
            Text("Video is recording while this app is running")
        ]
        self.system_api.record_display_video(10)
