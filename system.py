import threading
from typing import Any

from gui.abstract.app import Application
from gui.abstract.widget import Widget


class System:
    """
    OpenAR system
    """
    system_apps: list[Widget | Application]
    user_apps: list[Widget | Application]
    threads: list[tuple[str, Any, threading.Thread]]

    def __init__(self):
        self.system_apps = []
        self.user_apps = []
        self.threads = []

    def add_widget(self, widget: Widget):
        self.user_apps.append(widget)

    def run_app(self, app: Application):
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
        # self.threads += [
        #     # ['camera', camera.job, None],
        #     # ['widgets', gui_job, None],
        #     ('display', self.video_thread, None)
        #     # ["video", video_writer]
        # ]

        for name, proc, thread in self.threads:
            if not thread.is_alive():
                print(f"Thread {name} is not alive, starting...")
                thread.start()

        while len(self.threads) > 0:
            name, routine, thread = self.threads[0]
            thread.join()
            self.threads.pop(0)
