import json
import logging
import os

from core.permissions import Permission
from device_config import root_path


class AppManifest:
    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            match key:
                case "permissions":
                    self.permissions = [Permission(p) for p in val]
                case _:
                    setattr(self, key, val)

    manifest_version: float
    name: str
    package_name: str
    permissions: list[Permission]
    size: tuple[int, int]
    is_system: bool


class AppStorage:
    system_apps: list[AppManifest]
    user_apps: list[AppManifest]

    def __init__(self):
        self.system_apps = []
        self.user_apps = []

    def find_installed_apps(self):
        sys_apps_dir = '/'.join([root_path, "data", "system_apps"])
        user_apps_dir = '/'.join([root_path, "data", "apps"])

        self.add_apps(os.listdir(user_apps_dir), False)
        self.add_apps(os.listdir(sys_apps_dir), True)

    def add_apps(self, apps: list[str], is_system):
        for app_name in apps:
            self.append_installed_app(app_name, is_system)

    def append_installed_app(self, app_name: str, is_system=False):
        apps_dir = "system_apps" if is_system else "apps"
        manifest_path = '/'.join([root_path, "data", apps_dir, app_name, "manifest.json"])
        try:
            with open(manifest_path, encoding='utf-8') as f:
                json_manifest = json.load(f)

            manifest = AppManifest(**json_manifest, package_name=app_name, is_system=is_system)
            if is_system:
                self.system_apps.append(manifest)
            else:
                self.user_apps.append(manifest)
        except FileNotFoundError:
            logging.warning(f"App {app_name} does not have manifest")

    def get_installed_apps(self):
        return self.user_apps + self.system_apps

    def get_manifest(self, package_name: str):
        for app in self.get_installed_apps():
            if app.package_name == package_name:
                return app
        raise NameError(package_name)
