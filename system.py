import threading
from typing import Any

from gui.abstract.app import Application
from gui.abstract.widget import Widget


class System:
    """
    Система
    """
    system_apps: list[Widget | Application]
    user_apps: list[Widget | Application]
    threads: list[tuple[str, Any, threading.Thread]]

    def __init__(self, video_job):
        self.system_apps = []
        self.user_apps = []
        self.video_thread = video_job

    def add_widget(self, widget: Widget):
        self.user_apps.append(widget)

    def run_app(self, app: Application):
        self.user_apps.append(app)
        thread = threading.Thread(name=app.name, target=app.main)
        thread.start()
        self.threads.append((app.name, app.main, thread))

    def run(self):
        """
        Запустить AR шлем в многопоточном. Выполняется, пока не завершатся все потоки
        @return:
        """
        self.threads = [
            # ['camera', camera.job, None],
            # ['widgets', gui_job, None],
            ('display', self.video_thread, None)
            # ["video", video_writer]
        ]

        for i, (name, proc, _) in enumerate(self.threads):
            thread = threading.Thread(name=name, target=proc)
            thread.start()
            self.threads[i] = (name, proc, thread)

        while len(self.threads) > 0:
            name, routine, thread = self.threads[0]
            thread.join()
