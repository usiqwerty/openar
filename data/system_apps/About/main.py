from gui.abstract.app import Application
from gui.elements.text import Text


class App(Application):
    def on_start(self):
        self.elements = [
            Text("The About App", font_size=36, x=0, y=100),
            Text("OpenAR v1.1 dev", x=0, y=200)
        ]
