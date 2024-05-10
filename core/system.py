import threading
from typing import Any

from core.app_loader import load_app
from core.permissive import PermissiveCore
from gui.abstract.app import Application
from gui.abstract.appwidget import Widget
from hands.gesture import Gesture
from hands.tracking_mp_opt import HandTracker


class System:
    """
    OpenAR system
    """
    system_apps: list[Widget | Application]
    user_apps: list[Widget | Application]
    threads: list[tuple[str, Any, threading.Thread]]
    permissive: PermissiveCore
    hand_tracker: HandTracker

    def __init__(self, permissive: PermissiveCore, hand_tracker: HandTracker):
        self.hand_tracker = hand_tracker
        self.hand_tracker.on_gesture_callback = self.on_gesture
        self.system_apps = []
        self.user_apps = []
        self.threads = []
        self.permissive = permissive

        self.silent_add_thread("hand-tracker", hand_tracker.job)

    def add_widget(self, widget: Widget):
        self.user_apps.append(widget)

    def run_app(self, app_name: str):
        """
        Load and run the app
        @param app_name: package name to be imported
        """
        app = load_app(app_name)
        app.system_api = self.permissive.generate_api_accessor(app.permissions)
        self.user_apps.append(app)
        thread = threading.Thread(name=app.name, target=app.on_start)
        # thread.start()
        self.threads.append((app.name, app.on_start, thread))

    def silent_add_thread(self, name: str, routine):
        """
        Add thread without starting it
        @param name: Thread name
        @param routine: function to be run in thread
        """
        self.threads.append((name, routine, threading.Thread(name=name, target=routine)))

    def start_thread(self, name: str, routine):
        self.threads.append((name, routine, threading.Thread(name=name, target=routine)))
        self.threads[-1][2].start()

    def run(self):
        """
        Запустить OpenAR в многопоточном режиме. Выполняется, пока не завершатся все потоки
        @return:
        """

        for name, proc, thread in self.threads:
            if not thread.is_alive():
                print(f"Thread {name} is not alive, starting...")
                thread.start()

        while len(self.threads) > 0:
            name, routine, thread = self.threads[0]
            thread.join()
            self.threads.pop(0)

    def on_gesture(self, gesture: Gesture):
        for app in self.user_apps:
            if not isinstance(app, Application): continue
            print(app.name, gesture)
            if gesture.name == "none":
                print("Release")
                app.on_release()
            if in_rect(gesture.index_finger, app.position, app.size):
                if gesture.name == "triple":
                    app.on_drag(gesture.index_finger)


def in_rect(pos, corner, size):
    """
    Check if point is inside rectangle
    @param pos: point to be checked
    @param corner: upper left corner rectangle
    @param size: rect size
    @return:
    """
    x, y = pos
    rx, ry = corner
    w, h = size
    return rx <= x <= rx + w and ry <= y <= ry + h
