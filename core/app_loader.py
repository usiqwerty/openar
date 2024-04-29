import importlib
import json

from gui.abstract.app import Application
from device_config import root_path


def load_app(app_name) -> Application:
    """
    Load app package from storage
    @param app_name: package to be imported
    @return: app object
    """
    manifest_path = '/'.join([root_path, *app_name.split('.'), "manifest.json"])

    with open(manifest_path, encoding='utf-8') as f:
        app_manifest: dict = json.load(f)

    app_module = importlib.import_module(app_name)

    # TODO: передавать путь к папке с приложением
    app_object: Application = app_module.App(app_manifest)
    return app_object
