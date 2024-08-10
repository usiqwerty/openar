import threading
from typing import Any

from core.app_loader import load_app
from core.app_storage import AppStorage
from core.permissive import PermissiveCore
from gui.abstract.app import Application
# from gui.abstract.appwidget import AppWidget
from hands.gesture import Gesture, GestureName
from hands.tracking_mp_opt import HandTracker
from video.utils import in_rect


class System:
    """
    OpenAR system
    """
    system_apps: list[Application]
    user_apps: list[Application]
    threads: list[tuple[str, Any, threading.Thread]]
    autorun: list[str]
    app_storage: AppStorage
    permissive: PermissiveCore
    hand_tracker: HandTracker

    def __init__(self, permissive: PermissiveCore, hand_tracker: HandTracker):
        self.hand_tracker = hand_tracker
        self.hand_tracker.on_gesture_callback = self.on_gesture
        self.system_apps = []
        self.user_apps = []
        self.threads = []
        self.autorun = []
        self.permissive = permissive
        self.app_storage = AppStorage()
        self.silent_add_thread("hand-tracker", hand_tracker.job)


    def run_app(self, app_name: str, system=False):
        """
        Load and run the app
        :param app_name: package name to be imported
        :param system: whether app is system or not
        """
        app = load_app(app_name, self.app_storage)
        app.system_api = self.permissive.generate_api_accessor(app.permissions)
        self.user_apps.append(app)
        thread = threading.Thread(name=app.name, target=app.on_start)
        # thread.start()
        self.threads.append((app.name, app.on_start, thread))

    def silent_add_thread(self, name: str, routine):
        """
        Add thread without starting it
        :param name: Thread name
        :param routine: function to be run in thread
        """
        self.threads.append((name, routine, threading.Thread(name=name, target=routine)))

    def start_thread(self, name: str, routine):
        self.threads.append((name, routine, threading.Thread(name=name, target=routine)))
        self.threads[-1][2].start()

    def run(self):
        """
        Запустить OpenAR в многопоточном режиме. Выполняется, пока не завершатся все потоки
        """
        self.app_storage.find_installed_apps()
        for package_name in self.autorun:
            self.run_app(package_name)
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
            if not isinstance(app, Application):
                continue
            if gesture.name == GestureName.NoGesture:
                app.on_release()
            if in_rect(gesture.index_finger, app.position, app.size):
                if gesture.name == GestureName.Triple:
                    app.on_drag(gesture.index_finger)
                if gesture.name == GestureName.Double:
                    app.on_touch(gesture.index_finger)
