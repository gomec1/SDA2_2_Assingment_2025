from dataclasses import dataclass, field
from typing import List, Iterable

from .plugin_base import BasePlugin
from . import plugin_loader


@dataclass
class TextProcessingCore:
    """
    Microkernel core: responsible for I/O and orchestrating plugins.
    It doesn't contain any text processing logic itself.
    """
    plugins: List[BasePlugin] = field(default_factory=list)

    @classmethod
    def from_discovery(cls) -> "TextProcessingCore":
        """Discovers and loads all plugins dynamically."""
        plugins = plugin_loader.load_plugins()
        return cls(plugins=plugins)

    def list_plugins(self) -> List[BasePlugin]:
        """Returns all loaded plugins."""
        return self.plugins

    def apply_plugins(self, text: str, selected_plugin_names: Iterable[str]) -> str:
        """
        Applies selected plugins to the text in the order they're provided.
        If no plugins are selected, returns original text unchanged.
        """
        name_to_plugin = {p.name: p for p in self.plugins}

        processed = text
        for name in selected_plugin_names:
            plugin = name_to_plugin.get(name)
            if plugin is None:
                continue
            processed = plugin.process(processed)
        return processed

    @staticmethod
    def read_text_from_bytes(file_bytes: bytes, encoding: str = "utf-8") -> str:
        """Decode uploaded file bytes into a string."""
        return file_bytes.decode(encoding, errors="replace")

    @staticmethod
    def write_text_to_bytes(text: str, encoding: str = "utf-8") -> bytes:
        """Encode processed text for download as a file."""
        return text.encode(encoding)
