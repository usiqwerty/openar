import importlib
import traceback

from core.app_storage import AppStorage
from gui.abstract.app import Application


class AppNotLoaded(Exception):
    pass


def load_app(app_name: str, app_storage: AppStorage) -> Application:
    """
    Load app package from storage
    :param app_name: package name to be imported
    :param app_storage: applications storage accessor
    :return: app object
    """

    # manifest_path = '/'.join([root_path, "data", app_dir, app_name, "manifest.json"])

    try:
        app_manifest = app_storage.get_manifest(app_name)
    except NameError as e:
        raise AppNotLoaded(f"Could not find app manifest: {app_name}") from e

    app_dir = "system_apps" if app_manifest.is_system else "apps"
    try:
        app_module = importlib.import_module(f"data.{app_dir}.{app_name}.main")
    except ModuleNotFoundError:
        raise AppNotLoaded(f"Package has no 'main' module: {app_name}")

    try:
        # TODO: передавать путь к папке с приложением
        app_object: Application = app_module.App(app_manifest)
        return app_object
    except Exception as e:
        print(traceback.format_exc())
        raise AppNotLoaded(f"Exception happened while loading app: {e}") from e
