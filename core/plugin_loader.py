import importlib
import inspect
import pkgutil
from typing import List, Type

from .plugin_base import BasePlugin


def discover_plugin_classes(package_name: str = "plugins") -> List[Type[BasePlugin]]:
    """.
    This is the 'plugin registry' of the microkernel.
    """
    plugin_classes: List[Type[BasePlugin]] = []
    try:
        package = importlib.import_module(package_name)
    except ModuleNotFoundError:
        # No plugins package -> core still work
        return plugin_classes

    for module_info in pkgutil.iter_modules(package.__path__, package.__name__ + "."):
        module_name = module_info.name
        try:
            module = importlib.import_module(module_name)
        except Exception:
            # Bad/broken plugins don't crash the core
            continue

        for _, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, BasePlugin) and obj is not BasePlugin:
                plugin_classes.append(obj)

    return plugin_classes


def load_plugins(package_name: str = "plugins") -> List[BasePlugin]:
    """
    Creates objects for all discovered plugin classes.
    If a plugin fails to instantiate, we skip it.
    """
    instances: List[BasePlugin] = []
    for cls in discover_plugin_classes(package_name):
        try:
            instances.append(cls())
        except Exception:
            # Broken plugin constructor -> ignore
            continue
    return instances
