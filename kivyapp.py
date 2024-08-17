import threading
from functools import partial

from kivy.app import App
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.screenmanager import Screen, ScreenManager

from core.headset import Headset


class MainScreen(Screen):
    pass


class Manager(ScreenManager):
    pass


class Main(App):
    main_screen: MainScreen

    def build(self):
        threading.Thread(target=self.run_device, daemon=True).start()

        sm = ScreenManager()
        self.main_screen = MainScreen()
        sm.add_widget(self.main_screen)
        return sm

    def run_device(self):
        device = Headset(lambda x: Clock.schedule_once(partial(self.display_frame, x)))
        device.system.autorun.append("Launcher")
        device.run()

    def display_frame(self, frame, dt):
        # display the current video frame in the kivy Image widget

        # create a Texture the correct size and format for the frame
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')

        # copy the frame data into the texture
        texture.blit_buffer(frame.tobytes(order=None), colorfmt='bgr', bufferfmt='ubyte')

        # flip the texture (otherwise the video is upside down
        texture.flip_vertical()

        # actually put the texture in the kivy Image widget
        self.main_screen.ids.vid.texture = texture
