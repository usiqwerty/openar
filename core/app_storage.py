import json
import logging
import os
from dataclasses import dataclass

from core.permissions import Permission
from device_config import root_path


@dataclass
class AppManifest:
    manifest_version: float
    name: str
    permissions: list[Permission]
    size: list[int, int]


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
            try:
                self.append_installed_app(app_name, is_system)
            except FileNotFoundError:
                logging.warning(f"App {app_name} does not have manifest")

    def append_installed_app(self, app_name: str, is_system=False):
        apps_dir = "system_apps" if is_system else "apps"
        manifest_path = '/'.join([root_path, "data", apps_dir, app_name, "manifest.json"])
        with open(manifest_path, encoding='utf-8') as f:
            json_manifest = json.load(f)
        if is_system:
            self.system_apps.append(AppManifest(**json_manifest))
        else:
            self.user_apps.append(AppManifest(**json_manifest))
