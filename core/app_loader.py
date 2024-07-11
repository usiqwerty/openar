import importlib
import json
import traceback

from device_config import root_path
from gui.abstract.app import Application


class AppNotLoaded(Exception):
    pass


def load_app(app_name) -> Application:
    """
    Load app package from storage
    @param app_name: package to be imported
    @return: app object
    """
    manifest_path = '/'.join([root_path, *app_name.split('.'), "manifest.json"])

    try:
        with open(manifest_path, encoding='utf-8') as f:
            app_manifest: dict = json.load(f)
    except FileNotFoundError:
        raise AppNotLoaded(f"Could not find manifest: {manifest_path}")

    try:
        app_module = importlib.import_module(f"{app_name}.main")
    except ModuleNotFoundError:
        raise AppNotLoaded(f"Package has no 'main' module: {app_name}")

    try:
        # TODO: передавать путь к папке с приложением
        app_object: Application = app_module.App(app_manifest)
        return app_object
    except Exception as e:
        print(traceback.format_exc())
        raise AppNotLoaded(f"Exception happened while loading app: {e}") from e
