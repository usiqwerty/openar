import importlib
import json
import traceback

from core.app_storage import AppManifest
from device_config import root_path
from gui.abstract.app import Application


class AppNotLoaded(Exception):
    pass


def load_app(app_name: str, system: bool = False) -> Application:
    """
    Load app package from storage
    @param app_name: package name to be imported
    @param system: whether app is system or not
    @return: app object
    """
    app_dir = "system_apps" if system else "apps"
    manifest_path = '/'.join([root_path, "data", app_dir, app_name, "manifest.json"])

    try:
        with open(manifest_path, encoding='utf-8') as f:
            app_manifest: dict = json.load(f)
    except FileNotFoundError:
        raise AppNotLoaded(f"Could not find manifest: {manifest_path}")

    try:
        app_module = importlib.import_module(f"data.{app_dir}.{app_name}.main")
    except ModuleNotFoundError:
        raise AppNotLoaded(f"Package has no 'main' module: {app_name}")
    app_module.App: type[Application]
    try:
        # TODO: передавать путь к папке с приложением
        app_object: Application = app_module.App(AppManifest(**app_manifest))
        return app_object
    except Exception as e:
        print(traceback.format_exc())
        raise AppNotLoaded(f"Exception happened while loading app: {e}") from e
